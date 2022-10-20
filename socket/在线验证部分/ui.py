import tkinter as tk
from unittest import result
import ClientClass as cc
import tkinter.messagebox
import random
import sys
from PIL import Image, ImageDraw, ImageFont  # PIL模块中的Image,ImageDraw,ImageFont用于生成一张指定大小的验证码图片


def createCheckCode() -> str:  # 返回值char_check为
    '''生成本地验证码图片函数
    :参数：无参数
    :返回：对应图片中的字符串
    '''
    img1 = Image.new(mode="RGB", size=(140, 40), color=(50, 50, 40))  # 定义使用Image类实例化一个140px*40px,RGB(50,50,40)的图片
    draw1 = ImageDraw.Draw(img1, mode="RGB")  # 实例化一支画笔
    font1 = ImageFont.truetype("consolaz.ttf", 28)  # 定义要使用的字体
    char_check = ''
    for i in range(5):
        # 生成一个不包括0,o和O的字符
        char1 = random.choice([chr(random.randint(65, 78)), chr(random.randint(80, 90)), str(random.randint(1, 9)),
                               chr(random.randint(97, 110)), chr(random.randint(112, 122))])
        char_check += char1
        color1 = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))  # 每循环一次重新生成随机颜色
        draw1.text([i * 30, 0], char1, color1, font=font1)
        with open("pic.png", "wb") as f:  # 把生成的图片保存为本地目录下"pic.png"
            img1.save(f, format="png")
    return char_check

class UI_Register:
    def __init__(self, window : tk.Tk, client : cc.Client):
        # 定义长在窗口上的窗口
        self.__window_sign_up = tk.Toplevel(window)
        self.__window_sign_up.geometry('600x360')
        self.__window_sign_up.resizable(width=False, height=False)
        self.__window_sign_up.title('Fight Against Gravity')
        self.__client = client
        tk.Label(self.__window_sign_up, 
            text    = '注册Fight Against Gravity账户', 
            font    = ('Microsoft YaHei', 20)).place(x=120, y=20)

        self.__new_name = tk.StringVar()  # 将输入的注册名赋值给变量
        tk.Label(self.__window_sign_up, 
            text    = '用户名: ', 
            font    = ('Microsoft YaHei', 14)).place(x=90, y=80)
        self.__entry_new_name = tk.Entry(self.__window_sign_up, 
            font            = ('Microsoft YaHei', 14), 
            textvariable    = self.__new_name)
        self.__entry_new_name.place(x=210, y=80)

        self.__new_email = tk.StringVar()  # 将输入的邮箱赋值给变量
        tk.Label(self.__window_sign_up, 
            text    = '邮箱: ', 
            font    = ('Microsoft YaHei', 14)).place(x=90, y=120)
        self.__entry_new_email = tk.Entry(self.__window_sign_up, 
            font            = ('Microsoft YaHei', 14), 
            textvariable    = self.__new_email)
        self.__entry_new_email.place(x=210, y=120)

        self.__new_pwd = tk.StringVar()
        tk.Label(self.__window_sign_up, 
            text    = '密码: ', 
            font    = ('Microsoft YaHei', 14)).place(x=90, y=160)
        self.__entry_usr_pwd = tk.Entry(self.__window_sign_up, 
            font            = ('Microsoft YaHei', 14), 
            textvariable    = self.__new_pwd, 
            show            = '*')
        self.__entry_usr_pwd.place(x=210, y=160)

        self.__new_pwd_confirm = tk.StringVar()
        tk.Label(self.__window_sign_up, 
            text    = '确认密码: ', 
            font    = ('Microsoft YaHei', 14)).place(x=90, y=200)
        entry_usr_pwd_confirm = tk.Entry(self.__window_sign_up, 
        font            = ('Microsoft YaHei', 14), 
        textvariable    = self.__new_pwd_confirm,
        show            = '*')
        entry_usr_pwd_confirm.place(x=210, y=200)

        self.__check_code = tk.StringVar()
        tk.Label(self.__window_sign_up, 
            text    = '邮箱验证码: ', 
            font    = ('Microsoft YaHei', 14)).place(x=90, y=240)
        self.__entry_check_code = tk.Entry(self.__window_sign_up, 
            font            = ('Microsoft YaHei', 14), 
            textvariable    = self.__check_code)
        self.__entry_check_code.place(x=210, y=240)
        
        self.__btn_get_mail_code = tk.Button(self.__window_sign_up,
            text    = '获取', 
            height  = 1,
            font    = ('Microsoft YaHei', 14),
            relief  = 'groove', 
            command = self.get_email_code)
        self.__btn_get_mail_code.place(x=450, y=235)

        # 下面的注册和取消按钮
        self.__btn_comfirm_sign_up = tk.Button(self.__window_sign_up,
            text    = '注册', 
            width   = 14, 
            height  = 1, 
            font    = ('Microsoft YaHei', 14),
            relief  = 'groove', 
            command = self.sign_get)
        self.__btn_comfirm_sign_up.place(x=80, y=300)

        self.__btn_comfirm_cancel = tk.Button(self.__window_sign_up, 
            text    = '取消', 
            width   = 14, 
            height  = 1, 
            font    = ('Microsoft YaHei', 14),
            relief  = 'groove', 
            command = self.__window_sign_up.destroy)
        self.__btn_comfirm_cancel.place(x=320, y=300)
    
    def get_email_code(self) -> str:
        global check_code
        reg_acc = self.__new_name.get()
        reg_email = self.__new_email.get()
        check_code = str(self.__client.tcpClientGetCodes(reg_email, reg_acc), encoding='utf-8')

    def sign_get(self) -> bool:
        # 以下三行就是获取我们注册时所输入的信息
        reg_pas = self.__new_pwd.get()
        reg_pas_confirm = self.__new_pwd_confirm.get()
        reg_acc = self.__new_name.get()
        reg_email = self.__new_email.get()
        reg_check_code = self.__check_code.get()

        if reg_pas != '' and reg_pas_confirm != '' and reg_acc != '':
            # 这里就是判断，如果两次密码输入不一致，则报错
            if reg_pas == reg_pas_confirm:
                if reg_check_code == check_code:
                    result = self.__client.tcpClientRegister(reg_email, reg_acc, reg_pas)
                    if result:
                        tkinter.messagebox.showinfo("提示", '注册成功！欢迎加入Fight Against Gravity!')
                        self.__window_sign_up.destroy()
                    else:
                        tkinter.messagebox.showerror('错误', '注册失败！请稍后重试！')
                else:
                    tkinter.messagebox.showerror('错误', '验证码输入有误！')
            else:
                tkinter.messagebox.showerror('错误', '密码和重复密码必须保持一致!')

        else:
            tkinter.messagebox.showerror('错误', '注册选项卡不得留空！')

    def get_reg_pas(self) -> str:
        return self.__new_pwd.get()
    
    def get_reg_pas_confirm(self) -> str:
        return self.__new_pwd_confirm.get()

    def get_reg_acc(self) -> str:
        return self.__new_name.get()

    def get_reg_email(self) -> str:
        return self.__new_email.get()

    def show(self) -> None:
        self.__window_sign_up.mainloop()

class UI_Main:
    def __init__(self, title : str, register_host: str, register_port: int, login_host: str, login_port: int):
        self.__log_con = (False, '')
        self.__width = 600
        self.__height = 300
        self.__window = tk.Tk()
        self.__window.geometry(f'{self.__width}x{self.__height}')  
        # 这里的乘是小x
        self.__window.title('Fight Against Gravity')
        self.__window.resizable(width=False, height=False)

        self.__check_code = createCheckCode()
        self.__client = cc.Client(register_host, register_port, login_host, login_port)
        # 设置为不可伸缩
        tk.Label(self.__window, 
        text='Fight Against Gravity ', 
        font=('Microsoft YaHei', 20), 
        anchor='center').place(x=160, y=20)
        
        tk.Label(self.__window, 
            text='用户名：', 
            font=('Microsoft YaHei', 14)).place(x=70, y=100)
        
        tk.Label(self.__window, 
            text='密码：', 
            font=('Microsoft YaHei', 14)).place(x=70, y=140)
        
        tk.Label(self.__window, 
            text='验证码：', 
            font=('Microsoft YaHei', 14)).place(x=70, y=180)

        canvas = tk.Canvas(self.__window, 
            bg      = 'white', 
            height  = 40, 
            width   = 140)

        global image_file # 将image_file设置为全局变量避免被GC回收导致图片不显示
        image_file = tk.PhotoImage(file="pic.png")
        canvas.create_image(70, 20, anchor='center', image=image_file)  ####
        canvas.place(x=430, y=180)

        self.__var_usr_name = tk.StringVar()
        self.__entry_usr_name = tk.Entry(self.__window, 
            textvariable    = self.__var_usr_name, 
            font            = ('Microsoft YaHei', 14))

        self.__entry_usr_name.place(x=190, y=100)

        self.__var_usr_pwd = tk.StringVar()
        self.__entry_usr_pwd = tk.Entry(self.__window, 
            textvariable = self.__var_usr_pwd, 
            font         = ('Microsoft YaHei', 14), show='*')

        self.__entry_usr_pwd.place(x=190, y=140)

        self.__var_usr_check_code = tk.StringVar()
        self.__entry_usr_name = tk.Entry(self.__window, 
            textvariable    = self.__var_usr_check_code, 
            font            = ('Microsoft YaHei', 14))
        self.__entry_usr_name.place(x=190, y=180)

        self.__btn_login = tk.Button(self.__window, 
            text    = '登录', 
            font    = ('Microsoft YaHei', 12), 
            width   = 12, 
            height  = 1, 
            command = self.login_get)
        self.__btn_login.place(x=80, y=250)

        self.__btn_sign_up = tk.Button(self.__window, 
            text    = '注册', 
            font    = ('Microsoft YaHei', 12), 
            width   = 12, 
            height  = 1, 
            command = self.usr_sign_up)
        self.__btn_sign_up.place(x=220, y=250)

        self.__btn_cancel = tk.Button(self.__window, 
            text    = '退出', 
            font    = ('Microsoft YaHei', 12), 
            width   = 12, 
            height  = 1, 
            command = self.cancel)
        self.__btn_cancel.place(x=360, y=250)
    
    def show(self) -> None:
        self.__window.mainloop()

    def cancel(self) -> None:
        """UI窗口的析构函数
        :参数：无参数
        :返回：无返回
        """
        self.__window.destroy()
        self.__log_con = (False, '')

    def getLog_con(self) -> tuple:
        """获取经过UI的登录状态
        :参数：无参数
        :返回：返回登录状态和用户名的元组
        """
        return self.__log_con
    
    def getWindow(self) -> tk.Tk:
        """获取主界面窗口
        :参数：无参数
        :返回：返回主界面窗口对象
        """
        return self.__window
    
    def usr_sign_up(self):
        self.__sign_up_window = UI_Register(self.__window, self.__client)
        self.__sign_up_window.show()

        # 定义长在窗口上的窗口
    def login_get(self):
        pass
