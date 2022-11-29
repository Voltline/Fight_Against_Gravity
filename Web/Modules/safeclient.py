﻿import json
import socket
import time
from threading import Thread
import queue


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
        """客户端"""
        self.__port = port
        """服务器端口"""
        self.__host = ip
        """服务器ip"""
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

    def message_handler(self):
        while True:
            lenth = 1024
            # lenth = self.__socket.recv(4)
            # lenth = int(lenth.decode())
            recv = self.__socket.recv(lenth).decode()
            # 粘连包切片
            tmpmsg = []
            cutpos = [0]
            for i in range(1, len(recv)):
                if recv[i - 1] == '}' and recv[i] == '{':
                    cutpos.append(i)
            cutpos.append(len(recv))
            for i in range(1, len(cutpos)):
                tmpmsg.append(recv[cutpos[i - 1]:cutpos[i]])
            for item in tmpmsg:
                try:
                    msg = json.loads(item)
                    if msg["opt"] != 0:
                        self.que.put(msg)
                except Exception as err:
                    print("[warning info]消息{}不是json格式报文,未解析".format(msg), err)
                    self.que.put(msg)
                # print("[debug]", msg)

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
        # lenth = len(message)
        # lenth = "%04d" % lenth
        # self.__socket.sendall(lenth.encode())
        self.__socket.sendall(message.encode())

    def receive(self):
        """
        返回数据
        """
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
    client = SocketClient(ip, port, 5)
    cnt = 0
    a = input()
    while True:
        if a == "0":
            break
        msg = {
            "opt": -1,
            "info": a
        }
        print(msg)
        client.send(msg)
        for i in range(5):
            msg = client.receive()
            print(msg)
        time.sleep(0.01)
    client.close()
