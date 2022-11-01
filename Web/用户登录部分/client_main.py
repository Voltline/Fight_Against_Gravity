from Web.SafeSocket import safeclient
import json

if __name__ == "__main__":
    client = safeclient.SocketClient("localhost", 25555)
    user = input("input the user name")
    password = input("input the pass word")
    msg = {
        "opt": 1,
        "user": user,
        "password": password
    }
    client.send(json.dumps(msg))
    print(json.dumps(msg))
    print(type(json.dumps(msg)))
    while True:
        pass
