from Server.Modules import OptType, safeclient
from Server.identify_client import IdentifyClient
import os
import json

OptType = OptType.OptType


class ClientMain:
    def __init__(self, path, _debug_=False):
        self.absolute_setting_path = path + "settings/settings.json"
        if _debug_:
            self.absolute_setting_path = path + "settings/settings_local.json"
        print("[server info] running at", self.absolute_setting_path)
        with open(self.absolute_setting_path, "r") as f:
            settings = json.load(f)

        self.ip = settings["Client"]["Game_Online_IP"]
        self.port = settings["Client"]["Game_Port"]
        self.heart_beat = settings["Client"]["heart_beat"]
        self.reg_ip = settings["Client"]["Reg_IP"]
        self.reg_port = settings["Client"]["Reg_Port"]
        self.aes_key = settings["AES_Key"]

        self.client = safeclient.SocketClient(self.ip, self.port, heart_beat=self.heart_beat)
        self.user = None
        self.roomid = None

    def register(self, username, email):
        identify_client = IdentifyClient(self.reg_ip, self.reg_port, self.ip, self.port, self.aes_key)
        check_code = identify_client.get_check_code(username, email)
        if check_code != '':
            input_check_code = input("Input the check_code in your mailbox: ")
            if check_code.lower() == input_check_code.lower():
                password = input("Input your password: ")
                result = identify_client.send_all_information(username, email, password)
                if result is True:
                    print("Register Successfully!")
                    return True
                else:
                    print("Error! Try again later!")
                    return False
            else:
                print("Error! Try again later!")
                return False

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
            self.user = user
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
    s = ClientMain()
    # s.start()
    # s.register("test", "541665621@qq.com")