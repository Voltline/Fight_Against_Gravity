import socket
import queue
from threading import Thread

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
            recv = self.socket.recvfrom(self.msg_len)
            self.que.put((recv[1], recv[0]))

    def get_message(self):
        """
        返回当前消息队列中的所有消息
        格式[(address, msg)]
        """
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        return res


if __name__ == "__main__":
    s = UdpServer("127.0.0.1", 25556)
    res = []
    while True:
        res = s.get_message()
        if len(res):
            print(res)
