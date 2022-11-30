﻿import json
import socket
import time
from threading import Thread
import queue
import base64
import re
from Crypto.Cipher import AES


class SocketClient:
    """
    使用TCP连接的socket函数封装
    """

    def __init__(self, ip: str, port: int, heart_beat: int = -1, debug=False, warning=False, msg_len: int = 1024,
                 password: str = None):
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
        self.msg_len = msg_len
        """消息长"""
        self.password = password.encode()
        """加密选项,如需加密请直接输入秘钥"""
        if (password is not None) and (len(password) != 16):
            raise ValueError("秘钥长度非16")
        try:
            self.__socket.connect((self.__host, self.__port))
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, True)
        except Exception as err:
            print(err, "无法连接到服务器")
            return 0
        self.message_thread = Thread(target=self.message_handler)
        self.message_thread.setDaemon(True)
        self.message_thread.setName("message_thread")
        self.message_thread.start()
        if heart_beat > 0:
            self.heart_thread = Thread(target=self.beating)
            self.heart_thread.setDaemon(True)
            self.heart_thread.setName("heart_beat_thread")
            self.heart_thread.start()

    def encrypt(self, message: str) -> bytes:
        message = message.encode()
        lenth = len(message) % 16
        message = message + b'$' * (16 - lenth)
        e = AES.new(self.password, AES.MODE_ECB).encrypt(message)
        return e

    def decrypt(self, msg: bytes) -> str:
        d = AES.new(self.password, AES.MODE_ECB).decrypt(msg)
        d = d.strip(b'$')
        return d.decode()

    @staticmethod
    def decode(msg: str):
        """
        mathch all messsage in the msg
        return list
        """
        res = []
        msg_list = re.findall("-S-([^-]*?)-E-", msg)
        for item in msg_list:
            msg = item[:]
            msg = base64.b64decode(msg)
            res.append(msg.decode())
        return res

    @staticmethod
    def encode(message: str):
        message = base64.b64encode(message.encode())
        message = message.decode()
        message = "-S-" + message + "-E-"
        return message

    def message_handler(self):
        try:
            while True:
                recv_segment = self.__socket.recv(self.msg_len)
                if self.password:
                    try:
                        recv_segment = self.decrypt(recv_segment)
                    except UnicodeError:
                        print("[client info]消息解密失败,请检查与服务端的秘钥是否一致")
                        continue
                else:
                    recv_segment = recv_segment.decode()
                # 粘连包切片
                tmpmsg = self.decode(recv_segment)
                for item in tmpmsg:
                    message = None
                    try:
                        message = json.loads(item)
                        if message["opt"] != 0:
                            self.que.put(message)
                    except Exception as err:
                        if self.warnig:
                            print("[warning info]消息{}不是json格式报文,未解析".format(message), err)
                        self.que.put(item)
                    if self.debug:
                        if len(item) <= 150:
                            print("[debug info] receive", item, len(item))
                        else:
                            print("[debug info] receive msg, lenth", len(item))
        except Exception as err:
            print("[client info]client closed", err)

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
        message = self.encode(message)  # base64
        if self.debug:
            print("[debug info]lenth of message after encode is", len(message))
        if self.password:
            message = self.encrypt(message)
        else:
            message = message.encode()
        self.__socket.sendall(message)

    def receive(self):
        """
        返回数据(阻塞方式）
        """
        res = self.que.get()
        return res

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

    def close(self):
        """
        关闭连接
        """
        self.__socket.close()


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    online = False
    if online:
        ip = "124.70.162.60"
    client = SocketClient(ip, port, 1, debug=False, msg_len=8192, password="1234567887654321")
    cnt = 0
    while True:
        a = input()
        # a = "a" * a
        if a == "0":
            break
        msg = {
            "opt": -1,
            "info": a
        }
        # print(msg)
        client.send(msg)
        recv = client.get_message()
        while recv is None:
            recv = client.get_message()

        print(recv)
        time.sleep(0.02)
    client.close()
