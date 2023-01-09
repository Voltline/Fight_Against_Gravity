import socket
import queue


class UdpClient:
    def __init__(self, ip, port: int, msg_len: int = 1024):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((ip, port))
        self.msg_len = msg_len
        self.que = queue.Queue

    def message_handler(self):
        while True:
            recv = self.socket.recvfrom(self.msg_len)
            self.que.put((recv[1], recv[1]))

    def get_message(self):
        """
        返回当前消息队列中的所有消息
        格式[(address, msg)]
        """
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        return res

    def send(self, address, message: str):
        """
        发送数据
        """
        self.socket.sendto(message.encode(), address)


if __name__ == "__main__":
    c = UdpClient("127.0.0.1", 25557)
    for i in range(10):
        c.send(("127.0.0.1", 25556), "test")
