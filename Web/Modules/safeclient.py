import json
import socket
import time
from threading import Thread
import queue
import base64
import re


class SocketClient:
    """
    使用TCP连接的socket函数封装
    """

    def __init__(self, ip: str, port: int, heart_beat: int = -1, debug=False, warning=False):
        """
        ip:服务端ip地址
        port:服务端端口
        heart_beat:心跳检测 默认0
        初始化
        初始化后已经和服务端建立了socket连接
        """
        self.__socket = socket.socket()
        """客户端"""
        self.__port = port
        """服务器端口"""
        self.__host = ip
        """服务器ip"""
        self.debug = debug
        """debug选项"""
        self.warnig = warning
        """是否开启warning"""
        self.heart_beat = heart_beat
        """心跳检测"""
        self.que = queue.Queue()
        """消息队列"""
        try:
            self.__socket.connect((self.__host, self.__port))
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, True)
        except Exception as err:
            print(err, "无法连接到服务器")
        self.message_thread = Thread(target=self.message_handler)
        self.message_thread.setDaemon(True)
        self.message_thread.start()
        if heart_beat > 0:
            self.heart_thread = Thread(target=self.beating)
            self.heart_thread.setDaemon(True)
            self.heart_thread.start()

    @staticmethod
    def decode(msg: str):
        """
        mathch all messsage in the msg
        return list
        """
        res = []
        msg_list = re.findall("-S-([^-]*?)-E-", msg)
        # print(msg_list)
        for item in msg_list:
            msg = item[:]
            # print(msg)
            msg = base64.b64decode(msg)
            # print(msg.decode())
            res.append(msg.decode())
        return res

    @staticmethod
    def encode(msg: str):
        msg = base64.b64encode(msg.encode())
        msg = msg.decode()
        # print(msg)
        msg = "-S-" + msg + "-E-"
        # print(msg)
        return msg

    def message_handler(self):
        try:
            while True:
                lenth = 1024
                recv = self.__socket.recv(lenth).decode()
                # 粘连包切片
                tmpmsg = self.decode(recv)
                for item in tmpmsg:
                    msg = None
                    try:
                        msg = json.loads(item)
                        if msg["opt"] != 0:
                            self.que.put(msg)
                    except Exception as err:
                        if self.warnig:
                            print("[warning info]消息{}不是json格式报文,未解析".format(msg), err)
                        self.que.put(item)
                    if self.debug:
                        print("[debug]", msg)
        except:
            print("[client info]client closed")

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
        # base64
        message = self.encode(message)
        try:
            self.__socket.sendall(message.encode())
        except Exception as err:
            print("[client info]client closed")

    def receive(self):
        """
        返回数据
        """
        if self.que.empty():
            return None
        res = self.que.get()
        return res

    def close(self):
        """
        关闭连接
        """
        self.__socket.close()


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    client = SocketClient(ip, port, 5, True)
    cnt = 0
    while True:
        a = input()
        if a == "0":
            break
        msg = {
            "opt": -1,
            "info": a
        }
        print(msg)
        for i in range(3):
            client.send(msg)
        for j in range(5):
            msg = client.receive()
            print(msg)
        # time.sleep(0.01)
    client.close()
