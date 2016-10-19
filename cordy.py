import time,os,linecache,random,_thread


def precaution():
#this function is not required
#terminate itself in an hour automatically
#prevent from leaving it running under any circumstances
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
timestamp=0.00001

def init():
#read node file
	#global nodelist
	for line in linecache.getlines("ukkonodes"):
		if line.strip() != "":
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
	
	#get login user name
	username = os.popen("who am i").read().split(' ')[0]
	#get current path
	path = os.popen("pwd").read().strip()+"/"
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
	os.system("ssh -p 22 "+username+"@"+node[0]+".hpc.cs.helsinki.fi \'python3 "+path+"chase_cat.py S "+name+"\'")
	return 0

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
		if cat["Catty"] != "w" and cat["Jazzy"] !="w" :
			#none of cat find the mouse
			#continue to assign available cat to an arbitrary node
			_thread.start_new_thread(assign,(cname,[],))
		#one cat found mouse
		#locate the target node and send the another cat for double check
		elif cat["Jazzy"] == "w" and cat["Catty"] == "p":
			ukko = 0
			while ukko<len(nodelist) and nodelist[ukko][1] != "p":
				ukko += 1
			_thread.start_new_thread(assign,("Catty",nodelist[ukko],))
		elif cat["Catty"] == "w" and cat["Jazzy"] == "p":
			ukko = 0
			while ukko<len(nodelist) and nodelist[ukko][1] != "p":
				ukko += 1
			_thread.start_new_thread(assign,("Jazzy",nodelist[ukko],))
	elif info == "F":
		cat[cname] = "w"
		if nodelist[ukko][1] != "p":
			#One cat find the mouse for first time
			nodelist[ukko][1] = "p"
		else:
			#Another cat find the mouse again and start an attack			
			#get login user name
			username = os.popen("who am i").read().split(' ')[0]
			#get current path
			path = os.popen("pwd").read().strip()+"/"
			#assign Jazzy to attack
			os.system("ssh -p 22 "+username+"@"+nodelist[ukko][0]+".hpc.cs.helsinki.fi \'python3 "+path+"chase_cat.py A Jazzy\'")
	global timestamp
	timestamp = float(msg[3]) #update time stamp
	
init()
_thread.start_new_thread(assign,("Jazzy",[],))
time.sleep(6)
_thread.start_new_thread(assign,("Catty",[],))
while True:
	#read cmsg every 2 second
	f = open("cmsg","r")
	cmsg = f.read().split("\n")
	f.close()
	for line in cmsg:
		msg = line.strip().split(" ")
		if len(msg)==4 and float(msg[len(msg)-1]) > timestamp:
		#ignore old time stamp and response to larger time stamp
			print(msg)
			operation(msg)
	time.sleep(2)