import os
import sys

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"
sys.path.append(path)
from threading import Thread
from Server.Modules import safeserver, database_operate, send_email, OptType
from Server.Modules.Flogger import Flogger
import json
import time

OptType = OptType.OptType
email_sent = {}
reset_sent = {}
user_list = []  # {"username" : address}


class IdentifyServer:
    def __init__(self, ip: str, port: int, password: str, heart_time: int = -1, debug: bool = False):
        """注册服务器初始化
        :参数: ip: 服务器ip， port: 端口， heart_time: 心跳时间（默认-1），debug: 调试模式
        :返回: 无返回
        """
        self.accept_thread = None
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

    def reset_send_email_opt(self, username: str, email: str, addr: tuple):
        """重置密码发送验证码操作
        :参数: username：用户名，email：邮箱，addr：地址元组
        :返回: 无返回
        """
        check = database_operate.check_match([username, email])
        if check:
            reset_sent[(username, email)] = True
            id_code = send_email.generate_id_code()
            send_ans = send_email.send_email(username, email, id_code, 1)
            if send_ans:
                self.server.send(addr, id_code)
            else:
                self.server.send(addr, "ERROR")
        else:
            self.server.send(addr, "ERROR")

    def reset_confirm_opt(self, username: str, email: str, rmessage: dict, addr: tuple):
        """接受并写入数据库操作
        :参数: username：用户名，email：邮箱，rmessage：传入的各种信息字典，addr：地址元组
        :返回: 无返回
        """
        if (username, email) in reset_sent:
            password = rmessage["password"]
            time_n = time.ctime()
            database_operate.reset_password_data([password, username])
            reset_sent.pop((username, email))
        else:
            self.server.send(addr, "ERROR")
        self.server.close(addr)

    def console(self):
        all_cmd_list = ['ls', 'find', 'check', 'help', 'clear']
        help_script = """Identify Server 控制台帮助文档
* 目前已支持指令：ls   find   check   help   clear
* 所有指令会根据参数数量按顺序提取，多余的会被丢弃
基本用法：
*| ls [no_args]
    作用: 无参数，列出所有用户信息
    例如: ls
*| find [arg]
    作用: 了解用户名是否已注册
    例如: ls username
*| check [arg1] [arg2]
    作用: 检测用户名与密码是否匹配
    例如: check username password
*| help [no_args]
    作用: 帮助
    例如: help
*| clear [no_args]
    作用: 清除后台内容
    例如: clear
"""

        def console_help():
            print(help_script)

        def console_ls():
            self.all_reg_acc = database_operate.get_all_reg_acc()
            print(f"{'账户':18}{'密码':28}邮箱")
            for key, value_list in self.all_reg_acc.items():
                print(f"{key:20}{value_list[0]:30}{value_list[1]}")
            print("---------------------------------")

        def console_find(cmd_lst: list) -> bool:
            if len(cmd_lst) >= 2:
                self.all_reg_acc = database_operate.get_all_reg_acc()
                if cmd_lst[1] in self.all_reg_acc:
                    print(f"用户{cmd_list[1]}为已注册用户！")
                else:
                    print(f"用户{cmd_list[1]}尚不存在！")
                return True
            else:
                return False

        def console_check(cmd_lst: list) -> bool:
            if len(cmd_list) >= 3:
                self.all_reg_acc = database_operate.get_all_reg_acc()
                usr, pwd = cmd_list[1], cmd_list[2]
                if usr in self.all_reg_acc and self.all_reg_acc[usr][0] == pwd:
                    print(f"用户{cmd_list[1]}验证成功！")
                else:
                    print(f"用户{cmd_list[1]}验证失败！")
                return True
            else:
                return False

        def console_clear():
            if sys.platform == 'linux' or sys.platform == 'darwin':
                os.system('clear')
            elif sys.platform == 'win32':
                os.system('cls')
            else:
                print("抱歉，暂时没有适配您的系统！")

        while True:
            ans = True
            cmd = input()
            if cmd != "":
                if len(cmd) <= 1000:
                    cmd_list = cmd.split()
                    cmd_key = cmd_list[0].strip(' ')
                    if cmd_key in all_cmd_list:
                        if cmd_key == 'ls':
                            console_ls()
                        elif cmd_key == 'find':
                            ans = console_find(cmd_list)
                        elif cmd_key == 'help':
                            console_help()
                        elif cmd_key == 'check':
                            ans = console_check(cmd_list)
                        elif cmd_key == 'clear':
                            console_clear()
                    else:
                        ans = False
                else:
                    print("指令长度太长！请重新输入！")

            if not ans:
                print("指令输入有误/操作失败！请重新输入！")

    def start(self):
        self.accept_thread = Thread(target=self.console)
        self.accept_thread.setDaemon(True)
        self.accept_thread.setName("Console_thread")
        self.accept_thread.start()
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
                    if rmessage["opt"] == OptType.resetSendEmail or rmessage["opt"] == OptType.resetSendPassword:
                        if rmessage["opt"] == OptType.resetSendEmail:
                            self.reset_send_email_opt(username,  email, addr)
                        elif rmessage["opt"] == OptType.resetSendPassword:
                            self.reset_confirm_opt(username, email, rmessage, addr)
                    else:
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
