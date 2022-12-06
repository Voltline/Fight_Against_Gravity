import pygame
from InputBox_Class import InputBox
from Button_Class import Button
from Label_Class import Label
import sys
import os
from Web import identify_client as ic
from all_settings import Settings


class UI:

    def __init__(self):
        pygame.init()
        self.page_status = 0
        self.UI_current_directory = os.getcwd()  # UI文件夹路径
        self.fag_directory = os.path.dirname(self.UI_current_directory)  # FAG文件夹路径
        self.font_path_light = "UI/Font/SourceHanSans-Light.ttc"
        self.font_path_normal = "UI/Font/SourceHanSans-Normal.ttc"
        self.btbg_light = "UI/Img/light_butbg_unpressed.png"  # 按钮浅灰底，未按版
        self.btbg_light_pressed = "UI/Img/light_butbg.png"  # 鼠标移动反响
        os.chdir(self.fag_directory)
        self.log_font = {
            'font': pygame.font.Font(self.font_path_normal, 22),
            'tc': (36, 41, 47),
            'bc': None,
            'align': 1,
            'valign': 1
        }  # 黑字用于白底
        self.r_font = {
            'font': pygame.font.Font(self.font_path_normal, 16),
            'tc': (169, 183, 198),
            'bc': None,
            'align': 0,
            'valign': 0
        }  # 白字用于黑底
        self.menu_font = {
            'font': pygame.font.Font(self.font_path_normal, 60),
            'tc': (36, 41, 47),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        self.switcher = 0
        self.START = pygame.USEREVENT + 1
        self.BACK = pygame.USEREVENT + 2
        self.REGISTER = pygame.USEREVENT + 3
        self.SENDREGISTER = pygame.USEREVENT + 4
        self.LOGIN = pygame.USEREVENT + 5
        self.SENDCHECK = pygame.USEREVENT + 6
        self.LOCAL = pygame.USEREVENT + 7
        self.ONLINE = pygame.USEREVENT + 8
        self.SETTING = pygame.USEREVENT + 9
        # CONFIRM = pygame.USEREVENT + 7

    def load_start(self):
        """准备开始界面的组件, 对应页面状态 0"""
        os.chdir(self.fag_directory)
        start_font = {
            'font': pygame.font.Font(self.font_path_light, 65),
            'tc': (36, 41, 47),
            'bc': None,
            'align': 1,
            'valign': 1
        }
        start_rect = pygame.Rect(455, 300, 290, 100)
        start_title = pygame.image.load("assets/texture/FAGtitle.png")
        start_title = pygame.transform.smoothscale(start_title, (514, 200))
        start_title = start_title.convert_alpha()

        start = Button("start", self.START, start_rect, "UI/Img/start_unpressed.png", 1, 'Start', start_font)
        start.add_img("UI/Img/start_press.png")
        return {'img': start_title, 'label': None, 'box': None, 'button': [start]}

    def load_login(self):
        """加载登录界面组件, 对应页面状态1"""
        """登录界面"""
        os.chdir(self.fag_directory)
        id_label = Label(330, 250, 98, "账号(用户名)")
        password_label = Label(330, 350, 42, "密码")
        id_box = InputBox(pygame.Rect(450, 250, 350, 35))  # 输入框的宽不由传入参数决定。
        password_box = InputBox(pygame.Rect(450, 350, 350, 35), is_pw=1)
        boxL = [id_box, password_box]
        """注册按钮"""
        register_rect = pygame.Rect(600, 450, 180, 40)
        register_button = Button("register", self.REGISTER, register_rect, self.btbg_light, 0, '没有账号?注册',
                                 self.log_font)
        register_button.add_img(self.btbg_light_pressed)
        """登录按钮"""
        login_rect = pygame.Rect(450, 450, 70, 40)
        login_button = Button("login", self.LOGIN, login_rect, self.btbg_light, 0, "登录", self.log_font)
        login_button.add_img(self.btbg_light_pressed)
        return {'label': [id_label, password_label], 'box': boxL, 'button': [register_button, login_button]}

    def load_register(self):
        """加载注册组件"""
        os.chdir(self.fag_directory)
        r_email_label = Label(315, 180, 98, "请输入您的邮箱", self.r_font)
        r_id_label = Label(315, 260, 106, "请输入您的用户名", self.r_font)
        r_password_label = Label(315, 340, 42, "设置您的密码", self.r_font)
        r_check_label = Label(315, 420, 40, "验证码", self.r_font)
        labels = [r_email_label, r_id_label, r_password_label, r_check_label]

        r_email_box = InputBox(pygame.Rect(450, 180, 350, 35))
        r_id_box = InputBox(pygame.Rect(450, 260, 350, 35))
        r_password_box = InputBox(pygame.Rect(450, 340, 350, 35))
        r_check_box = InputBox(pygame.Rect(450, 420, 350, 35))
        boxes = [r_email_box, r_id_box, r_password_box, r_check_box]

        r_rect = pygame.Rect(650, 500, 100, 40)
        r_button = Button("r", self.SENDREGISTER, r_rect, self.btbg_light, 0, '确认注册', self.log_font)
        r_button.add_img(self.btbg_light_pressed)
        check_rect = pygame.Rect(430, 500, 110, 40)
        r_check_button = Button('check', self.SENDCHECK, check_rect, self.btbg_light, 0, '发送验证码', self.log_font)
        r_check_button.add_img(self.btbg_light_pressed)
        buttons = [r_button, r_check_button]
        return {'label': labels, 'box': boxes, 'button': buttons}

    def load_menu(self):
        """点击登录之后进入游戏主菜单"""
        os.chdir(self.fag_directory)
        labels = None
        boxes = None

        menu_local_rect = pygame.Rect(455, 200, 290, 80)
        menu_local_button = Button('local game', self.LOCAL, menu_local_rect,
                                   self.btbg_light, 0, '本地游戏', self.menu_font)
        menu_online_rect = pygame.Rect(455, 360, 290, 80)
        menu_online_button = Button('online game', self.ONLINE, menu_online_rect,
                                    self.btbg_light, 0, '线上房间', self.menu_font)
        menu_local_button.add_img(self.btbg_light_pressed)
        menu_online_button.add_img(self.btbg_light_pressed)
        buttons = [menu_local_button, menu_online_button]
        return {'label': labels, 'box': boxes, 'button': buttons}

    def update_event(self, loaded, e):
        """将对应页面加载了的组件全部进行状态更新，会post新的event"""
        if loaded['button'] is not None:
            for bt in loaded['button']:
                bt.update(e)
        if loaded['box'] is not None:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    loaded['box'][self.switcher].active = False
                    self.switcher = (self.switcher + 1) % len(loaded['box'])
                    loaded['box'][self.switcher].active = True
            for bx in loaded['box']:
                bx.deal_event(e)

    def draw_elements(self, loaded, surface):
        if loaded['button'] is not None:
            for bt in loaded['button']:
                bt.render(surface)
        if loaded['label'] is not None:
            for lb in loaded['label']:
                lb.render(surface)
        if loaded['box'] is not None:
            for bx in loaded['box']:
                bx.draw(surface)

    def bt_color_switch(self, loaded, e):
        """把对应页面内加载出来的组件中的按钮添加颜色变化响应"""
        if loaded['button'] is not None:
            for bt in loaded['button']:
                bt.check_move(e)

    def hide_bt(self, loaded):
        """让页面内的所有按钮失效隐藏"""
        if loaded['button'] is not None:
            for bt in loaded['button']:
                bt.hide()
                print("clicked", bt.name)
                bt.disable()

    def show_bt(self, loaded):
        """在返回上一界面时，要让上一界面所有按钮重新激活显示"""
        if loaded['button'] is not None:
            for bt in loaded['button']:
                bt.show()
                bt.enable()

    def createPage(self):
        pygame.init()
        running = True
        screen = pygame.display.set_mode((1200, 800))
        elements_1 = self.load_start()  # 开始界面的
        elements_2 = self.load_login()  # 登录界面
        elements_3 = self.load_register()  # 注册界面
        elements_4 = self.load_menu()  # 主界面
        os.chdir(self.UI_current_directory)
        """与客户端交流的组件"""
        check_code = ''
        identify_client = ic.createIdentifyClient()
        """全局组件，返回按钮和设置按钮"""
        back_rect = pygame.Rect(20, 20, 45, 45)
        back = Button("back", self.BACK, back_rect, "UI/Img/back.png", 1)

        set_rect = pygame.Rect(1050, 700, 60, 60)
        set_button = Button('setting', self.SETTING, set_rect, "UI/Img/setting_light.png", 1)
        set_button.add_img("UI/Img/setting_light_pressed.png")
        """
        单个按钮状态切换使用update以及check_move
        对于页面组件按钮状态切换使用update_event和bt_color_switch
        """
        while running:
            """背景"""
            if self.page_status == 0:
                screen.fill((255, 255, 255))
            else:
                screen.fill((10, 10, 10))
            """事件处理"""
            for event in pygame.event.get():
                if self.page_status == 0:
                    self.update_event(elements_1, event)  # 事件处理
                    self.bt_color_switch(elements_1, event)
                    if event.type == self.START:
                        self.hide_bt(elements_1)
                        self.page_status += 1
                elif self.page_status == 1:
                    back.update(event)
                    set_button.update(event)
                    set_button.check_move(event)
                    self.update_event(elements_2, event)
                    self.bt_color_switch(elements_2, event)
                    if event.type == self.BACK:
                        self.show_bt(elements_1)
                        self.page_status -= 1
                    elif event.type == self.REGISTER:
                        self.page_status += 1
                        self.switcher = 0  # 重置输入框Switch
                        self.hide_bt(elements_2)
                        self.show_bt(elements_3)
                    elif event.type == self.LOGIN:
                        userid = elements_2['box'][0].text
                        userpw = elements_2['box'][1].text
                        answer = identify_client.login(userid, userpw)
                        if answer:
                            print("登录成功")
                            self.hide_bt(elements_2)
                            self.page_status = 3  # 转到游戏主界面
                        else:
                            print("failed")
                elif self.page_status == 2:
                    back.update(event)
                    self.bt_color_switch(elements_3, event)
                    self.update_event(elements_3, event)
                    if event.type == self.BACK:
                        self.page_status -= 1
                        self.switcher = 0  # 重置输入框Switch
                        self.hide_bt(elements_3)
                        self.show_bt(elements_2)
                    elif event.type == self.SENDREGISTER:
                        print(check_code + '\n' + elements_3['box'][3].text)
                        if check_code != '':
                            if check_code.lower() == elements_3['box'][3].text.lower():
                                result = identify_client.send_all_information(elements_3['box'][1].text,
                                                                              elements_3['box'][0].text,
                                                                              elements_3['box'][2].text)
                                if result:
                                    print('成功')
                                else:
                                    print("注册失败")
                                    print(elements_3['box'][1].text +
                                          '\n' + elements_3['box'][0].text,
                                          '\n' + elements_3['box'][2].text)
                                    self.page_status -= 1
                        # ic.send_all_information(r_email_box.text, r_id_box.text, r_password_box.text)
                    elif event.type == self.SENDCHECK:  # 发送验证码
                        username = elements_3['box'][1].text
                        print(username)
                        email = elements_3['box'][0].text
                        check_code = identify_client.get_check_code(username, email)
                elif self.page_status == 3:
                    back.update(event)
                    self.update_event(elements_4, event)
                    self.bt_color_switch(elements_4, event)
                    if event.type == self.BACK:
                        self.hide_bt(elements_4)
                        self.show_bt(elements_2)
                        self.page_status = 1
                    elif event.type == self.LOCAL:
                        os.chdir(self.fag_directory)
                        pygame.quit()
                        os.system('main.py')
                        running = False
                if event.type == pygame.QUIT:  # 要加一个client的析构
                    running = False
                    pygame.quit()
                    sys.exit()
            if self.page_status == 0:
                screen.blit(elements_1['img'], (10, 10))
                self.draw_elements(elements_1, screen)
            elif self.page_status == 1:
                pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
                self.draw_elements(elements_2, screen)
                back.render(screen)
                set_button.render(screen)
            elif self.page_status == 2:
                pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
                back.render(screen)
                self.draw_elements(elements_3, screen)
            elif self.page_status == 3:
                pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
                back.render(screen)
                self.draw_elements(elements_4, screen)
            # setting.render(screen)
            pygame.display.flip()


page_manager = UI()
page_manager.createPage()


# """页面状态"""
# page_status = 0
#
# """自定义事件"""
# START = pygame.USEREVENT + 1
# BACK = pygame.USEREVENT + 2
# REGISTER = pygame.USEREVENT + 3
# SENDREGISTER = pygame.USEREVENT + 4
# LOGIN = pygame.USEREVENT + 5
# SENDCHECK = pygame.USEREVENT + 6
# # CONFIRM = pygame.USEREVENT + 7
# SET = pygame.USEREVENT + 8
# """文件资源操作"""
# current_work_directory = os.getcwd()  # 当前路径
# print(current_work_directory)
# fag_directory = os.path.dirname(current_work_directory)  # 上级路径
# print(fag_directory)
# os.chdir(fag_directory)
# settings = Settings()
# pygame.init()
# screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
# os.chdir(current_work_directory)
# """开始游戏界面配置"""
# start_font = {
#     'font': pygame.font.Font("Font/SourceHanSans-Light.ttc", 65),
#     'tc': (36, 41, 47),
#     'bc': None,
#     'align': 1,
#     'valign': 1
# }
# start_rect = pygame.Rect(455, 300, 290, 100)
#
# os.chdir(fag_directory)
# start_title = pygame.image.load("assets/texture/FAGtitle.png")
# start_title = pygame.transform.smoothscale(start_title, (514, 200))
# start_title = start_title.convert_alpha()
#
# os.chdir(current_work_directory)
# start = Button("start", START, start_rect, "Img/start_unpressed.png", 1, 'Start', start_font)
# start.add_img("Img/start_press.png")
#
# """返回按钮"""
# back_rect = pygame.Rect(20, 20, 45, 45)
# back = Button("back", BACK, back_rect, "Img/back.png", 1)
#
# """设置按钮"""
# setting_rect = pygame.Rect(1100, 750, 48, 48)
# setting = Button("setting", SET, setting_rect, "Img/setting_dark.png", 1)
# """登录界面"""
# id_label = Label(330, 250, 98, "账号(用户名)")
# password_label = Label(330, 350, 42, "密码")
# id_box = InputBox(pygame.Rect(450, 250, 350, 35))  # 输入框的宽不由传入参数决定。
# password_box = InputBox(pygame.Rect(450, 350, 350, 35))
# boxL = [id_box, password_box]
# """注册按钮"""
# register_rect = pygame.Rect(600, 450, 180, 40)
# register_font = {
#                 'font': pygame.font.Font("Font/SourceHanSans-Normal.ttc", 22),
#                 'tc': (36, 41, 47),
#                 'bc': None,
#                 'align': 1,
#                 'valign': 1
#             }
# register_button = Button("register", REGISTER, register_rect, "Img/light_butbg.png", 0, '没有账号?注册', register_font)
# """登录按钮"""
# login_rect = pygame.Rect(450, 450, 70, 40)
# login_button = Button("login", LOGIN, login_rect, "Img/light_butbg.png", 0, "登录", register_font)
# """注册界面"""
# r_font = {
#             'font': pygame.font.Font("Font/SourceHanSans-Normal.ttc", 16),
#             'tc': (169, 183, 198),
#             'bc': None,
#             'align': 0,
#             'valign': 0
#             }
# r_email_label = Label(315, 180, 98, "请输入您的邮箱", r_font)
# r_id_label = Label(315, 260, 106, "请输入您的用户名", r_font)
# r_password_label = Label(315, 340, 42, "设置您的密码", r_font)
# r_check_label = Label(315, 420, 40, "验证码", r_font)
#
# r_email_box = InputBox(pygame.Rect(450, 180, 350, 35))
# r_id_box = InputBox(pygame.Rect(450, 260, 350, 35))
# r_password_box = InputBox(pygame.Rect(450, 340, 350, 35))
# r_check_box = InputBox(pygame.Rect(450, 420, 350, 35))
#
# r_rect = pygame.Rect(650, 500, 100, 40)
# r_button = Button("r", SENDREGISTER, r_rect, "Img/light_butbg.png", 0, '确认注册', register_font)
# check_rect = pygame.Rect(430, 500, 110, 40)
# r_check_button = Button('check', SENDCHECK, check_rect, "Img/light_butbg.png", 0, '发送验证码', register_font)
#
# # confirm_rect = pygame.Rect(430, 500, 80, 40)
# # confirm_button = Button('confirm', CONFIRM, confirm_rect, "Img/light_butbg.png", 0, '确认', register_font)
# """注册测试"""
# check_code = ''
# identify_client = ic.createIdentifyClient()
# running = True
# while running:
#     if page_status == 0:
#         screen.fill((255, 255, 255))
#     else:
#         screen.fill((10, 10, 10))
#     for event in pygame.event.get():
#         if page_status == 0:  # 开始界面
#             start.update(event)
#             start.check_move(event)
#             if event.type == START:
#                 start.hide()
#                 print("clicked Start")
#                 start.disable()
#                 page_status += 1
#         elif page_status == 1:
#             id_box.deal_event(event)
#             password_box.deal_event(event)
#             back.update(event)
#             register_button.update(event)
#             login_button.update(event)
#             if event.type == BACK:
#                 start.show()
#                 start.enable()
#                 page_status -= 1
#             elif event.type == REGISTER:
#                 page_status += 1
#                 register_button.hide()
#                 register_button.disable()
#                 login_button.hide()
#                 login_button.disable()
#                 r_check_button.show()
#                 r_check_button.enable()
#             elif event.type == LOGIN:
#                 userid = id_box.text
#                 userpw = password_box.text
#                 answer = identify_client.login(userid, userpw)
#                 if answer:
#                     print("登录成功")
#                 else:
#                     print("failed")
#
#         elif page_status == 2:
#             back.update(event)
#             r_email_box.deal_event(event)
#             r_id_box.deal_event(event)
#             r_password_box.deal_event(event)
#             r_check_box.deal_event(event)
#             r_button.update(event)
#             r_check_button.update(event)
#             if event.type == BACK:
#                 page_status -= 1
#                 r_check_button.hide()
#                 r_check_button.disable()
#                 register_button.show()
#                 register_button.enable()
#                 login_button.show()
#                 login_button.enable()
#
#             elif event.type == SENDREGISTER:  # 发送用户信息到客户端
#                 print(check_code+'\n'+r_check_box.text)
#                 if check_code != '':
#                     if check_code.lower() == r_check_box.text.lower():
#                         result = identify_client.send_all_information(r_id_box.text, r_email_box.text, r_password_box.text)
#                         if result:
#                             print('成功')
#                         else:
#                             print("注册失败")
#                 print(r_email_box.text)
#                 print(r_id_box.text)
#                 print(r_password_box.text)
#                 # ic.send_all_information(r_email_box.text, r_id_box.text, r_password_box.text)
#             elif event.type == SENDCHECK:  # 发送验证码
#                 username = r_id_box.text
#                 print(username)
#                 email = r_email_box.text
#                 check_code = identify_client.get_check_code(username, email)
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
#             sys.exit()
#     if page_status == 0:
#         screen.blit(start_title, (10, 10))
#         start.render(screen)
#     elif page_status == 1:
#         pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
#         id_label.render(screen)
#         password_label.render(screen)
#         back.render(screen)
#         id_box.draw(screen)
#         password_box.draw(screen)
#         register_button.render(screen)
#         login_button.render(screen)
#     elif page_status == 2:
#         pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
#         back.render(screen)
#         r_email_label.render(screen)
#         r_id_label.render(screen)
#         r_password_label.render(screen)
#         r_check_label.render(screen)
#
#         r_email_box.draw(screen)
#         r_id_box.draw(screen)
#         r_password_box.draw_password(screen)
#         r_check_box.draw(screen)
#
#         register_button.render(screen)
#         r_button.render(screen)
#         r_check_button.render(screen)
#     setting.render(screen)
#     pygame.display.flip()

