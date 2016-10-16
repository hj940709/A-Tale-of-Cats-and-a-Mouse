import socket,linecache,os,time,_thread

def precaution():
	time.sleep(3600)
	os._exit(0)
_thread.start_new_thread(precaution,())

def init():
#create of empty cmsg file
#set hostname and port pair
	f = open("cmsg","w")
	f.truncate()
	f.close()
	port = 0
	for line in linecache.getlines("port_number"):
		str_arr = line.strip().split(" ")
		if len(str_arr)>0 and str_arr[1] == "Listy":
			port = int(str_arr[0])
			break
	host = socket.gethostname()
	return (host,port)

s = socket.socket()
(host,port) = init()
s.bind((host, port))
s.listen(5)
while True:
#message format: (msg),(hostname),(catname),(timestamp)
	conn, addr = s.accept()
	msg = str(conn.recv(1024)).strip()
	msg = msg[2:len(msg)-1]
	if msg=="" :
		continue
	else:
		f = open("cmsg","a")
		f.write(msg+" "+str(time.time())+"\n")
		f.close()
		if msg.split(' ')[0] == "G":
			exit(0)
