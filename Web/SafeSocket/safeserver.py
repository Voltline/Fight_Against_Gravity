import socket
from threading import Thread
import queue
import time


class SocketSever:
    """
    对服务端的socket进行封装
    """

    def __init__(self, ip: str, port: int, heart_time: int = -1):
        """
        初始化socketserver
        ip:绑定服务器ip
        port:进程端口号
        """
        self.heart_time = heart_time
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = ip
        self.__port = port
        self.que = queue.Queue()  # 消息队列 [（address， recv）]
        self.conn_poll = {}  # 连接池 以字典方式存储 {address : socket}
        self.accept_thread = None  # 消息接收线程
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
            self.conn_poll.update({address: client})
            if self.heart_time > 0:
                client.settimeout(self.heart_time)
            thread_message = Thread(target=self.message_handle, args=(client, address))
            thread_message.setDaemon(True)
            thread_message.start()

    def message_handle(self, client: socket.socket, address):
        """
        消息接收函数 传入socket和address，将接收到的消息存入消息队列
        """

        def close(close_reason: str, err_reason=None):
            if address in self.conn_poll:
                self.conn_poll.pop(address)
            client.close()
            if err_reason is not None:
                print(err_reason)
            print("连接{0}{1}断开".format(address, close_reason))

        while True:
            if getattr(client, '_closed'):
                print("{}已停止运行".format(address))
                break
            try:
                recv = client.recv(1024)
            except socket.timeout as err:
                close("超时", err_reason=err)
                break
            except Exception as err:
                close("意外", err_reason=err)
                break
            if recv is None or len(recv) == 0:
                close("客户端主动")
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

    def get_connection(self) -> list:
        """
        放回连接池中的address
        """
        return list(self.conn_poll.keys())

    def close(self, address):
        """
        关闭指定连接
        """
        try:
            client = self.conn_poll[address]
            self.send(address, "close")
            client.close()
            self.conn_poll.pop(address)
        except Exception as err:
            print(err, "连接未找到")

    def send(self, address, msg: str):
        try:
            client: socket
            client = self.conn_poll[address]
            client.sendall(msg.encode())
        except Exception as err:
            print(err, "发送失败")


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    server = SocketSever(ip, port, heart_time=5)
    server.start()
    cmd_que = queue.Queue()
    while True:
        messages = server.get_message()
        for item in messages:
            print(item)
        lt = server.get_connection()
        # for item in lt:
        #     server.close(item)
