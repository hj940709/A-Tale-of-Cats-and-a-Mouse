import socket,time,linecache,random

s = socket.socket()

def init():
#randomly select node
#pick the port
	port = 0
	for line in linecache.getlines('port_number'):
		str_arr = line.strip().split(' ')
		if len(str_arr)>0 and str_arr[1] == 'mouse':
			port = int(str_arr[0])
			break
	ukkos = linecache.getlines('ukkonodes')
	host = socket.gethostname()
	return (host,port)

(host,port) = init()

s.bind((host, port))       
s.listen(5)
while True:
	conn, addr = s.accept()
	msg = str(conn.recv(1024)).strip()
	msg = string[2:len(string)-1]
	if msg!='' :
		continue
	
	if msg =='MEOW':
		time.sleep(8)
		conn.send(bytes('OUCH','UTF-8'))
		break
