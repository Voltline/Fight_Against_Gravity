from Server.Modules import OptType, safeclient
from Server.Modules.Flogger import Flogger
from Server.identify_client import IdentifyClient
import json

OptType = OptType.OptType


class ClientMain:
    def __init__(self, path, _debug_=False):
        self.logger = Flogger(models=Flogger.FILE_AND_CONSOLE, level=Flogger.L_INFO,
                              folder_name="client_main", logpath=path)
        self.absolute_setting_path = path + "settings/settings.json"
        client_models = Flogger.FILE
        client_level = Flogger.L_INFO
        if _debug_:
            self.absolute_setting_path = path + "settings/settings_local.json"
            client_models = Flogger.FILE_AND_CONSOLE
            client_level = Flogger.L_DEBUG
        with open(self.absolute_setting_path, "r") as f:
            settings = json.load(f)
        self.ip = settings["Client"]["Game_Online_IP"]
        self.port = settings["Client"]["Game_Port"]
        self.heart_beat = settings["Client"]["heart_beat"]
        self.reg_ip = settings["Client"]["Reg_IP"]
        self.reg_port = settings["Client"]["Reg_Port"]
        self.aes_key = settings["AES_Key"]
        try:
            self.client = safeclient.SocketClient(self.ip, self.port, heart_beat=self.heart_beat, models=client_models,
                                                  logpath=path, level=client_level)
        except Exception as err:
            self.logger.error("客户端启动失败" + str(err))
            # exit(-1)
            raise Exception("无法连接到服务器")
        self.user = None
        self.roomid = None

    def register_get_checkcode(self, username, email):
        identify_client = IdentifyClient(self.reg_ip, self.reg_port, self.ip, self.port, self.aes_key)
        # identify_client = safeclient.SocketClient(self.reg_ip, self.reg_port, password=se)
        check_code = identify_client.get_check_code(username, email)
        self.logger.info("[register]{}{}Register get check_code{}".format(username, email, check_code))
        del identify_client
        return check_code

    def register_push_password(self, username, email, check_code, input_check_code, password):
        identify_client = IdentifyClient(self.reg_ip, self.reg_port, self.ip, self.port, self.aes_key)
        if check_code != '':
            if check_code.lower() == input_check_code.lower():
                result = identify_client.send_all_information(username, email, password)
                del identify_client
                if result is True:
                    self.logger.info("[register]{}{}Register Successfully!".format(username, email))
                    return True
                else:
                    self.logger.info("[register]{}{}Register Failed!".format(username, email))
                    return False
            else:
                self.logger.info("[register]{}{}Register Failed!".format(username, email))
                return False
        else:
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
            self.logger.info("[login]" + str(recvMsg))
            return True
        else:
            self.logger.info("[login]" + str(recvMsg))
            return False

    def changemap(self, roommap):
        msg = {
            "opt": OptType.changemap,
            "user": self.user,
            "roommap": roommap,
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
        self.user = "test__1"
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
            if opt == 10:
                new_roommap = input("input the new roommap")
                print(self.changemap(new_roommap))
            else:
                continue
        self.client.close()
        exit(0)


if __name__ == "__main__":
    s = ClientMain()
    # s.start()
