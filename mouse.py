import socket,time,linecache,random

s = socket.socket()

def init():
#pick the port
	port = 0
	for line in linecache.getlines("port_number"):
		str_arr = line.strip().split(" ")
		if len(str_arr)>0 and str_arr[1] == "mouse":
			port = int(str_arr[0])
			break
	host = socket.gethostname()
	return (host,port)

(host,port) = init()

s.bind((host, port))       
s.listen(5)
while True:
# 8 seconds for OUCH message
#waiting for searching message or attacking message
	conn, addr = s.accept()
	msg = str(conn.recv(1024)).strip()
	msg = msg[2:len(msg)-1]	
	if msg =="MEOW":
		time.sleep(8)
		conn.send(bytes("OUCH","UTF-8"))
		break
	elif msg!="" :
		conn.send(bytes("mouse confirmed","UTF-8")) #mouse positive confirmation