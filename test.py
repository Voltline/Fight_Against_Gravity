import time

from Server.Modules import safeserver
from Server.Modules import  safeclient
# s = safeserver.SocketServer("192.168.3.13", 25555)
c = safeclient.SocketClient("192.168.3.13", 25555)
c.send("test")
# msg = []
# while True:
#     msg = s.get_message()
#     if len(msg):
#         break
# Adr, Msg = msg[0]
# print(msg)
# s.send(Adr, "test2")
# print(c.receive())

"""
    "Game_Local_IP": "192.168.3.13",
    "Game_Online_IP": "123.129.198.66",
    "Game_Local_Port": 25555,
    "Game_Online_Port": 15662,
"""