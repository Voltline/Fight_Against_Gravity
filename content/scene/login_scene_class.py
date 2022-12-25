from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.register_scene_class import RegScene
from content.scene.menu_scene import MenuScene
from content.online.player_info import PlayerInfo
import pygame


class LogInScene(Scene):
    """登录界面"""

    def __init__(self):
        super().__init__()
        self.id = 0
        self.bg = (10, 10, 10)
        id_label = Label(330, 250, 98, "账号(用户名)")
        password_label = Label(330, 350, 42, "密码")
        id_box = InputBox(pygame.Rect(450, 250, 325, 35))  # 输入框的宽不由传入参数决定。
        password_box = InputBox(pygame.Rect(450, 350, 325, 35), is_pw=1)
        boxL = [id_box, password_box]
        """注册按钮"""
        register_rect = pygame.Rect(600, 450, 180, 40)
        register_button = Button("register", self.register_is_clicked, register_rect,
                                 self.settings.btbg_light, 0, '没有账号?注册', SceneFont.log_font)
        register_button.add_img(self.settings.btbg_light_pressed)
        """登录按钮"""
        login_rect = pygame.Rect(450, 450, 70, 40)
        login_button = Button("login", self.login_is_clicked, login_rect,
                              self.settings.btbg_light, 0, "登录", SceneFont.log_font)
        login_button.add_img(self.settings.btbg_light_pressed)

        self.loaded = {'img': None, 'label': [id_label, password_label], 'box': boxL,
                       'button': [self.back, register_button, login_button],
                       'panel': []}

    def show(self):
        self.screen.fill(self.bg)
        pygame.draw.rect(self.screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
        self.draw_elements()
        pygame.display.flip()

    def register_is_clicked(self):
        ScenePlayer.push(RegScene())

    def login_is_clicked(self):
        userid = self.loaded['box'][0].text
        userpw = self.loaded['box'][1].text
        answer = self.client.login(userid, userpw)
        if answer:
            print("登录成功")
            PlayerInfo.player_name = userid
            ScenePlayer.pop()
        else:
            print("failed")
