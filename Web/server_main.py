import Web.Modules.safeserver as safeserver
import Web.Modules.safeclient as safeclient
import Web.Modules.OptType as OptType
import json
import uuid

OptType = OptType.OptType
_debug_ = False  # debug选项 请勿在生产环境中开启


class User:
    """
    玩家类 存储玩家信息 包括address name 房间号
    """

    def __init__(self, add, name: str):
        self.address = add
        self.name = name
        self.roomid = None

    def get_address(self):
        return self.address

    def get_name(self):
        return self.name

    def get_roomid(self):
        return self.roomid


class Room:
    """
    房间类 存储玩家，房间号，运行每局游戏主逻辑
    """

    def __init__(self, roomid, owner: User):
        self.roomid = roomid
        self.owner = owner
        self.roomname = None
        self.userlist = [owner]
        pass
    # TODO：修改 用成员函数
    # TODO: 选择地图 踢出多余的人 room大厅 开始游戏/准备 start
    # TODO：get_message


class ServerMain:
    """
    服务器主类 运行服务器主逻辑
    """

    def __init__(self):
        self.user_list = {}
        """{"username" : User}"""
        self.room_list = {}
        """"{roomid: Room}"""
        self.server = safeserver.SocketServer("127.0.0.1", 25555, heart_time=5, debug=_debug_)

    def back_msg(self, message: dict, feedback: str):
        # TODO:"ACK"/"NAK"
        pass

    @staticmethod
    def check(user: str, password: str) -> bool:
        """
        真的去注册服务器 进行check
        """
        if _debug_:
            pass
            print("[debug info]ACK user", user)
            return True
        with open("Modules/settings.json", 'r') as f:
            information = json.load(f)
        reg_ip = information["Client"]["Reg_IP"]
        reg_port = information["Client"]["Reg_Port"]
        information = ''
        msg = {
            "opt": OptType.loginTransfer,
            "user": user,
            "password": password
        }
        check_client = safeclient.SocketClient(reg_ip, reg_port)
        check_client.send(msg)
        status = check_client.receive()
        check_client.close()
        if status == "ERROR":
            return False
        elif status == "close":
            return True
        else:
            print("ServerReturnError!")
            return False

    def login(self, message):
        """
        处理用户登录请求
        """
        messageAdr, messageMsg = message
        if self.check(messageMsg["user"], messageMsg["password"]):
            newUser = User(messageAdr, messageMsg["user"])
            self.user_list[messageMsg["user"]] = newUser
            print(self.user_list)
            sendMsg = messageMsg
            sendMsg["status"] = "ACK"
            self.server.send(messageAdr, sendMsg)
        else:
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            self.server.send(messageAdr, sendMsg)
            self.server.close(messageAdr)

    def creatroom(self, message):
        """
        创建房间
        #TODO:roomname roommap
        """
        messageAdr, messageMsg = message
        user = messageMsg["user"]
        if(_debug_):
            print("[debug] userlist",self.user_list)
        if user not in self.user_list:
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            sendMsg["roomid"] = None
            self.server.send(messageAdr, sendMsg)
        else:
            roomid = str(uuid.uuid1())
            newroom = Room(roomid, self.user_list[user])
            self.room_list[roomid] = newroom
            sendMsg = messageMsg
            sendMsg["status"] = "ACK"
            sendMsg["roomid"] = roomid
            self.server.send(messageAdr, sendMsg)

    def deleteroom(self, message):
        """
        删除房间
        """
        messageAdr, messageMsg = message

        def returnfalse():
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            self.server.send(messageAdr, sendMsg)

        roomid = messageMsg["roomid"]
        if roomid not in self.room_list:
            returnfalse()
            return False
        if self.room_list[roomid].owner != messageMsg["user"]:
            returnfalse()
            return False
        if len(self.room_list[roomid].userlist) > 1:
            returnfalse()
            return False
        self.room_list.pop(roomid)
        sendMsg = messageMsg
        sendMsg["status"] = "ACK"
        self.server.send(messageAdr, sendMsg)
        return True

    def joinroom(self, message):
        # TODO joinroom
        pass

    def leftroom(self, message):
        # TODO leftroom
        pass

    def getroom(self, message):
        # TODO getroom
        pass

    def clear(self):
        """
        处理失效连接
        """
        # 清除已失效连接
        connections = self.server.get_connection()
        to_del = []  # 即将删除的连接
        # print(connections)
        for name, user in self.user_list.items():
            if user.get_address() not in connections:
                if _debug_:
                    print("[debug info]user {0} is unused".format((name, user.get_address())))
                to_del.append(name)
        for item in to_del:
            print("[game info]user {0} left the game".format((item, self.user_list[item].name)))
            self.user_list.pop(item)

    def start(self):
        self.server.start()
        print("[game info] server start")
        while True:
            # 处理消息队列
            messages = self.server.get_message()
            for message in messages:
                if _debug_:
                    print("[debug info]message", message)
                messageAdr, messageMsg = message
                """
                解码后的message
                """
                opt = messageMsg["opt"]
                if opt == OptType.login:
                    self.login(message)
                elif opt == OptType.creatRoom:
                    self.creatroom(message)
                elif opt == OptType.deleteRoom:
                    self.deleteroom(message)
                else:
                    print("[warning]unexpected opt", message)
            self.clear()


if __name__ == "__main__":
    _debug_ = True  # 测试环境debug设置为1
    s = ServerMain()
    s.start()
