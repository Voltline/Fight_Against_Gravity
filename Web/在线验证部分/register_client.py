from Web.SafeSocket import safeclient
import json


class Client:
    def __init__(self, reg_ip: str, reg_port: int,
                 game_ip: str, game_port: int,
                 heart_time: int = -1):
        """初始化
        :参数：reg_ip, reg_port：注册服务器与端口，game_ip, game_port：游戏服务器与端口, hear_time：心跳时间
        :返回：服务器返回验证码
        """
        self.__reg_client = safeclient.SocketClient(reg_ip, reg_port)
        self.__log_client = safeclient.SocketClient(game_ip, game_port)

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
        self.__reg_client.send(json.dumps(msg_opt1))
        check_code = self.__reg_client.receive()
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
        self.__reg_client.send(json.dumps(msg_opt2))
        status = self.__reg_client.receive()
        if status == "WRONG":
            return False
        elif status == "close":
            return True
        else:
            print("ServerReturnError!")
            return False

    def login(self, username: str, password: str) -> bool:
        msg_opt = {
            "opt": 3,
            "user": username,
            "password": password
        }
        self.__log_client.send(json.dumps(msg_opt))
        status = self.__log_client.receive()
        if status == "WRONG":
            return False
        elif status == "close":
            return True
        else:
            print("ServerReturnError!")
            return False


if __name__ == "__main__":
    with open("settings.json", "r") as f:
        information = json.load(f)
    reg_ip = information["Client"]["Reg_IP"]
    reg_port = information["Client"]["Reg_Port"]
    log_ip = information["Client"]["Game_IP"]
    log_port = information["Client"]["Game_Port"]
    information = ""
    client = Client(reg_ip, reg_port, log_ip, log_port)
    choice = input("Input 'A' for login, 'B' for register: ")
    username = input("Input your username: ")
    if choice in ['A', 'a']:
        password = input("Input your password: ")
        result = client.login(username, password)
        if result is True:
            print("Login successfully!")
        else:
            print("Error! Try again later!")
    else:
        email = input("Input your email: ")
        check_code = client.get_check_code(username, email)
        input_check_code = input("Input the check_code in your mailbox: ")
        if check_code == input_check_code:
            password = input("Input your password: ")
            result = client.send_all_information(username, email, password)
            if result is True:
                print("Register Successfully!")
            else:
                print("Error! Try again later!")
