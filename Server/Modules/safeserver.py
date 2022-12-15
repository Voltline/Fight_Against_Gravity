import json
import socket
from threading import Thread
import queue
import base64
import re
from Crypto.Cipher import AES
from Server.Modules.Flogger import Flogger


class SocketServer:
    """
    对服务端的socket进行封装
    一些info
    {
        [server info]服务器正常info
        [debug info]debug信息
        [err info]错误信息
        [warning info]警报信息，代表有一些不影响运行的错误发生
    }
    """

    def __init__(self, ip: str, port: int, heart_time: int = -1, debug: bool = False,
                 msg_len: int = 1024, password: str = None,
                 models=Flogger.DLOGG, logpath=None, level=Flogger.L_INFO):
        """
        初始化socketserver
        ip:绑定服务器ip
        port:进程端口号
        heart_time: 心跳检测，即超时断开连接时间。默认heart_time = -1表示不开启
        debug: debug选项
        warning: warning选项
        msg_len: 报文长度 默认1024 实测在每秒60帧，4Mbps情况下，报文长度最高3000，否则丢包
        password：AES加密秘钥，默认None
        models，logpath，level，folde_name都是日志选项
        收发流程：
        发：msg->encode(msg)->encrypt(encode(msg))
        收：encrypt(encode(msg))->encode(msg)->msg
        """
        self.logger = Flogger(models, logpath, level, folder_name="safeserver")
        self.heart_time = heart_time
        """心跳检测"""
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """服务端socket"""
        self.__host = ip
        """服务端ip，云端请保留云服务器ip"""
        self.__port = port
        """服务器端口"""
        self.que = queue.Queue()
        """消息队列 [（address， recv）]"""
        self.conn_poll = {}  #
        """socket连接池 以字典方式存储 {address : socket}"""
        self.accept_thread = None
        """消息接收线程"""
        self.debug = debug
        """debug选项"""
        self.msg_len = msg_len
        """消息长度（建议短"""
        self.password = None
        """加密选项,如需加密请直接输入秘钥"""
        if password:
            self.password = password.encode()
        if (password is not None) and (len(password) != 16):
            self.logger.error("秘钥长度非16:" + password)
            exit(-1)

        try:
            self.__socket.bind((self.__host, self.__port))
            self.__socket.listen(5)
        except Exception as err:
            self.logger.error("Fail to build a socked listener" + str(err))
            exit(-1)
        # 以下是初始化logging
        self.logger.info("heart time：" + str(self.heart_time))
        self.logger.info("ip:" + str(self.__host) + " port:" + str(self.__port))
        self.logger.info("message length:" + str(self.msg_len))
        self.logger.info("debug:" + str(self.debug))
        if password:
            self.logger.info("Encrypt message on")
        else:
            self.logger.info("Encrypt message off")

        def start():
            """
            开始接收连接
            """
            self.logger.info("server started")
            self.accept_thread = Thread(target=self.accept_client)
            self.accept_thread.setDaemon(True)
            self.accept_thread.setName("accept_thread")
            self.accept_thread.start()

        start()

    def accept_client(self):
        """
        接受连接，请新开线程使用 以免阻塞
        """
        while True:
            client, address = self.__socket.accept()
            self.logger.info("client {0} connected".format(address))
            client.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, True)
            self.conn_poll.update({address: client})
            if self.heart_time > 0:
                client.settimeout(self.heart_time)
            thread_message = Thread(target=self.message_handle, args=(client, address))
            thread_message.setDaemon(True)
            thread_message.setName("message_" + str(address))
            thread_message.start()

    def encrypt(self, message: str) -> bytes:
        message = message.encode()
        lenth = len(message) % 16
        message = message + b'$' * (16 - lenth)
        e = AES.new(self.password, AES.MODE_ECB).encrypt(message)
        return e

    def decrypt(self, message: bytes) -> str:
        d = AES.new(self.password, AES.MODE_ECB).decrypt(message)
        d = d.strip(b'$')
        return d.decode()

    @staticmethod
    def decode(message: str):
        """
        mathch all messsage in the msg
        return list
        """
        res = []
        msg_list = re.findall("-S-([^-]*?)-E-", message)
        for item in msg_list:
            message = item[:]
            message = base64.b64decode(message)
            res.append(message.decode())
        return res

    @staticmethod
    def encode(message: str):
        message = base64.b64encode(message.encode())
        message = message.decode()
        message = "-S-" + message + "-E-"
        return message

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
            self.logger.info("连接{0}{1}断开".format(address, close_reason))

        while True:
            if getattr(client, '_closed'):
                self.logger.info("[server info] {}已停止运行".format(address))
                break
            try:
                recv = client.recv(self.msg_len)
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
                if self.password:
                    try:
                        recv = self.decrypt(recv)
                    except ValueError as err:
                        self.logger.error("消息解密失败，请检查{}数据是否加密或秘钥是否一致".format(address) + str(err))
                        continue
                else:
                    recv = recv.decode()
                # 粘连包切片
                tmpmsg = self.decode(recv)
                for message in tmpmsg:
                    if len(message) <= 50:
                        self.logger.debug("{recv %d lenth msg from%s}:%s" % (len(message), address, message))
                    else:
                        self.logger.debug("{recv %d lenth msg from%s}" % (len(message), address))
                    try:
                        message = json.loads(message)
                        if message["opt"] != 0:
                            # 0是heart beat 不存入消息队列
                            self.que.put((address, message))
                    except Exception as err:
                        self.logger.warning("消息{}不是json格式报文,未解析".format(message) + str(err))
                        if self.debug:
                            exit(-1)
                        self.que.put((address, message))

    def get_message(self):
        """
        返回当前消息队列中的所有消息
        格式[(address, msg)]
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
            self.logger.error("[in close]" + str(err) + "连接未找到")

    def send(self, address, message):
        """
        msg:支持dict（json）/str格式
        """
        try:
            client: socket
            client = self.conn_poll[address]
            if type(message) == dict:
                message = json.dumps(message)
            if len(message) <= 50:
                self.logger.debug("{send %d lenth msg to %s}:%s" % (len(message), address, message))
            else:
                self.logger.debug("{send %d lenth msg to %s}" % (len(message), address))
            message = self.encode(message)
            if self.password:
                message = self.encrypt(message)
            else:
                message = message.encode()
            client.sendall(message)
        except Exception as err:
            self.logger.error("[in send]" + str(err) + "发送失败")


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    online = False
    if online:
        ip = "192.168.0.57"
    server = SocketServer(ip, port, heart_time=10, debug=False, msg_len=8192,
                          password="0123456789abcdef")
    while True:
        messages = server.get_message()
        for item in messages:
            print(item)
            address = item[0]
            msg = {
                "opt": -1,
                "info": item
            }
            # print(msg)
            server.send(address, msg)
        lt = server.get_connection()
