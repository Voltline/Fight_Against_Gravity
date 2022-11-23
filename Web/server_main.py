import Web.Modules.safeserver as safeserver
import Web.Modules.safeclient as safeclient
import json


def check(user: str, password: str) -> bool:
    """
    真的去注册服务器 进行check
    """
    with open("Modules/settings.json", 'r') as f:
        information = json.load(f)
    print("checking2")
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
    print(msg)
    status = check_client.receive()
    check_client.close()
    print(status)
    if status == "ERROR":
        return False
    elif status == "close":
        return True
    else:
        print("ServerReturnError!")
        return False


user_list = []  # {"username" : address}
if __name__ == "__main__":
    server = safeserver.SocketSever("127.0.0.1", 25555, heart_time=5, debug=1)
    server.start()
    while True:
        try:
            # 处理消息队列
            messages = server.get_message()
            # print(1)
            for message in messages:
                print(message)
                messageAdr, messageMsg = message
                """
                解码后的message
                """
                if messageMsg["opt"] == 1:
                    print("checking")
                    if check(messageMsg["user"], messageMsg["password"]):
                        user_list.append({messageMsg["user"]: messageAdr})
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
        except Exception as e:
            print("[Error] : {e}", e)
