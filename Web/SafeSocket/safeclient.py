import json
import socket
import time
from threading import Thread


class SocketClient:
    """
    使用TCP连接的socket函数封装
    """

    def __init__(self, ip: str, port: int, heart_beat: int = -1):
        """
        ip:服务端ip地址
        port:服务端端口
        heart_beat:心跳检测 默认0
        初始化
        初始化后已经和服务端建立了socket连接
        """
        self.__socket = socket.socket()
        self.__port = port
        self.__host = ip
        self.heart_beat = heart_beat
        try:
            self.__socket.connect((self.__host, self.__port))
        except Exception as err:
            print(err, "无法连接到服务器")
        if heart_beat > 0:
            self.heart_thread = Thread(target=self.beating)
            self.heart_thread.setDaemon(True)
            self.heart_thread.start()

    def beating(self):
        while True:
            msg = {"opt": 0, "heartbeat": self.heart_beat}
            self.send(msg)
            time.sleep(self.heart_beat - 0.4)

    def send(self, msg):
        """
        data:数据 支持str/json格式
        发送数据
        """
        if type(msg) == dict:
            msg = json.dumps(msg)
        self.__socket.sendall(msg.encode())

    def receive(self):
        """
        返回数据
        """
        return self.__socket.recv(1024).decode()

    def close(self):
        """
        关闭连接
        """
        self.__socket.close()


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    client = SocketClient(ip, port, 5)
    print(1)
    while True:
        a = input()
        if a == "0":
            break
        a = {
            "opt": -1,
            "info": a
        }
        print(a)
        client.send(a)
    client.close()
