import socket
s = socket.socket()
host  = socket.gethostname()
port = 25555

s.connect((host, port))
s.send("test".encode())
print(s.recv(1024).decode())
s.close()
