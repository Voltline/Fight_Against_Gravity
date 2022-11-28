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

    def send(self, message):
        """
        data:数据 支持str/json格式
        发送数据
        """
        if type(message) == dict:
            message = json.dumps(message)
        lenth = len(message)
        lenth = "%04d" % lenth
        self.__socket.sendall(lenth.encode())
        self.__socket.sendall(message.encode())

    def receive(self):
        """
        返回数据
        """
        message = self.__socket.recv(1024).decode()
        try:
            message = json.loads(message)
        except Exception as err:
            print("[warning info]消息{}不是json格式报文,未解析".format(message), err)
        return message

    def close(self):
        """
        关闭连接
        """
        self.__socket.close()


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    client = SocketClient(ip, port, 5)
    cnt = 0
    while True:
        # a = input()
        a = 0
        if a == "0":
            break
        a = "t" * 1024 * 8
        a = {
            "opt": -1,
            "info": a
        }
        cnt += 1
        print(a)
        client.send(a)
        msg = client.receive()
        print(msg)
        time.sleep(0.01)
    client.close()
