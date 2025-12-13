import socket
import queue
from threading import Thread

import msgpack

from Server.Modules.message_dealer import MessageDealer


class UdpServer:
    def __init__(self, ip, port: int, msg_len: int = 1024):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((ip, port))
        self.msg_len = msg_len
        self.que = queue.Queue()
        thread_message = Thread(target=self.message_handler)
        thread_message.setDaemon(True)
        thread_message.start()

    def message_handler(self):
        while True:
            try:
                recv = self.socket.recvfrom(self.msg_len)
                decoded = MessageDealer.decode(recv[0])
                for message in decoded:
                    if isinstance(message, (dict, list)):
                        self.que.put((recv[1], message))
                    elif isinstance(message, (bytes, bytearray)):
                        self.que.put((recv[1], msgpack.unpackb(message, raw=False)))
                    else:
                        self.que.put((recv[1], message))
            except OSError as oserr:
                print("上一个消息发送失败 " + str(oserr))
            except Exception as err:
                print("in message_handler" + str(err))

    def get_message(self):
        """
        返回当前消息队列中的所有消息
        格式[(address, msg)]
        """
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        return res

    def send(self, address, message):
        """
        发送数据
        """
        try:
            encoded = MessageDealer.encode(message)
            self.socket.sendto(encoded, address)
        except Exception as err:
            print("fail to send message" + str(err))


if __name__ == "__main__":
    s = UdpServer("192.168.3.23", 25556)
    res = []
    while True:
        res = s.get_message()
        for item in res:
            addr, msg = item
            # print(item)
            s.send(addr, {"id": msg["id"]})
