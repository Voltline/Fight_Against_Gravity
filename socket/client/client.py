from ctypes import WinError
from signal import raise_signal
import socket


class Socket_client:
    def __init__(self, ip: str, port: int):
        """
        初始化
        """
        self.__socket = socket.socket()
        self.__port = port
        self.__host = ip
        try:
            self.__socket.connect((self.__host, self.__port))

        except Exception as err:
            print(err, "无法连接到服务器")

    def send(self, data):
        self.__socket.send(data.encode())

    def receive(self):
        print(self.__socket.recv(1024).decode())

    def colse(self):
        self.__s.close()


if __name__ == "__main__":
    client = Socket_client("localhost", 25555)
