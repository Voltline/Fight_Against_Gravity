import socket
s = socket.socket()
host = socket.gethostname()
port  = 25555
s.bind((host, port))

s.listen(5)
while True:
   c,addr = s.accept()
   print("链接地址",addr)
   print(c.recv(1024).decode())
   msg = ("test").encode()
   c.send(msg)
   c.close()