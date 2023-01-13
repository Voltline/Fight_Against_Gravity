import sys
import time
import pygame
from Server.Modules import OptType, safeclient, safeserver
from Server.Modules.Flogger import Flogger
from Server.Modules.User import User
from Server.Modules.Room import Room
from Server.Modules.udpserver import UdpServer
from content.maps.map_obj import Map
import json
import uuid
import os

OptType = OptType.OptType


# TODO：debugger
class ServerMain:
    """
    服务器主类 运行服务器主逻辑
    """

    def __init__(self, game_settings, path, _debug_=False):
        # 获取服务器IP和端口
        self.absolute_setting_path = path + "/settings/settings.json"
        self.logger = Flogger(models=Flogger.FILE_AND_CONSOLE, level=Flogger.L_INFO,
                              folder_name="server_main", logpath=path)
        server_model = Flogger.FILE
        server_level = Flogger.L_INFO
        if _debug_:
            self.absolute_setting_path = path + "settings/settings_local.json"
        if "--sakura" in sys.argv:
            self.absolute_setting_path = path + "settings/settings_sakura.json"
        if "--logger" in sys.argv:
            server_model = Flogger.FILE_AND_CONSOLE
            server_level = Flogger.L_DEBUG
        with open(self.absolute_setting_path, "r") as f:
            settings = json.load(f)
        ip = settings["Client"]["Game_Local_IP"]
        port = settings["Client"]["Game_Local_Port"]
        udp_ip = settings["Client"]["Udp_Local_IP"]
        udp_port = settings["Client"]["Udp_Local_Port"]
        heart_beat = settings["Client"]["heart_beat"]
        self.msg_len = settings["Client"]["msg_len"]
        self.user_list: {str: User} = {}
        """{"username" : User}"""
        self.tmp_user_list: {str: User} = {}
        """正在建立连接的用户{"username" : User}"""
        self.room_list: {str: Room} = {}
        """"{"roomid": Room}"""
        self.server = safeserver.SocketServer(ip, port, debug=False, heart_time=heart_beat,
                                              models=server_model, logpath=path, level=server_level,
                                              msg_len=self.msg_len)
        # print(udp_ip, udp_port)
        self.udp_server = UdpServer(udp_ip, udp_port, self.msg_len)
        self.game_settings = game_settings

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
    def check(user: str, password: str, path) -> bool:
        """
        真的去注册服务器 进行check
        """
        with open(path, 'r') as f:
            information = json.load(f)
        reg_ip = information["Client"]["Reg_IP"]
        reg_port = information["Client"]["Reg_Port"]
        key = information["AES_Key"]
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
            return False

    def login(self, message):
        """
        处理用户登录请求
        """
        messageAdr, messageMsg = message
        id = messageMsg["id"]
        if id == 1:  # tcp建立连接
            recv = False
            try:
                recv = self.check(messageMsg["user"], messageMsg["password"], path=self.absolute_setting_path)
            except Exception as err:
                self.logger.error("验证服已被关闭" + str(err))
            if (messageMsg["user"] not in self.user_list) and recv and (messageMsg["user"] not in self.tmp_user_list):
                newUser = User(messageAdr, messageMsg["user"])
                self.tmp_user_list[messageMsg["user"]] = newUser
                self.logger.info(
                    "[game info]user {},ip{},connect the game with tcp".format(newUser.get_name(), str(messageAdr)))
                self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
                return True
            else:
                self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
                return False
        if id == 2:  # udp建立连接
            if messageMsg["user"] in self.tmp_user_list:
                user = self.tmp_user_list[messageMsg["user"]]
                user.set_udp_address(messageAdr)
                self.udp_server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
                self.logger.info(
                    "[game info]user {},ip{},connect the game with udp".format(user.get_name(), str(messageAdr)))
            else:
                self.udp_server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
        if id == 3:
            if (messageMsg["user"] in self.tmp_user_list) and \
                    self.tmp_user_list[messageMsg["user"]].get_udp_address() and \
                    (messageMsg["user"] not in self.user_list):
                user = self.tmp_user_list[messageMsg["user"]]
                self.user_list[messageMsg["user"]] = user
                self.tmp_user_list.pop(messageMsg["user"])
                self.logger.info(
                    "[game info]user {},tcp_address{},udp_address{},connect the game with tcp".
                    format(user.get_name(),
                           user.get_address(),
                           user.get_udp_address()))
                self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
            else:
                self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))

    def logout(self, message):
        """
        用户登出
        """
        messageAdr, messageMsg = message
        if messageMsg["user"] not in self.user_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        if messageMsg["user"] in self.user_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
            user: User = self.user_list[messageMsg["user"]]
            roomid = user.get_roomid()
            if roomid in self.room_list:
                room: Room = self.room_list[roomid]
                room.del_user(user)
            # self.server.close(messageAdr)
            self.logger.info("[game info]user {} logout the game".format(user.get_name()))
            self.user_list.pop(messageMsg["user"])
            return True

    def creatroom(self, message):
        """
        创建房间
        """
        messageAdr, messageMsg = message
        username, roomname, roommap = messageMsg["user"], messageMsg["roomname"], messageMsg["roommap"]
        if username not in self.user_list:
            # 非法用户
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            sendMsg["roomid"] = None
            self.server.send(messageAdr, sendMsg)
            return False
        user = self.user_list[username]
        if user.get_roomid():
            # 用户已在房间
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            sendMsg["roomid"] = None
            self.server.send(messageAdr, sendMsg)
            return False
        try:
            self.get_map_size(roommap)
        except Exception as err:
            # 创建的房间地图错误
            sendMsg = messageMsg
            sendMsg["status"] = "NAK"
            sendMsg["roomid"] = None
            self.logger.error("[creatroom]wrong roommap" + str(err))
            self.server.send(messageAdr, sendMsg)
        else:
            roomid = str(uuid.uuid1())
            newroom = Room(roomid, user, roomname, roommap, self.udp_server, self.server, self.game_settings)
            self.room_list[roomid] = newroom
            user.set_roomid(roomid)
            sendMsg = messageMsg
            sendMsg["status"] = "ACK"
            sendMsg["roomid"] = roomid
            self.logger.info("[game info]user {} creat room {}, id {}".format(username, roomname, roomid))
            self.server.send(messageAdr, sendMsg)

    def changemap(self, message):
        messageAdr, messageMsg = message
        username, roomid, nroommap = messageMsg["user"], messageMsg["roomid"], messageMsg["roommap"]
        if roomid not in self.room_list:  # 无效房间
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room = self.room_list[roomid]
        maxsize = 0
        try:
            maxsize = self.get_map_size(nroommap)
        except Exception as err:
            self.logger.error("[in changemap]" + str(err))
        if maxsize < len(room.get_userlist()):  # 房间人数大于新地图人数
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        self.logger.info(
            "[game info]room {},id{},changed map from {} to {}".format(room.get_roomname(), roomid, room.get_roommap(),
                                                                       nroommap))
        room.change_map(nroommap)
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
        return True

    def changeroomname(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        if username not in self.user_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        if roomid not in self.room_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room = self.room_list[roomid]
        room.changeroomname(messageMsg["new_roomname"])
        self.logger.info(
            "room {},id{},changed roomname to {}".format(room.get_roomname(), roomid, messageMsg["new_roomname"]))
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))

    def deleteroom(self, message):
        """
        删除房间
        """
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        if username not in self.user_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        user = self.user_list[username]
        if roomid not in self.room_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        if self.room_list[roomid].owner.get_name() != messageMsg["user"]:
            # 用户不是房主
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room: Room = self.room_list[roomid]
        room.del_user(user)
        if len(self.room_list[roomid].userlist) == 0:
            # 用户没了
            room.stop()
            self.logger.info(
                "[game info]room (roomname:{},roomid:{}) was deleted".format(room.get_roomname(), room.get_roomid()))
            self.room_list.pop(roomid)
        else:
            useer_list = room.get_userlist()
            room.change_ownener(useer_list[0])
        user.set_roomid(None)
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
        return True

    def startgame(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        if roomid not in self.room_list:
            """非法房间"""
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
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
        if room.get_started():
            """游戏已经开始，不能重复开始"""
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        self.logger.info("[game info]room ({}{}) start game".format(room.get_roomname(), room.get_roomid()))
        room.start()
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
        self.logger.info("[game info] user " + username + " is ready? " + isready)
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))

    def joinroom(self, message):
        messageAdr, messageMsg = message
        roomid = messageMsg["roomid"]
        username = messageMsg["user"]
        if username not in self.user_list:
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        user = self.user_list[username]
        if roomid not in self.room_list:
            # 不存在的房间
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room = self.room_list[roomid]
        if len(room.get_userlist()) == self.get_map_size(room.get_roommap()):
            # 房间人数上限
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        if room.get_started():
            # 游戏已开始
            self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            return False
        room.join_user(user)
        user.set_roomid(room.get_roomid())
        sendMsg = messageMsg
        sendMsg["status"] = "ACK"
        sendMsg["roomid"] = room.get_roomid()
        self.logger.info("[game info]user {} join the room {}".format(username, room.get_roomname()))
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
            # 房主调用删除房间来离开
            # self.server.send(messageAdr, self.back_msg(messageMsg, "NAK"))
            self.deleteroom(message)
            if room.get_started():
                room.game.player_quit(user.get_name())
            self.logger.info("[game info]user {} left the room {}".format(username, room.get_roomname()))
            return True

        if room.get_started():
            room.game.player_quit(user.get_name())
        room.del_user(user)
        user.set_roomid(None)
        self.server.send(messageAdr, self.back_msg(messageMsg, "ACK"))
        self.logger.info("[game info]user {} left the room {}".format(username, room.get_roomname()))
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
        self.server.send(messageAdr, sendMsg)

    def getroomlist(self, message):
        """拆分消息实现"""
        messageAdr, messageMsg = message
        reslist = []
        for roomid, room in self.room_list.items():
            owner = room.owner.get_name()
            size = len(room.get_userlist())
            started = room.get_started()
            roommap = room.get_roommap()
            roomname = room.get_roomname()
            reslist.append(
                {
                    "roomid": roomid,
                    "owner": owner,
                    "size": size,
                    "started": started,
                    "roommap": roommap,
                    "roomname": roomname
                }
            )
        sendMsg = messageMsg
        sendMsg["length"] = len(reslist)
        self.server.send(messageAdr, sendMsg)
        for i in range(len(reslist)):
            sendMsg["id"] = i
            sendMsg["roomlist"] = reslist[i]
            self.server.send(messageAdr, sendMsg)
            time.sleep(0.1)

    def ping_test(self, message):
        messageAdr, messageMsg = message
        sendMsg = {
            "opt": OptType.PingTest
        }
        self.server.send(messageAdr, sendMsg)
        # self.logger.info("[game info]send Addr {0} ping test".format(messageAdr))

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
                to_del.append(name)
        # 清除与掉线玩家有关的数据
        for item in to_del:
            self.logger.info("[game info]user {0} left the game".format((item, self.user_list[item].name)))
            user: User = self.user_list[item]
            roomid = user.get_roomid()
            if roomid in self.room_list:
                room = self.room_list[roomid]
                room.del_user(user)
            self.user_list.pop(item)
        to_del.clear()
        # 找到已掉线的申请玩家列表
        for name, user in self.tmp_user_list.items():
            if user.get_address() not in connections:
                to_del.append(name)
        # 清除与掉线玩家有关的数据
        for item in to_del:
            self.logger.info("[game info]user {0} stop join the game".format((item, self.tmp_user_list[item].name)))
            user: User = self.tmp_user_list[item]
            self.tmp_user_list.pop(item)
        to_del.clear()
        # 找到空的房间列表
        for roomid, room in self.room_list.items():
            if len(room.get_userlist()) == 0:
                room.stop()
                to_del.append(roomid)
        # 清除空房间
        for item in to_del:
            self.room_list.pop(item)
            self.logger.info("[game info]room {} is deleted".format(item))

    def start(self):
        self.logger.critical("[game info] server start")
        while True:
            # 处理消息队列
            time.sleep(0.001)
            # TCP
            messages = self.server.get_message()  + self.udp_server.get_message()
            for message in messages:
                self.logger.debug("[debug info]message" + str(message))
                messageAdr, messageMsg = message
                """
                解码后的message
                """
                opt = messageMsg["opt"]
                if opt == OptType.login:
                    self.login(message)
                elif opt == OptType.logout:
                    self.logout(message)
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
                elif opt == OptType.changeroomname:
                    self.changeroomname(message)
                elif 27 <= opt <= 30:
                    room_id = messageMsg['args'][0]
                    if room_id in self.room_list:
                        room: Room = self.room_list[room_id]
                        room.release_message(message)
                elif opt == OptType.PingTest:
                    self.ping_test(message)
                else:
                    self.logger.warning("unexpected udp message opt" + str(message))
            self.clear()


if __name__ == "__main__":
    s = ServerMain()
    try:
        s.start()
    except Exception as err:
        print(err)
