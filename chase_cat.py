import socket,linecache,sys,time

#get name and order from cordy by ssh
command = sys.argv[1]
name = sys.argv[2]

if name != "Catty" and name != "Jazzy":
	print("Error")
	exit()

def getMouseInfo():
#get the port of mouse
	port = 0
	for line in linecache.getlines("port_number"):
		str_arr = line.strip().split(" ")
		if len(str_arr)>0 and str_arr[1] == "mouse":
			port = int(str_arr[0])
			break
	host = socket.gethostname()
	return (host,port)

def report(msg):
#get Listy port and location
#send message to Listy
#add timestamp for each message, timestamp is in a number of second format

	s = socket.socket()
	port = 0
	for line in linecache.getlines("port_number"):
		str_arr = line.strip().split(" ")
		if len(str_arr)>0 and str_arr[1] == "Listy":
			port = int(str_arr[0])
			break
	host = linecache.getline("listy_location",1).strip()
	if s.connect_ex((host,port)) == 0: 
		s.send(bytes(msg,"UTF-8"))
		s.close()

def search():
# 8 seconds for searching
#search for mouse
	time.sleep(12)
	s = socket.socket()
	try:
		flag  = False
		if s.connect_ex(getMouseInfo()) == 0: 
			message = "ping" #send any thing for correct response 
			s.send(bytes(message,'UTF-8'))
			msg = str(s.recv(1024)).strip()
			msg = msg[2:len(msg)-1]	
			if msg == "mouse confirmed":
				flag = True
		if flag:
			report("F "+socket.gethostname()+" "+name)
		else:
			report("NF "+socket.gethostname()+" "+name)
	except:
			report("NF "+socket.gethostname()+" "+name)


def attack():
# 6 seconds for attacking
#attack
#report the result
	time.sleep(6)
	s = socket.socket()
	if s.connect_ex(getMouseInfo()) == 0: 
		message = "MEOW"
		s.send(bytes(message,'UTF-8'))
		msg = str(s.recv(1024)).strip()
		msg = msg[2:len(msg)-1]	
		if msg == "OUCH":
			report("G "+socket.gethostname()+" "+name)


if command == "S":
	search()
elif command == 'A':
	attack()
else:
	print("Error")
	exit()