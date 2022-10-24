from Web.SafeSocket import safeclient
from Web.SafeSocket import safeserver
import json


def check(user : str, password : str) -> bool:
    return True
    """
    假装去注册服务器 进行check
    """
    pass


if __name__ == "__main__":
    server = safeserver.SocketSever("localhost", "25555")
    server.start()
    while True:
        messages = server.get_message()
        for message in messages:
            rmessage = json.loads(message[0])
            """
            解码后的message
            """
            if rmessage["opt"] == 1:

            else:
                print("unexpected opt")
