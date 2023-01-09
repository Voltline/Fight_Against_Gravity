import time

from Server.Modules import safeserver
from Server.Modules import  safeclient
s = safeserver.SocketServer("127.0.0.1", 25555,password="1234567887654321")
c = safeclient.SocketClient("127.0.0.1", 25555,password="1234567887654321")
c.send("test")
msg = []
while True:
    msg = s.get_message()
    if len(msg):
        break
Adr, Msg = msg[0]
print(msg)
s.send(Adr, "test2")
print(c.receive())