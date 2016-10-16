import time,os,linecache,random,_thread

def precaution():
	time.sleep(3600)
	os._exit(0)
_thread.start_new_thread(precaution,())

#internal key-value pair for cat state
#three states for chase cat : s(searching),w(waiting for attack),p(pending)
cat = {"Jazzy":"p","Catty":"p"}

#internal list for node state
#three states for ukko nodes : p(positive),u(unknown),s(under searching)
nodelist = []

#timestamp for update state
timestamp=0

def init():
#read node file
	global nodelist
	for line in linecache.getlines("ukkonodes"):
		nodelist.append([line.strip(),"u"])

def assign(name,cnode):
#assign cat to a node, if node is not given then choose an arbitrary node
	#check cat if it is not pending return 1
	if cat[name]!="p":
		return 1
	#check nodes if all nodes is under searching return 2
	counter = 0
	for ukko in nodelist:
		if ukko[1] != "u":
			counter += 1
	if counter == len(nodelist):
		return 2
	
	print(name,cnode)
	
	#get login user name
	username = os.popen("who am i").read().split(' ')[0] 
	node = cnode
	if len(node) < 2 :
		#choose a arbitrary node
		selected = -1
		while selected == -1 or nodelist[selected][0] == "" or nodelist[selected][1] != "u":
			selected = random.randrange(0,len(nodelist))
		#change node state
		nodelist[selected][1]="s"
		#global cat
		cat[name] = "s"
		node = nodelist[selected]
	#assign a cat to an arbitrary node
	os.system("ssh -p 22 "+username+"@"+node[0]+".hpc.cs.helsinki.fi \'python3 chase_cat.py S "+name+"\'")
	return 0
	
def autoAssign(interval):
#auto assign cat to node which is neither under searching nor has been searched
#if one cat is in waiting state, auto assign will stop
	while len(nodelist)>0:
		if cat["Catty"] == "w" or cat["Jazzy"] == "p" and assign("Jazzy",[]) == 2:
			break
		if cat["Jazzy"] == "w" or cat["Catty"] == "p" and assign("Catty",[]) == 2:
			break
		time.sleep(interval)

def operation(msg):
	info = msg[0]
	ukko = 0
	cname = msg[2]
	while ukko<len(nodelist) and nodelist[ukko][0]!=msg[1]:
		ukko += 1
	#global nodelist,cat,timestamp
	if info == "G":
		exit()
	elif info == "NF":
		cat[cname] = "p"
		nodelist.remove(nodelist[ukko])
	elif info == "F":
		cat[cname] = "w"
		if nodelist[ukko][1] != "p":
			nodelist[ukko][1] = "p"
		else:
			#get login user name
			username = os.popen("who am i").read().split(' ')[0]
			#assign Jazzy to attack
			os.system("ssh -p 22 "+username+"@"+nodelist[ukko][0]+".hpc.cs.helsinki.fi \'python3 chase_cat.py A Jazzy\'")
	timestamp = msg[3]
	if cat["Jazzy"] == "w" and cat["Catty"] == "p":
		assign("Catty",nodelist[ukko])
	elif cat["Jazzy"] == "p" and cat["Catty"] == "w":
		assign("Jazzy",nodelist[ukko])

init()
_thread.start_new_thread(autoAssign,(1,))
while True:
	#read cmsg every 2 second
	time.sleep(2)
	cmsg = linecache.getlines("cmsg")
	for line in cmsg:
		msg = line.strip().split(' ')
		if float(msg[len(msg)-1]) > timestamp:
			operation(msg)