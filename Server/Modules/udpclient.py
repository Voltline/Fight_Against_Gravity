import socket
import queue
import json
from message_dealer import MessageDealer
from threading import Thread


class UdpClient:
    def __init__(self, ip, server_port: int, msg_len: int = 1024):
        self.socket = self.create_client()
        if self.socket is None:
            raise Exception("fail to build a udp client")
        self.msg_len = msg_len
        self.que = queue.Queue()
        self.server_address = (ip, server_port)
        thread_message = Thread(target=self.message_handler)
        thread_message.setDaemon(True)
        thread_message.start()

    def create_client(self, port=0):
        if port > 65535:
            return None
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.bind((socket.gethostbyname(socket.gethostname()), port))
            return client
        except:
            return self.create_client(port + 1)

    def message_handler(self):
        while True:
            try:
                recv = self.socket.recvfrom(self.msg_len)
                message = recv[0].decode()
                try:
                    message = json.loads(message)
                except:
                    pass
                self.que.put((recv[1], message))
            except Exception as err:
                print("in message_handler", err)

    def send(self, message):
        """
        发送数据
        """
        try:
            if type(message) == dict:
                message = json.dumps(message)
            if type(message) != str:
                return False
            message = message.encode()
            self.socket.sendto(message, self.server_address)
            print(self.server_address)
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
    c = UdpClient("192.168.3.13", 25556)
    for i in range(100):
        c.send({0: "1", "id": i})
    while True:
        print(c.receive())