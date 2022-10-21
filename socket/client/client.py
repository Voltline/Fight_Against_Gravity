import socket


class Socket_client:
    """
    使用TCP连接的socket函数封装
    """
    def __init__(self, ip: str, port: int):
        """
        初始化
        初始化后已经和服务端建立了socket连接
        """
        self.__socket = socket.socket()
        self.__port = port
        self.__host = ip
        try:
            self.__socket.connect((self.__host, self.__port))
        except Exception as err:
            print(err, "无法连接到服务器")

    def send(self, data):
        """
        发送数据
        """
        self.__socket.send(str(data).encode())

    def receive(self):
        """
        返回数据
        """
        return self.__socket.recv(1024).decode()

    def colse(self):
        """
        关闭连接
        """
        self.__s.close()


if __name__ == "__main__":
    ip = "175.24.235.109"
    client = Socket_client(ip, 25555)
    while(True):
        a = input()
        if(a == "0"):
            break;
        client.send(a)
        print(client.receive())
    client.close()
