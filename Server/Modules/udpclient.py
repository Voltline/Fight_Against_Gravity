import socket
import queue
from threading import Thread

import msgpack

from Server.Modules.message_dealer import MessageDealer


class UdpClient:
    def __init__(self, ip, server_port: int, msg_len: int = 1024):
        self.server_address = (ip, server_port)
        self.socket = self.create_client()
        if self.socket is None:
            raise Exception("fail to build a udp client")
        try:
            # 连接目标以便操作系统自动选择合适的本地地址（避免绑定到错误网卡无法回环）
            self.socket.connect(self.server_address)
        except Exception:
            pass
        self.msg_len = msg_len
        self.que = queue.Queue()
        self.uque = queue.Queue()
        thread_message = Thread(target=self.message_handler)
        thread_message.daemon = True
        thread_message.start()
        thread_dealer = Thread(target=self.message_dealer)
        thread_dealer.daemon = True
        thread_dealer.start()

    def create_client(self, port=0):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 绑定 0.0.0.0:0，让系统选择与目标匹配的本地地址
            client.bind(("", port))
            return client
        except Exception as err:
            print("fail to build udp client", err)
            return None

    def message_dealer(self):
        while True:
            recv = self.uque.get()
            try:
                decoded = MessageDealer.decode(recv[0])
                for message in decoded:
                    if isinstance(message, (dict, list)):
                        self.que.put(message)
                    elif isinstance(message, (bytes, bytearray)):
                        self.que.put(msgpack.unpackb(message, raw=False))
                    else:
                        self.que.put(message)
            except Exception as err:
                # 保留异常信息，避免线程悄悄退出
                print("udp client decode error", err, recv)

    def message_handler(self):
        while True:
            try:
                recv = self.socket.recvfrom(self.msg_len)
                self.uque.put(recv)
                # print("recv", recv)
            except Exception as err:
                print("in message_handler", err)

    def send(self, message):
        """
        发送数据
        """
        # print("try to send", message, self.server_address)
        try:
            encoded = MessageDealer.encode(message)
            self.socket.send(encoded)
            # print("send", message)
        except Exception as err:
            print(err)

    def receive(self):
        return self.que.get()

    def get_message(self):
        """
        获取消息（非阻塞）
        若无消息返回None
        """
        if self.que.empty():
            return None
        res = self.que.get()
        return res

    def get_message_list(self):
        """
        获取消息队列
        """
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        return res


if __name__ == "__main__":
    c = UdpClient("192.168.3.23", 25556)
    for i in range(100):
        c.send({0: "1", "id": i})
    while True:
        print(c.receive())
