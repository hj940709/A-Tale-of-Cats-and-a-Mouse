import socket

s = socket.socket()
host = socket.gethostname()
'''
10001 mouse
10002 Catty
10003 Jazzy
10004 Listy
10005 Cordy
'''

port=10001
print(host,port)
if s.connect_ex((host,port)) == 0: 
	message = "MEOW"
	s.send(bytes(message,'UTF-8'))
	print(s.recv(1024))
