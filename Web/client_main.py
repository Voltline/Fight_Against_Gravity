import Web.Modules.safeclient as safeclient
# client_main暂时没有更新，请勿使用
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
    while True:
        pass
