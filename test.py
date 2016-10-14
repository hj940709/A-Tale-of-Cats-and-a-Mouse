import socket

s = socket.socket()
host = socket.gethostname()
port=10002
if s.connect_ex((host,port)) == 0: 
	message = ""
	s.send(bytes(message,'UTF-8'))
	print()
