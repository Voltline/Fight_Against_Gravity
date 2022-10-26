from Web.SafeSocket import safeclient
from Web.SafeSocket import safeserver
import json
import time


def check(user: str, password: str) -> bool:
    """
    假装去注册服务器 进行check
    """
    return True


user_list = []  # {"username" : address}
if __name__ == "__main__":
    _debug_ = 1
    server = safeserver.SocketSever("localhost", 25555)
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
            if rmessage["opt"] == 1:
                if check(rmessage["user"], rmessage["password"]):
                    user_list.append({rmessage["user"]: message[0]})
                else:
                    server.close(message[0])
            else:
                print("unexpected opt")
        # 处理超时链接
        get_user_list = server.get_message()
