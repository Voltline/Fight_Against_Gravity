import socket
import threading

import Web.Modules.safeserver as safeserver
import Web.Modules.safeclient as safeclient
import Web.Modules.OptType as OptType
import json
import uuid
import server_game
import queue
import os

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

    def set_roomid(self, roomid):
        self.roomid = roomid

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

    def __init__(self, roomid, owner: User, roomname: str, roommap: str):
        self.roomid = roomid
        self.owner = owner
        self.roomname = roomname
        self.userlist = [owner]
        self.roommap = roommap
        self.game = None
        self.message_queue = queue.Queue()

    def start(self):
        # TODO:检查玩家准备状态
        self.game = server_game.ServerGame(
            settings=[],
            net=self.message_queue,
            room_id=self.roomid,
            map_name=self.roommap,
            player_names=self.get_userlist()
        )
        """
        不知道settings是什么 留空了
        net不能从server传出，暂时不能作为参数传递
        map还没有进行合法性检测 可能导致服务器异常 已经在TODO了
        
        """
        if _debug_:
            print("start")
            return 0
        thread = threading.Thread(target=self.game.main())
        thread.setDaemon(True)
        thread.setName("game of room {}{}".format(self.roomname, self.roomid))
        thread.start()

    def get_message(self):
        """
        从房间消息队列获取游戏相关消息
        """
        if self.message_queue.empty():
            return None
        res = self.message_queue.get()
        return res

    def push_message(self, message):
        """
        向房间消息队列push相关游戏消息
        """
        self.message_queue.put(message)

    def get_roomid(self):
        return self.roomid

    def get_owener(self):
        return self.owner

    def get_roomname(self):
        return self.roomname

    def get_userlist(self) -> [User]:
        return self.userlist

    def change_map(self, roommap: str):
        self.roommap = roommap

    def del_user(self, user: User):
        """
        删除玩家
        """
        self.userlist.remove(user)

    def join_user(self, user: User):
        self.userlist.append(user)

    def get_all_info(self):
        """
        返回所有属性
        """
        return self.roomid, self.owner, self.roomname, self.userlist, self.roommap,

    # TODO: 选择地图 踢出多余的人 room大厅 开始游戏/准备 start 房主离开更换房主
    # TODO：get_message


class ServerMain:
    """
    服务器主类 运行服务器主逻辑
    """

    def __init__(self):
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
    def back_msg(message: dict, feedback: str):
        message["status"] = feedback
        return message

    @staticmethod
    def check(user: str, password: str) -> bool:
        """
        真的去注册服务器 进行check
        """
        if _debug_:
            print("[debug info]ACK user", user)
            return True
        with open("Modules/settings.json", 'r') as f:
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
        else:
            roomid = str(uuid.uuid1())
            # TODO:检测roommap是否合法
            newroom = Room(roomid, user, roomname, roommap)
            self.room_list[roomid] = newroom
            user.set_roomid(roomid)
            sendMsg = messageMsg
            sendMsg["status"] = "ACK"
            sendMsg["roomid"] = roomid
            print("[game info]user {} creat room {}, id {}".format(user, roomname, roomid))
            self.server.send(messageAdr, sendMsg)

    def deleteroom(self, message):
        """
        删除房间
        """
        OptType.deleteRoom
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
        user = self.user_list[username]
        # TODO:检查roomid，user，owner合法性
        room = self.room_list[roomid]
        room.start()
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))

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
        # TODO：玩家掉线后从房间清除
        for name, user in self.user_list.items():
            if user.get_address() not in connections:
                if _debug_:
                    print("[debug info]user {0} is unused".format((name, user.get_address())))
                to_del.append(name)
        for item in to_del:
            print("[game info]user {0} left the game".format((item, self.user_list[item].name)))
            self.user_list.pop(item)

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
                else:
                    print("[warning]unexpected opt", message)
            self.clear()


if __name__ == "__main__":
    _debug_ = True  # 测试环境debug设置为1
    s = ServerMain()
    s.start()
