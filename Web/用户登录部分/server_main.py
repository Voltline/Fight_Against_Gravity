from Web.SafeSocket import safeclient
from Web.SafeSocket import safeserver
import json
import time


def check(user: str, password: str) -> bool:
    """
    真的去注册服务器 进行check
    """
    with open("settings.json", 'r') as f:
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
    check_client.send(json.dumps(msg))
    status = check_client.receive()
    check_client.close()
    if status == "ERROR":
        return False
    elif status == "close":
        return True
    else:
        print("ServerReturnError!")
        return False


user_list = []  # {"username" : address}
if __name__ == "__main__":
    _debug_ = 1
    server = safeserver.SocketSever("", 25555)
    server.start()
    sttm = time.time()
    while True:
        if time.time() - sttm > 4:
            print(user_list)
            sttm = time.time()
        # 处理消息队列
        messages = server.get_message()
        for message in messages:
            rmessage = json.loads(message[1])
            """
            解码后的message
            """
            if rmessage["opt"] == 3:
                if check(rmessage["user"], rmessage["password"]):
                    user_list.append({rmessage["user"]: message[0]})
                    server.send(message[0], "ACCEPT")
                else:
                    server.close(message[0])
            else:
                print("unexpected opt")
        # 处理超时链接
        get_user_list = server.get_message()
