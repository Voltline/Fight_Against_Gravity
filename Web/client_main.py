import Web.Modules.safeclient as safeclient
import Web.Modules.OptType as OptType

OptType = OptType.OptType


class ClientMain:
    def __init__(self):
        pass

    def login(user: str, password: str, client: safeclient.SocketClient):
        msg = {
            "opt": OptType.login,
            "user": user,
            "password": password
        }
        client.send(msg)
        recvMsg = client.receive()
        if recvMsg["status"] == "ACK":
            print("ACK")
            return True
        else:
            print("NAK")
            print("登陆失败 请重新启动游戏")
            input("回车以继续")
            return False

    def creatroom(user: str):
        msg = {
            "opt": OptType.creatRoom,
            "user": user
        }


if __name__ == "__main__":
    client = safeclient.SocketClient("localhost", 25555, heart_beat=5)
    user = input("input the user name")
    password = input("input the pass word")
    if not login(user, password, client):
        client.close()
        exit(0)
    while True:
        pass
