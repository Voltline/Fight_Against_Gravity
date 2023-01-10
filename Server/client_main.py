import time

from Server.Modules import OptType, safeclient
from Server.Modules.Flogger import Flogger
from Server.identify_client import IdentifyClient
import sys
import json

OptType = OptType.OptType


class ClientMain:
    def __init__(self, path, _debug_=False):
        self.path = path
        self.logger = Flogger(models=Flogger.FILE_AND_CONSOLE, level=Flogger.L_INFO,
                              folder_name="client_main", logpath=path)
        self.absolute_setting_path = path + "settings/settings.json"
        self.client_models = Flogger.FILE
        self.client_level = Flogger.L_INFO
        if "--debug" in sys.argv:
            self.absolute_setting_path = path + "settings/settings_local.json"
        if "--sakura" in sys.argv:
            self.absolute_setting_path = path + "settings/settings_sakura.json"
        if "--logger" in sys.argv:
            self.client_models = Flogger.FILE_AND_CONSOLE
            self.client_level = Flogger.L_DEBUG
        with open(self.absolute_setting_path, "r") as f:
            settings = json.load(f)
        self.ip = settings["Client"]["Game_Online_IP"]
        self.port = settings["Client"]["Game_Online_Port"]
        self.heart_beat = settings["Client"]["heart_beat"]
        self.reg_ip = settings["Client"]["Reg_IP"]
        self.reg_port = settings["Client"]["Reg_Port"]
        self.aes_key = settings["AES_Key"]
        self.msg_len = settings["Client"]["msg_len"]
        self.client = None
        self.user = None
        self.roomid = None
        self.is_start = False

    def get_start(self):
        return self.is_start

    def start_client(self):
        if self.is_start:
            return False
        self.is_start = True
        try:
            self.client = safeclient.SocketClient(self.ip, self.port, heart_beat=self.heart_beat,
                                                  models=self.client_models,
                                                  logpath=self.path, level=self.client_level, msg_len=self.msg_len)
        except Exception as err:
            self.is_start = False
            self.logger.error("客户端启动失败" + str(err))
            # exit(-1)
            raise Exception("无法连接到服务器")

    def register_get_checkcode(self, username, email):
        identify_client = IdentifyClient(self.reg_ip, self.reg_port, self.ip, self.port, self.aes_key)
        # identify_client = safeclient.SocketClient(self.reg_ip, self.reg_port, password=se)
        check_code = identify_client.get_check_code(username, email)
        self.logger.info("[register]user:{} email:{}Register get check_code".format(username, email))
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

    def reset_get_checkcode(self, username, email):
        identify_client = IdentifyClient(self.reg_ip, self.reg_port, self.ip, self.port, self.aes_key)
        # identify_client = safeclient.SocketClient(self.reg_ip, self.reg_port, password=se)
        check_code = identify_client.reset_get_check_code(username, email)
        self.logger.info("[register]user:{} email:{}Reset get check_code.".format(username, email))
        del identify_client
        return check_code

    def reset_push_password(self, username, email, check_code, input_check_code, password):
        identify_client = IdentifyClient(self.reg_ip, self.reg_port, self.ip, self.port, self.aes_key)
        if check_code != '':
            if check_code.lower() == input_check_code.lower():
                result = identify_client.reset_send_password(username, email, password)
                del identify_client
                if result is True:
                    self.logger.info("[register]{}{}Reset Successfully!".format(username, email))
                    return True
                else:
                    self.logger.info("[register]{}{}Reset Failed!".format(username, email))
                    return False
            else:
                self.logger.info("[register]{}{}Reset Failed!".format(username, email))
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

    def changeroomname(self, new_roomname):
        msg = {
            "opt": OptType.changeroomname,
            "user": self.user,
            "roomid": self.roomid,
            "new_roomname": new_roomname
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
        while 'status' not in recv:
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
        while 'status' not in recv:
            recv = self.client.receive()
        if recv["status"] == "ACK":
            self.roomid = recv["roomid"]
            return True
        elif recv["status"] == "NAK":
            return False

    def is_in_room(self):
        """返回是不是在房间里"""
        return self.roomid is not None

    def local_get_user(self):
        return self.user

    def local_isowner(self):
        res = self.getroom()
        if res:
            return self.user == res["owner"]
        else:
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

        if "status" in recv:
            if recv["status"] == "NAK":
                return False
            elif recv["status"] == "ACK":
                self.roomid = None
                return True
            else:
                pass
        else:
            self.roomid = None
            return True

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
        try:
            if recv["status"] == "NAK":
                return False
            elif recv["status"] == "ACK":
                return True
            else:
                pass
        except Exception as err:
            self.logger.error(str(err))
            return True

    def getroom(self):
        """
        {
            roomid : "str"
            roomname : "str"
            owner: "str"
            roommap: "str"
            userlist : {
                user:ready
            }
        }
        """
        if self.roomid is None:
            return False
        msg = {
            "opt": OptType.getRoom,
            "roomid": self.roomid
        }
        self.client.send(msg)
        # recv = self.client.receive()
        # if recv["status"] == "NAK":
        #     return False
        # res = recv["room"]
        # return res

    def getroomlist(self):
        """
        拆分消息实现，
        [{
            "roomid": uuid(str),
            "owner": 房主名(str),
            "size": 玩家人数(int),
            "started": 是否在游戏中(int:0/1),
            "roommap" : 地图名(str),
            "roomname" : 房间名(str)
        }]
        """
        msg = {
            "opt": OptType.getRoomlist,
        }
        self.client.send(msg)
        recv = self.client.receive()
        lenth = recv["length"]
        reslist = []
        for i in range(lenth):
            recv = self.client.receive()
            reslist.append(recv["roomlist"])
            # print(recv)
        return reslist

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

    def logout(self):
        msg = {
            "opt": OptType.logout,
            "user": self.user,
            "roomid": self.roomid
        }
        self.client.send(msg)
        recv = self.client.receive()
        if recv["status"] == "ACK":
            self.user = None
            self.roomid = None
            # self.client.close()
            # del self.client
            return True
        else:
            return False

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
        self.start_client()
        self.user = input("input the user name")
        password = input("input the pass word")
        # self.user = "sxm250"
        # password = "123123"
        if not self.login(self.user, password):
            self.client.close()
            exit(-1)
        # print(self.creatroom("12345678901234567890", "地月系统"))
        # for i in range(1000):
        #     st = time.time()
        #     self.deleteroom()
        #     print(time.time() - st)
        while True:
            ints = input()
            opt = -1
            if ints.isdigit():
                opt = int(ints)
            else:
                pass
            if opt == 0:
                self.logout()
                break;
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
            if opt == 11:
                new_roomname = input("input the new roomname")
                print(self.changeroomname(new_roomname))
            else:
                continue
        self.client.close()
        exit(0)


if __name__ == "__main__":
    s = ClientMain()
    # s.start()
