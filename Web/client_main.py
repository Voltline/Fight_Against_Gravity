import Web.Modules.safeclient as safeclient
import Web.Modules.OptType as OptType
import os
import json

OptType = OptType.OptType
_debug_ = False  # 调试选项 运行环境请勿开启


class ClientMain:
    def __init__(self):
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
            input("回车以继续")
            return False

    def creat_room(self):
        msg = {
            "opt": OptType.creatRoom,
            "user": self.user
        }
        self.client.send(msg)

    def start(self):
        self.user = input("input the user name")
        password = input("input the pass word")
        if not self.login(self.user, password):
            self.client.close()
            exit(0)
        while True:
            pass


if __name__ == "__main__":
    _debug_ = True
    s = ClientMain()
    s.start()
