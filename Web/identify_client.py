import Web.Modules.safeclient as safeclient
import Web.Modules.OptType as OptType
import json
import os

OptType = OptType.OptType

class IdentifyClient:
    def __init__(self, reg_ip: str, reg_port: int,
                 game_ip: str, game_port: int,
                 heart_time: int = -1):
        """初始化
        :参数：reg_ip, reg_port：注册服务器与端口，game_ip, game_port：游戏服务器与端口, hear_time：心跳时间
        :返回：服务器返回验证码
        """
        self.__reg_client = safeclient.SocketClient(reg_ip, reg_port)
        self.__game_client = safeclient.SocketClient(game_ip, game_port, heart_beat=5)

    def get_check_code(self, username: str, email: str) -> str:
        """验证客户端对象获取验证码
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
        if check_code != "DUPLICATE":
            return check_code
        else:
            print("Username or Email Duplicate Error!")
            return ""

    def send_all_information(self, username: str, email: str, password: str) -> bool:
        """验证客户端对象发送所有信息
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
        if status == "ERROR" or status == "DUPLICATE":
            return False
        elif status == "close":
            return True
        else:
            print("ServerReturnError!")
            return False

    def login(self, username: str, password: str) -> bool:
        """验证客户端登录函数
        :参数：username: 用户名, email：邮箱, password：密码
        :返回：服务器返回结果
        """
        msg_opt = {
            "opt": OptType.login,
            "user": username,
            "password": password
        }
        self.__game_client.send(json.dumps(msg_opt))
        status = self.__game_client.receive()['status']
        if status == "ACK":
            return True
        else:
            print(status)
            print("ServerReturnError!")
            return False

    def get_Game_Socket(self):
        """获取验证客户端中的游戏服务器socket"""
        return self.__game_client


def createIdentifyClient() -> IdentifyClient:
    current_path = os.getcwd()
    fag_directory = os.path.dirname(current_path)
    os.chdir(fag_directory)
    with open("Web/Modules/settings.json", "r") as f:
        information = json.load(f)
    reg_ip = information["Client"]["Reg_IP"]
    reg_port = information["Client"]["Reg_Port"]
    log_ip = information["Client"]["Game_IP"]
    log_port = information["Client"]["Game_Port"]
    information = ""
    client = IdentifyClient(reg_ip, reg_port, log_ip, log_port)
    return client

if __name__ == "__main__":
    client = createIdentifyClient()
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
        if check_code != '':
            input_check_code = input("Input the check_code in your mailbox: ")
            if check_code.lower() == input_check_code.lower():
                password = input("Input your password: ")
                result = client.send_all_information(username, email, password)
                if result is True:
                    print("Register Successfully!")
                else:
                    print("Error! Try again later!")
            else:
                print("Error! Try again later!")
