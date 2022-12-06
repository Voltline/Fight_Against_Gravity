from Modules import safeserver
from Modules import safeclient
from Modules import  OptType
from Modules.User import User
from Modules.Room import Room
from content.maps.map_obj import Map
import json
import uuid
import os

OptType = OptType.OptType
_debug_ = False  # debug选项 请勿在生产环境中开启


# TODO：get_message
# TODO:分发消息给玩家/玩家固定时间更新游戏状态
# TODO：debugger

class ServerMain:
    """
    服务器主类 运行服务器主逻辑
    """

    def __init__(self):
        # 获取服务器IP和端口
        current_path = os.getcwd()
        fag_directory = os.path.dirname(current_path)
        os.chdir(fag_directory)
        with open("Web/Modules/settings.json", "r") as f:
            settings = json.load(f)
        ip = settings["Client"]["Game_Local_IP"]
        port = settings["Client"]["Game_Port"]
        heart_beat = settings["Client"]["heart_beat"]
        if _debug_:
            ip = "localhost"
            port = 25555

        self.user_list: {str: User} = {}
        """{"username" : User}"""
        self.room_list: {str: Room} = {}
        """"{"roomid": Room}"""
        self.server = safeserver.SocketServer(ip, port, debug=False, heart_time=heart_beat)

    @staticmethod
    def get_map_size(mapname: str):
        """获取地图大小"""
        Map.load_maps()
        map_ = Map(mapname)
        return len(map_.ships_info)

    @staticmethod
    def back_msg(message: dict, feedback: str):
        message["status"] = feedback
        return message

    @staticmethod
    def check(user: str, password: str) -> bool:
        """
        真的去注册服务器 进行check
        """
        # if _debug_:
        #     print("[debug info]ACK user", user)
        #     return True
        with open("Web/Modules/settings.json", 'r') as f:
            information = json.load(f)
        reg_ip = information["Client"]["Reg_IP"]
        reg_port = information["Client"]["Reg_Port"]
        key = information["AES_Key"]
        information = ''
        msg = {
            "opt": OptType.loginTransfer,
            "user": user,
            "password": password
        }
        check_client = safeclient.SocketClient(reg_ip, reg_port, password=key)
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
            print("[game info]user {} join the game".format(newUser.get_name()))
            self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
        else:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            self.server.close(messageAdr)

    def creatroom(self, message):
        """
        创建房间
        """
        messageAdr, messageMsg = message
        username, roomname, roommap = messageMsg["user"], messageMsg["roomname"], messageMsg["roommap"]
        user = self.user_list[username]
        if _debug_:
            print("[debug] userlist", self.user_list)
        if username not in self.user_list:
            # 非法用户
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            sendMsg["roomid"] = None
            self.server.send(messageAdr, sendMsg)
        if user.get_roomid():
            # 用户已在房间
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            sendMsg["roomid"] = None
            self.server.send(messageAdr, sendMsg)
        try:
            self.get_map_size(roommap)
        except Exception as err:
            # 创建的房间地图错误
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            sendMsg["roomid"] = None
            self.server.send(messageAdr, sendMsg)
        else:
            roomid = str(uuid.uuid1())
            newroom = Room(roomid, user, roomname, roommap)
            self.room_list[roomid] = newroom
            user.set_roomid(roomid)
            sendMsg = messageMsg
            sendMsg["status"] = "ACK"
            sendMsg["roomid"] = roomid
            print("[game info]user {} creat room {}, id {}".format(username, roomname, roomid))
            self.server.send(messageAdr, sendMsg)

    def changemap(self, message):
        # TODO:changemap
        pass

    def deleteroom(self, message):
        """
        删除房间
        """
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        user = self.user_list[username]
        print(roomid, username)
        if roomid not in self.room_list:
            # print("not in list")
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        if self.room_list[roomid].owner.get_name() != messageMsg["user"]:
            # print("not owner")
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        if len(self.room_list[roomid].userlist) > 1:
            # print("not empty")
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room: Room = self.room_list[roomid]
        print("[game info]room ({}{}) was deleted".format(room.get_roomname(), room.get_roomid()))
        self.room_list.pop(roomid)
        user.set_roomid(None)
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
        return True

    def startgame(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        room = self.room_list[roomid]
        if room.get_owener().get_name() != username:
            # 非房主不允许开始游戏
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        for game_user in room.get_userlist():
            # 玩家咩准备好不允许开始游戏
            if not game_user.get_ready() and game_user != room.get_owener():
                self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
                return False
        room.start(self.server)
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))

    def ready(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        isready = messageMsg["ready"]
        if (roomid not in self.room_list) or (username not in self.user_list):
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        user = self.user_list[username]
        if isready == "YES":
            user.ready()
        else:
            user.dready()
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))

    def joinroom(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        user = self.user_list[username]
        if roomid not in self.room_list:
            # 不存在的房间
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
        room = self.room_list[roomid]
        if len(room.get_userlist()) == self.get_map_size(room.get_roommap()):
            # 房间人数上限
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
        room.join_user(user)
        user.set_roomid(room.get_roomid())
        sendMsg = messageMsg
        sendMsg["status"] = "ACK"
        sendMsg["roomid"] = room.get_roomid()
        self.server.send(messageAdr, sendMsg)

    def leftroom(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        if roomid not in self.room_list:
            # 非法房间
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room = self.room_list[roomid]
        user = self.user_list[username]
        if user.get_name() == room.get_owener().get_name():
            # 房主不允许离开
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False

        room.del_user(user)
        user.set_roomid(None)
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
        return True

    def getroom(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        if roomid not in self.room_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room: Room = self.room_list[roomid]
        sendMsg = messageMsg
        sendMsg["status"] = "ACK"
        sendMsg["room"] = room.get_all_info()
        # print("[debug info]", sendMsg)
        self.server.send(messageAdr, sendMsg)

    def getroomlist(self, message):
        messageAdr, messageMsg = message
        reslist = []
        for roomid, room in self.room_list.items():
            owner = room.owner.get_name()
            maxsize = self.get_map_size(room.get_roommap())
            size = len(room.get_userlist())
            started = room.get_started()
            if started:
                started = "YES"
            else:
                started = "NO"
            reslist.append(
                {
                    "roomid": roomid,
                    "owner": owner,
                    "size": size,
                    "maxsize": maxsize,
                    "started": started
                }
            )
        sendMsg = messageMsg
        sendMsg["roomlist"] = reslist[:]
        print(sendMsg)
        self.server.send(messageAdr, sendMsg)

    def clear(self):
        """
        处理失效连接
        """
        # 清除已失效连接
        connections = self.server.get_connection()
        to_del = []  # 即将删除的连接
        # 找到已掉线的玩家列表
        for name, user in self.user_list.items():
            if user.get_address() not in connections:
                if _debug_:
                    print("[debug info]user {0} is unused".format((name, user.get_address())))
                to_del.append(name)
        # 清除与掉线玩家有关的数据
        for item in to_del:
            print("[game info]user {0} left the game".format((item, self.user_list[item].name)))
            user: User = self.user_list[item]
            roomid = user.get_roomid()
            if roomid in self.room_list:
                room = self.room_list[roomid]
                room.del_user(user)
            self.user_list.pop(item)
        to_del.clear()
        # 找到空的房间列表
        for roomid, room in self.room_list.items():
            if len(room.get_userlist()) == 0:
                to_del.append(roomid)
        # 清除空房间
        for item in to_del:
            self.room_list.pop(item)

    def start(self):
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
                elif opt == OptType.startgame:
                    self.startgame(message)
                elif opt == OptType.joinRoom:
                    self.joinroom(message)
                elif opt == OptType.leftRoom:
                    self.leftroom(message)
                elif opt == OptType.getRoom:
                    self.getroom(message)
                elif opt == OptType.changemap:
                    self.changemap(message)
                elif opt == OptType.getRoomlist:
                    self.getroomlist(message)
                elif opt == OptType.userready:
                    self.ready(message)
                else:
                    # TODO：消息转发到每个房间
                    print("[warning]unexpected opt", message)
            self.clear()


if __name__ == "__main__":
    _debug_ = True  # 测试环境debug设置为1
    s = ServerMain()
    s.start()
