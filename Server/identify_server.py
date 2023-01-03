import os
import sys

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"
sys.path.append(path)
from Server.Modules import safeserver, database_operate, send_email, OptType
from Server.Modules.Flogger import Flogger
import json
import time

OptType = OptType.OptType
email_sent = {}
user_list = []  # {"username" : address}


class IdentifyServer:
    def __init__(self, ip: str, port: int, password: str, heart_time: int = -1, debug: bool = False):
        """注册服务器初始化
        :参数: ip: 服务器ip， port: 端口， heart_time: 心跳时间（默认-1），debug: 调试模式
        :返回: 无返回
        """
        self.all_reg_acc = database_operate.get_all_reg_acc()  # 服务器对象内置所有账户的字典
        self.server = safeserver.SocketServer(ip, port, heart_time, debug, password=password,
                                              models=Flogger.FILE,
                                              logpath=path, level=Flogger.L_INFO)
        self.logger = Flogger(models=Flogger.FILE_AND_CONSOLE, level=Flogger.L_INFO,
                              folder_name="identify_server", logpath=path)

    def sendCheckCode_opt(self, username: str, email: str, addr: tuple):
        """发送验证码操作
        :参数: username：用户名，email：邮箱，addr：地址元组
        :返回: 无返回
        """
        email_sent[(username, email)] = True
        id_code = send_email.generate_id_code()
        send_ans = send_email.send_email(username, email, id_code)
        if send_ans:
            self.server.send(addr, id_code)
        else:
            self.server.send(addr, "ERROR")

    def register_opt(self, username: str, email: str, rmessage: dict, addr: tuple):
        """接受并写入数据库操作
        :参数: username：用户名，email：邮箱，rmessage：传入的各种信息字典，addr：地址元组
        :返回: 无返回
        """
        if (username, email) in email_sent:
            password = rmessage["password"]
            time_n = time.ctime()
            database_operate.insert_acc_data([username, password, time_n, email])
            email_sent.pop((username, email))
        else:
            self.server.send(addr, "ERROR")
        self.server.close(addr)

    def login_opt(self, rmessage: dict, addr: tuple):
        """登录时的服务器操作
        :参数: rmessage：传入的各种信息元组，addr：地址元组
        :返回: 无返回
        """
        username = rmessage["user"]
        password = rmessage["password"]
        self.all_reg_acc = database_operate.get_all_reg_acc()  # 每次调用前完成一次获取操作
        if username in self.all_reg_acc:
            if password == self.all_reg_acc[username][0]:
                database_operate.insert_login_data([username, time.ctime()])
            else:
                self.server.send(addr, "ERROR")
        else:
            self.server.send(addr, "ERROR")
        self.server.close(addr)

    def start(self):
        while True:
            messages = self.server.get_message()
            for message in messages:
                self.logger.info(f"[Msg In]{time.ctime()} : {message}")
                addr = message[0]  # addr : client's address
                rmessage = message[1]
                user_list.append({rmessage["user"]: message[0]})
                all_reg_acc = database_operate.get_all_reg_acc()
                if rmessage["opt"] != OptType.loginTransfer:
                    username, email = rmessage["user"], rmessage["email"]
                    if database_operate.check_duplicate(username):
                        self.logger.info(f"[ERROR]user {username} Duplicate Error")
                        self.server.send(addr, "DUPLICATE")
                    else:
                        if rmessage["opt"] == OptType.sendCheckCode:
                            self.sendCheckCode_opt(username, email, addr)
                        elif rmessage["opt"] == OptType.sendAllInformation:
                            self.register_opt(username, email, rmessage, addr)
                        else:
                            self.logger.info("[ERROR]Unexpected Opt")
                else:
                    self.login_opt(rmessage, addr)


if __name__ == "__main__":
    _debug_ = "--debug" in sys.argv
    _local_ = "--local" in sys.argv
    if _local_:
        with open(path + "settings/settings_local.json", 'r') as f:
            information = json.load(f)
    else:
        with open(path + "settings/settings.json", 'r') as f:
            information = json.load(f)

    ip = ""
    port = information["Client"]["Reg_Port"]
    password = information["AES_Key"]
    try:
        server = IdentifyServer(ip, port, debug=_debug_, password=password)
        server.start()
    except Exception as e:
        print(f"[Error] {time.ctime()} : {e}")
