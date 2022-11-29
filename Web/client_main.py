import Web.Modules.safeclient as safeclient
import Web.Modules.OptType as OptType
import os
import json

OptType = OptType.OptType
_debug_ = False  # 调试选项 运行环境请勿开启


class ClientMain:
    def __init__(self):
        # TODO:heartbeat 服务端从json读取
        current_path = os.getcwd()
        fag_directory = os.path.dirname(current_path)
        os.chdir(fag_directory)
        with open("Web/Modules/settings.json", "r") as f:
            settings = json.load(f)
        ip = settings["Client"]["Game_IP"]
        port = settings["Client"]["Game_Port"]
        if _debug_:
            ip = "localhost"
            port = 25555

        self.client = safeclient.SocketClient(ip, port, heart_beat=5)
        self.user = None
        self.roomid = None

    def login(self, user: str, password: str):
        """
        用户登录
        user：用户名
        password：用户密码

        """
        msg = {
            "opt": OptType.login,
            "user": user,
            "password": password
        }
        self.client.send(msg)
        recvMsg = self.client.receive()
        if recvMsg["status"] == "ACK":
            print("ACK")
            return True
        else:
            print("NAK")
            print("登陆失败 请重新启动游戏")
            return False

    def creatroom(self):
        msg = {
            "opt": OptType.creatRoom,
            "user": self.user
        }
        self.client.send(msg)
        recv = self.client.receive()
        if recv["status"] == "NAK":
            return False
        elif recv["status"] == "ACK":
            self.roomid = recv["roomid"]
            return self.roomid
        else:
            pass

    def deleteroom(self):
        msg = {
            "opt": OptType.deleteRoom,
            "user": self.user,
            "roomid": self.roomid
        }
        self.client.send(msg)
        recv = self.client.receive()
        if recv["status"] == "NAK":
            return False
        elif recv["status"] == "ACK":
            return True
        else:
            pass

    def start(self):
        self.user = input("input the user name")
        password = input("input the pass word")
        if not self.login(self.user, password):
            self.client.close()
            exit(-1)
        while True:
            opt = int(input())
            if opt == 0:
                break
            if opt == 1:
                print("get1")
                print(self.creatroom())
            if opt == 2:
                print("get2")
                print(self.deleteroom())
        self.client.close()
        print("[client info] exit")
        exit(0)


if __name__ == "__main__":
    _debug_ = True
    s = ClientMain()
    s.start()
