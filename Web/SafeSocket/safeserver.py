import socket
from threading import Thread
import queue


class SocketSever:
    """
    对服务端的socket进行封装
    """

    def __init__(self, ip: str, port: int):
        """
        初始化socketserver
        ip:绑定服务器ip
        port:进程端口号
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = ip
        self.__port = port
        self.que = queue.Queue()  # 消息队列
        self.conn_poll = []  # 连接池
        self.accept_thread = None  #
        try:
            self.__socket.bind((self.__host, self.__port))
            self.__socket.listen(10)
        except Exception as err:
            print(err, "Fail to build a socked listener")

    def start(self):
        """
        开始接收连接
        """
        self.accept_thread = Thread(target=self.accept_client)
        self.accept_thread.setDaemon(True)
        self.accept_thread.start()

    def accept_client(self):
        """
        接受连接，请新开线程使用 以免阻塞
        """
        while True:
            client, address = self.__socket.accept()
            print("client {0} connected".format(address))
            self.conn_poll.append((client, address))
            thread_message = Thread(target=self.message_handle, args=(client, address))
            thread_message.setDaemon(True)
            thread_message.start()

    def message_handle(self, client: socket.socket, address):
        """
        消息接收函数 传入socket和address，将接收到的消息存入消息队列
        """
        self.conn_poll.append((client, address))
        while True:
            recv = None
            try:
                recv = client.recv(1024)
            except Exception as err:
                print(err, "连接{}意外断开".format(str(address)))
                self.conn_poll.remove((client, address))
                client.close()
                break
            if recv is None or len(recv) == 0:
                print("连接{}已断开".format(address))
                self.conn_poll.remove((client, address))
                client.close()
                break
            else:
                self.que.put((address, recv.decode()))

    def get_message(self):
        """
        返回当前消息队列中的所有消息
        """
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        return res

    def get_connection(self):
        """
        放回连接池
        """
        return self.conn_poll


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    server = SocketSever(ip, port)
    server.start()
    while True:
        messages = server.get_message()
        for item in messages:
            print(item)
