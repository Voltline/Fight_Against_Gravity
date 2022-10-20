import aes
import socket
import random 
import tkinter as tk
import tkinter.messagebox
from time import ctime


class Client:
    def __init__(self, register_host : str, register_port : int, login_host : str, login_port : int):
        self.__register_host = register_host
        self.__register_port = register_port
        self.__addr_register = (self.__register_host, self.__register_port)

        self.__login_host = login_host
        self.__login_port = login_port
        self.__addr_login = (self.__login_host, self.__login_port)

        self.__encoding = 'utf-8'
        self.__buffsize = 1024

        self.__aes_password = b''

        try:
            with open("password.txt", 'r') as f:
                self.__local_password = bytes(f.read(), encoding='utf-8')
                f.close()
        except:
            tkinter.messagebox.showerror("错误！","客户端启动异常，请联系管理员")
            raise("客户端启动异常，请联系管理员")

    def tcpClientSend(self, Type : bool,  Data : bytes) -> str:
        '''向tcp服务器发送信息 

        :参数：Data: bytes类型内容，Type：True为注册，False为登录
        :返回：服务器返回结果
        '''
        if Type:
            ADDR = self.__addr_register
        else:
            ADDR = self.__addr_login  
        ans = ""
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
            # 尝试连接服务器
            try:
                s.connect(ADDR)
                s.send(Data)
                # 接收返回数据
                outData = s.recv(self.__buffsize)
                ans = outData
                # 关闭客户端套接字
                s.close()
            except:
                tkinter.messagebox.showerror("错误！","服务器连接异常，请重启程序")
        return ans

    def tcpClientInitPW(self, Type : bool) -> None:
        aes_password = aes.generate_id_code() # 产生随机十六位密钥
        aes_password_upload = aes.aes_encrypt(self.__local_password, aes_password) # 用于上传的密钥
        aes_password = bytes(aes_password, 'utf-8') # 本地用的密钥
        self.tcpClientSend(Type, aes_password_upload) # 将加密后的密钥传出
        self.__aes_password = aes_password


    def tcpClientGetCodes(self, email : str, user_name : str) -> str:
        '''tcp客户端获取验证码操作
        :参数：email：邮箱, user_name：用户名
        :返回：验证码
        '''
        self.tcpClientInitPW(True)
        # try:
        result = self.tcpClientSend(True, aes.aes_encrypt(self.__aes_password, f'["{user_name}","{email}"]'))
        tkinter.messagebox.showinfo("提示", "已经向您发送了验证码！请注意查收")
        return result
        # except:
        #     tkinter.messagebox.showerror("错误！","验证码发送失败！请再次尝试")

    def tcpClientRegister(self, email : str, user_name : str, password : str) -> bool:
        '''tcp客户端注册操作
        :参数：email：邮箱, user_name：用户名, password：密码
        :返回：注册结果
        '''
        result = self.tcpClientSend(True, aes.aes_encrypt(self.__aes_password, f'["{user_name}","{password}","{ctime()}","{email}"]'))
        if eval(result):
            tkinter.messagebox.showinfo("提示", f"{user_name}，您的账户注册成功！")
            return True
        else:
            return False
    