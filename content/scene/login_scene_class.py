import pygame
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.UI.message_box import MessageBox
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.register_scene_class import RegScene
from content.online.player_info import PlayerInfo


class LogInScene(Scene):
    """登录界面"""

    def __init__(self):
        super().__init__()
        self.id = 0
        self.bg = (10, 10, 10)
        id_label = Label(0.305*self.width, 0.3125*self.height, 98, "账号(用户名)")
        password_label = Label(0.305*self.width, 0.4375*self.height, 42, "密码")
        id_box = InputBox(pygame.Rect(0.41*self.width, 0.3125*self.height, 0.271*self.width, 0.04375*self.height))  # 输入框的宽不由传入参数决定。
        password_box = InputBox(pygame.Rect(0.41*self.width, 0.4375*self.height, 0.271*self.width, 0.04375*self.height),
                                is_pw=1)
        boxL = [id_box, password_box]
        """注册按钮"""
        register_rect = pygame.Rect(0.5*self.width, 0.5725*self.height, 0.15*self.width, 0.05*self.height)
        register_button = Button("register", self.register_is_clicked, register_rect,
                                 self.settings.btbg_light, 0, '没有账号?注册', SceneFont.log_font)
        register_button.add_img(self.settings.btbg_light_pressed)
        """登录按钮"""
        login_rect = pygame.Rect(0.375*self.width, 0.5725*self.height, 0.0583*self.width, 0.05*self.height)
        login_button = Button("login", self.login_is_clicked, login_rect,
                              self.settings.btbg_light, 0, "登录", SceneFont.log_font)
        login_button.add_img(self.settings.btbg_light_pressed)

        self.loaded = {'img': None, 'label': [id_label, password_label], 'box': boxL,
                       'button': [self.back, register_button, login_button],
                       'panel': [], 'msgbox': []}

    def show(self):
        self.screen.fill(self.bg)
        pygame.draw.rect(self.screen, (46, 46, 46),
                         (0.25*self.width, 0.2*self.height, 0.5*self.width, 0.5*self.height),
                         border_radius=15)
        self.draw_elements()
        pygame.display.flip()

    def register_is_clicked(self):
        ScenePlayer.push(RegScene())

    def login_is_clicked(self):
        userid = self.loaded['box'][0].text
        userpw = self.loaded['box'][1].text
        if userid != '' and userpw != '':
            # 输入用户名和密码的时候才登录
            answer = self.client.login(userid, userpw)
            if answer:
                # print("登录成功")
                PlayerInfo.player_name = userid
                ScenePlayer.pop()
            else:
                error_msg_box = MessageBox((0.5, 0.5), "警告", "用户名或密码有误！")
                self.loaded['msgbox'] = [error_msg_box]
                self.has_msgbox = True
        else:
            empty_msg_box = MessageBox((0.5, 0.5), "警告", "用户名和密码不能为空！")
            self.loaded['msgbox'] = [empty_msg_box]
            self.has_msgbox = True
