from Server.Modules import safeclient, OptType
import json
import os

OptType = OptType.OptType


class IdentifyClient:
    def __init__(self, reg_ip: str, reg_port: int,
                 game_ip: str, game_port: int,
                 password: str, heart_time: int = -1):
        """初始化
        :参数：reg_ip, reg_port：注册服务器与端口，game_ip, game_port：游戏服务器与端口, hear_time：心跳时间
        :返回：服务器返回验证码
        """
        self.__game_ip = game_ip
        self.__game_port = game_port
        self.__heart_beat = heart_time
        self.__reg_client = safeclient.SocketClient(reg_ip, reg_port, password=password, heart_beat=heart_time)

    def get_check_code(self, username: str, email: str) -> str:
        """验证客户端对象获取验证码
        :参数：username: 用户名, email：邮箱
        :返回：服务器返回验证码
        """
        msg_opt1 = {
            "opt": OptType.sendCheckCode,
            "user": username,
            "email": email
        }
        self.__reg_client.send(msg_opt1)
        check_code = self.__reg_client.receive()
        if check_code != "DUPLICATE" or check_code != "ERROR":
            return check_code
        else:
            return ""

    def send_all_information(self, username: str, email: str, password: str) -> bool:
        """验证客户端对象发送所有信息
        :参数：username: 用户名, email：邮箱, password：密码
        :返回：服务器返回结果
        """
        msg_opt2 = {
            "opt": OptType.sendAllInformation,
            "user": username,
            "email": email,
            "password": password
        }
        self.__reg_client.send(msg_opt2)
        status = self.__reg_client.receive()
        self.__reg_client.close()
        if status == "ERROR" or status == "DUPLICATE":
            return False
        elif status == "close":
            return True
        else:
            return False

    def reset_get_check_code(self, username: str, email: str) -> str:
        """验证客户端对象获取验证码
        :参数：username: 用户名, email：邮箱
        :返回：服务器返回验证码
        """
        msg_opt1 = {
            "opt": OptType.resetSendEmail,
            "user": username,
            "email": email
        }
        self.__reg_client.send(msg_opt1)
        check_code = self.__reg_client.receive()
        if check_code != "ERROR":
            return check_code
        else:
            return ""

    def reset_send_password(self, username: str, email: str, password: str) -> bool:
        """验证客户端对象发送所有信息
        :参数：username: 用户名, email：邮箱, password：密码
        :返回：服务器返回结果
        """
        msg_opt2 = {
            "opt": OptType.resetSendPassword,
            "user": username,
            "email": email,
            "password": password
        }
        self.__reg_client.send(msg_opt2)
        status = self.__reg_client.receive()
        self.__reg_client.close()
        if status == "ERROR":
            return False
        elif status == "close":
            return True
        else:
            return False

    def login(self, username: str, password: str) -> bool:
        """验证客户端登录函数
        :参数：username: 用户名, email：邮箱, password：密码
        :返回：服务器返回结果
        """
        game_client = safeclient.SocketClient(self.__game_ip, self.__game_port, heart_beat=self.__heart_beat)
        msg_opt = {
            "opt": OptType.login,
            "user": username,
            "password": password
        }
        game_client.send(msg_opt)
        status = game_client.receive()['status']
        game_client.close()
        if status == "ACK":
            return True
        else:
            return False


def createIdentifyClient() -> IdentifyClient:
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"
    with open(path + "settings/settings.json", "r") as f:
        information = json.load(f)
    reg_ip = information["Client"]["Reg_IP"]
    reg_port = information["Client"]["Reg_Port"]
    log_ip = information["Client"]["Game_Online_IP"]
    log_port = information["Client"]["Game_Online_Port"]
    password = information["AES_Key"]
    information = ""
    client = IdentifyClient(reg_ip, reg_port, log_ip, log_port, password=password)
    return client


if __name__ == "__main__":
    client = createIdentifyClient()
    choice = input("Input 'A' for login, 'B' for register, 'C' for reset password: ")
    username = input("Input your username: ")
    if choice in ['A', 'a']:
        password = input("Input your password: ")
        result = client.login(username, password)
        if result is True:
            print("Login successfully!")
        else:
            print("Error! Try again later!")
    elif choice in ['B', 'b']:
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
    else:
        email = input("Input your email: ")
        check_code = client.reset_get_check_code(username, email)
        print(check_code)
        if check_code != '':
            input_check_code = input("Input the check_code in your mailbox: ")
            if check_code.lower() == input_check_code.lower():
                password = input("Input your password: ")
                result = client.reset_send_password(username, email, password)
                if result is True:
                    print("Reset Successfully!")
                else:
                    print("Error! Try again later!")
            else:
                print("Error! Try again later!")
