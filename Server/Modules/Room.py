import Server.Modules.User as User
from Server.Modules import OptType

OptType = OptType.OptType
from content.games import server_game
import queue
import threading
import Server.Modules.safeserver as safeserver
from settings import all_settings


class Room:
    """
    房间类 存储玩家，房间号，运行每局游戏主逻辑
    """

    def __init__(self, roomid, owner: User, roomname: str, roommap: str, server: safeserver.SocketServer,
                 game_settings: all_settings.Settings):
        self.roomid = roomid
        self.owner = owner
        self.roomname = roomname
        self.userlist: [User] = [owner]
        self.roommap = roommap
        self.message_queue = queue.Queue()
        self.started = False
        self.server_ = server
        self.game_settings = game_settings
        self.game: server_game.ServerGame = None

    def release_message(self, message):
        address, msg = message
        args = None
        mopt = msg['opt']
        if 'time' in msg:
            time = msg['time']
        if 'tick' in msg:
            tick = msg['tick']
        if 'args' in msg:
            args = msg['args']
        if 'kwargs' in msg:
            kwargs = msg['kwargs']
        if mopt == OptType.StartGame:
            room_id, map_name, player_names = args
            self.start()
        elif mopt == OptType.StopGame:
            room_id = args[0]
            self.game.is_run = False
        elif mopt == OptType.PlayerCtrl:
            room_id, player_name, ctrl_msg = args
            self.game.load_ctrl_msg(player_name, ctrl_msg)
        elif mopt == OptType.CheckClock:
            room_id, player_name = args
            self.game.send_check_clock_msg(player_name, address)
        elif mopt == OptType.ServerStartGameTime:
            if self.game.start_time:
                self.game.send_start_game_time(self.game.start_time)

    def start(self):
        self.started = True
        user_name_list = []
        addr_list = {}
        for user in self.userlist:
            user_name_list.append(user.get_name())
            addr_list[user.get_name()] = user.get_address()
        self.game = server_game.ServerGame(
            settings=self.game_settings,
            net=self.server_,
            room_id=self.roomid,
            map_name=self.roommap,
            player_names=user_name_list,
            addresses=addr_list
        )
        thread = threading.Thread(target=self.game.main)
        thread.setDaemon(True)
        thread.setName("game of room {}{}".format(self.roomname, self.roomid))
        thread.start()

    def stop(self):
        if self.started:
            self.game.is_run = False
            self.started = False

    def get_started(self):
        return self.started

    def get_roomname(self):
        return self.roomname

    def changeroomname(self, new_roomname):
        self.roomname = new_roomname

    def get_roomid(self):
        return self.roomid

    def get_owener(self) -> User:
        """返回房主 User"""
        return self.owner

    def change_ownener(self, user: User):
        self.owner = user

    def get_roommap(self):
        return self.roommap

    def get_userlist(self) -> [User]:
        return self.userlist

    def change_map(self, roommap: str):
        self.roommap = roommap

    def del_user(self, user: User):
        """
        删除玩家
        user: User
        """
        if user in self.userlist:
            self.userlist.remove(user)
        if self.owner not in self.userlist:
            if len(self.userlist):
                self.owner = self.userlist[0]
            else:
                self.owner = None

    def join_user(self, user: User):
        self.userlist.append(user)

    def get_all_info(self):
        """
        返回所有属性
        {
            roomid : "str"
            roomname : "str"
            owner: "str"
            roommap: "str"
            is_run: bool
            userlist : {
                user:ready
            }
        }
        """
        userlist = []
        for item in self.userlist:
            user = item
            userlist.append((user.get_name(), user.get_ready()))
        res = {
            "roomid": self.roomid,
            "roomname": self.roomname,
            "owner": self.owner.get_name(),
            "roommap": self.roommap,
            "is_run": self.started,
            "userlist": userlist
        }
        return res
