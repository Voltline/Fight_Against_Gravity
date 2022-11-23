import Web.Modules.safeserver as safeserver
import Web.Modules.safeclient as safeclient
import json

_debug_ = False  # debug选项 请勿在生产环境中开启


def check(user: str, password: str) -> bool:
    """
    真的去注册服务器 进行check
    """
    if _debug_:
        pass
        # print("[debug info]ACK user", user)
        # return True
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


user_list = {}  # {"username" : address}
if __name__ == "__main__":
    _debug_ = True  # 测试环境debug设置为1
    server = safeserver.SocketSever("127.0.0.1", 25555, heart_time=5, debug=_debug_)
    server.start()
    while True:
        try:
            # 处理消息队列
            messages = server.get_message()
            # print(1)
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
                    if check(messageMsg["user"], messageMsg["password"]):
                        user_list[messageMsg["user"]] = messageAdr
                        sendMsg = {
                            "opt": 2,
                            "status": "ACK"
                        }
                        server.send(messageAdr, sendMsg)
                    else:
                        sendMsg = {
                            "opt": 2,
                            "status": "NAK"
                        }
                        server.send(messageAdr, sendMsg)
                        server.close(messageAdr)
                else:
                    print("unexpected opt", message)
            # 清除已失效连接
            connections = server.get_connection()
            to_del = []  # 即将删除的连接
            for userName in user_list:
                if user_list[userName] not in connections:
                    if _debug_:
                        print("[debug info]user %s is unused" % userName)
                    to_del.append(userName)
            for item in to_del:
                if _debug_:
                    print("[debug info]user %s is deleted" % item)
                user_list.pop(item)
        except Exception as e:
            print("[Error] : {e}", e)
