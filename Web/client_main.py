import Web.Modules.safeclient as safeclient
if __name__ == "__main__":
    client = safeclient.SocketClient("localhost", 25555, heart_beat=5)
    user = input("input the user name")
    password = input("input the pass word")
    msg = {
        "opt": 1,
        "user": user,
        "password": password
    }
    print(msg)
    client.send(msg)
    recvMsg = client.receive()
    if recvMsg["status"] == "ACK":
        print("ACK")
    else:
        print("NAK")
        print("登陆失败 请重新启动游戏")
        input("回车以继续")
        client.close()
        exit(0)
    while True:
        pass
