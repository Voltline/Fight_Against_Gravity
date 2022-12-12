from Server import Modules as safeclient, Modules as OptType
import os
import json

OptType = Server.Modules.OptType
_debug_ = False  # 调试选项 运行环境请勿开启


class ClientMain:
    def __init__(self):
        # TODO:heartbeat 服务端从json读取
        current_path = os.getcwd()
        fag_directory = os.path.dirname(current_path)
        os.chdir(fag_directory)
        with open("Server/Modules/settings.json", "r") as f:
            settings = json.load(f)
        ip = settings["Client"]["Game_Online_IP"]
        port = settings["Client"]["Game_Port"]
        heart_beat = settings["Client"]["heart_beat"]
        if _debug_:
            ip = "localhost"
            port = 25555

        self.client = safeclient.SocketClient(ip, port, heart_beat=heart_beat)
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

    def creatroom(self, roomname, roommap):
        msg = {
            "opt": OptType.creatRoom,
            "user": self.user,
            "roomname": roomname,
            "roommap": roommap
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
            self.roomid = None
            return True
        else:
            pass

    def joinroom(self, roomid):
        if self.roomid:
            # 已经在房间了
            return False
        msg = {
            "opt": OptType.joinRoom,
            "user": self.user,
            "roomid": roomid
        }
        self.client.send(msg)
        recv = self.client.receive()
        if recv["status"] == "ACK":
            self.roomid = recv["roomid"]
            return True
        elif recv["status"] == "NAK":
            return False

    def leftroom(self):
        if self.roomid is None:
            return False
        msg = {
            "opt": OptType.leftRoom,
            "user": self.user,
            "roomid": self.roomid
        }
        self.client.send(msg)
        recv = self.client.receive()
        if recv["status"] == "ACK":
            self.roomid = None
            return True
        elif recv["status"] == "NAK":
            return False

    def startgame(self):
        if self.roomid is None:
            return False
        msg = {
            "opt": OptType.startgame,
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

    def getroom(self):
        if self.roomid is None:
            return False
        msg = {
            "opt": OptType.getRoom,
            "roomid": self.roomid
        }
        self.client.send(msg)
        recv = self.client.receive()
        if recv["status"] == "NAK":
            return False
        res = recv["room"]
        return res

    def getroomlist(self):
        msg = {
            "opt": OptType.getRoomlist,
        }
        self.client.send(msg)
        recv = self.client.receive()
        print(recv)
        return recv["roomlist"]

    def ready(self):
        if self.roomid is None:
            return False
        msg = {
            "opt": OptType.userready,
            "user": self.user,
            "roomid": self.roomid,
            "ready": "YES",
        }
        self.client.send(msg)
        recv = self.client.receive()
        return recv["status"] == "ACK"

    def dready(self):
        if self.roomid is None:
            return False
        msg = {
            "opt": OptType.userready,
            "user": self.user,
            "roomid": self.roomid,
            "ready": "NO",
        }
        self.client.send(msg)
        recv = self.client.receive()
        return recv["status"] == "ACK"

    def start(self):
        # self.user = input("input the user name")
        self.user = "test1"
        # password = input("input the pass word")
        password = "123456"
        if not self.login(self.user, password):
            self.client.close()
            exit(-1)
        while True:
            ints = input()
            opt = -1
            if ints.isdigit():
                opt = int(ints)
            else:
                pass
            if opt == 0:
                break
            if opt == 1:
                print("creat room")
                roomname = input("input room name")
                roommap = input("roommap")
                print(self.creatroom(roomname, roommap))
            if opt == 2:
                print("delete room")
                print(self.deleteroom())
            if opt == 3:
                print("start game")
                print(self.startgame())
            if opt == 4:
                print("join room")
                roomname = input("roomid：")
                print(self.joinroom(roomname))
            if opt == 5:
                print("get room", self.roomid)
                print(self.getroom())
            if opt == 6:
                print("get roomlist")
                print(self.getroomlist())
            if opt == 7:
                print("left room")
                print(self.leftroom())
            if opt == 8:
                print("ready")
                print(self.ready())
            if opt == 9:
                print("deready")
                print(self.dready())
            else:
                continue
        self.client.close()
        print("[client info] exit")
        exit(0)


if __name__ == "__main__":
    # _debug_ = True
    s = ClientMain()
    s.start()
