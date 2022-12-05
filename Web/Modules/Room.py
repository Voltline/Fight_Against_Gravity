import Web.Modules.User as User
import server_game
import queue
import threading

_debug_ = 1


class Room:
    """
    房间类 存储玩家，房间号，运行每局游戏主逻辑
    """

    def __init__(self, roomid, owner: User, roomname: str, roommap: str):
        self.roomid = roomid
        self.owner = owner
        self.roomname = roomname
        self.userlist: [User] = [owner]
        self.roommap = roommap
        self.game = None
        self.message_queue = queue.Queue()
        self.started = False

    def start(self):
        self.started = True
        if _debug_:
            print("[room debug info]{}{}started".format(self.roomname, self.roomid))
            return True
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
        thread = threading.Thread(target=self.game.main())
        thread.setDaemon(True)
        thread.setName("game of room {}{}".format(self.roomname, self.roomid))
        thread.start()

    def get_started(self):
        return self.started

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

    def get_roomname(self):
        return self.roomname

    def get_roomid(self):
        return self.roomid

    def get_owener(self) -> User:
        """返回房主 User"""
        return self.owner

    def get_roommap(self):
        return self.roommap

    def get_userlist(self) -> [User]:
        return self.userlist

    def change_map(self, roommap: str):
        self.roommap = roommap

    def del_user(self, user: User):
        """
        删除玩家
        """
        if user in self.userlist:
            self.userlist.remove(user)

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
            "userlist": userlist
        }
        return res
