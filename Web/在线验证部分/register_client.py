from Web.SafeSocket import safeclient
import json


class RegClient(safeclient.SocketClient):
    def __init__(self, ip: str, port: int, heart_time: int = -1):
        super().__init__(ip, port)

    def get_check_code(self, username: str, email: str) -> str:
        """注册客户端对象获取验证码
        :参数：username: 用户名, email：邮箱
        :返回：服务器返回验证码
        """
        msg_opt1 = {
            "opt": 1,
            "user": username,
            "email": email
        }
        print(msg_opt1)
        super().send(json.dumps(msg_opt1))
        print("sent")
        check_code = super().receive()
        return check_code

    def send_all_information(self, username: str, email: str, password: str) -> bool:
        """注册客户端对象发送所有信息
        :参数：username: 用户名, email：邮箱, password：密码
        :返回：服务器返回结果
        """
        msg_opt2 = {
            "opt": 2,
            "user": username,
            "email": email,
            "password": password
        }
        print(msg_opt2)
        super().send(json.dumps(msg_opt2))
        print("sent")
        status = super().receive()
        if status == "WRONG":
            return False
        elif status == "close":
            return True
        else:
            print("ServerReturnError!")
            return False


if __name__ == "__main__":
    ip = "47.100.27.66"
    port = 25555
    client = RegClient(ip, port)
    username = input("Input your username: ")
    email = input("Input your email: ")
    check_code = client.get_check_code(username, email)
    input_check_code = input("Input the check_code in your mailbox: ")
    if check_code == input_check_code:
        password = input("Input your password: ")
        result = client.send_all_information(username, email, password)
        if result is True:
            print("Welcome to Fight Against Gravity!")
        else:
            print("Error! Try again later!")
