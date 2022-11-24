import Web.Modules.safeserver as safeserver
import Web.Modules.safeclient as safeclient
import json

_debug_ = False  # debug选项 请勿在生产环境中开启


class Room:
    """
    房间类 存储玩家，房间号，运行每局游戏主逻辑
    """

    def __init__(self, ):
        pass


class User:
    """
    玩家类 存储玩家信息 包括address name 房间号
    """

    def __init__(self, add, name: str):
        self.address = add
        self.name = name
        self.roomid = None


class ServerMain:
    """
    服务器主类 运行服务器主逻辑
    """

    def __init__(self):
        self.user_list = {}
        self.room_list = {}  # {"username" : User}
        self.server = None
        self.server = safeserver.SocketSever("127.0.0.1", 25555, heart_time=5, debug=_debug_)

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
            "opt": 3,
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

    def start(self):
        self.server.start()
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
                if messageMsg["opt"] == 1:
                    if _debug_:
                        print("[debug info]checking", message)
                    if self.check(messageMsg["user"], messageMsg["password"]):
                        newUser = User(messageAdr, messageMsg["user"])
                        self.user_list[messageAdr] = newUser
                        sendMsg = {
                            "opt": 2,
                            "status": "ACK"
                        }
                        self.server.send(messageAdr, sendMsg)
                    else:
                        sendMsg = {
                            "opt": 2,
                            "status": "NAK"
                        }
                        self.server.send(messageAdr, sendMsg)
                        self.server.close(messageAdr)
                else:
                    print("unexpected opt", message)
            # 清除已失效连接
            connections = self.server.get_connection()
            to_del = []  # 即将删除的连接
            for userAdd in self.user_list:
                if userAdd not in connections:
                    if _debug_:
                        print("[debug info]user {0} is unused".format((userAdd, self.user_list[userAdd].name)))
                    to_del.append(userAdd)
            for item in to_del:
                print("[game info]user {0} left the game".format((item, self.user_list[item].name)))
                self.user_list.pop(item)


if __name__ == "__main__":
    _debug_ = True  # 测试环境debug设置为1
    s = ServerMain()
    s.start()
