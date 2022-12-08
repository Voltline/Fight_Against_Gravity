from Scene_Class import Scene
from Button_Class import Button
from InputBox_Class import InputBox
from Label_Class import Label
from Scene_Events import SceneEvents
from UI_Font import UIFont
import os
import pygame


class LogInScene(Scene):
    """加载登录界面组件, 对应页面状态1"""

    def __init__(self):
        super().__init__()
        os.chdir(self.fag_directory)
        id_label = Label(330, 250, 98, "账号(用户名)")
        password_label = Label(330, 350, 42, "密码")
        id_box = InputBox(pygame.Rect(450, 250, 350, 35))  # 输入框的宽不由传入参数决定。
        password_box = InputBox(pygame.Rect(450, 350, 350, 35), is_pw=1)
        boxL = [id_box, password_box]
        """注册按钮"""
        register_rect = pygame.Rect(600, 450, 180, 40)
        register_button = Button("register", SceneEvents.REGISTER, register_rect, self.btbg_light, 0, '没有账号?注册',
                                 self.log_font)
        register_button.add_img(self.btbg_light_pressed)
        """登录按钮"""
        login_rect = pygame.Rect(450, 450, 70, 40)
        login_button = Button("login", SceneEvents.LOGIN, login_rect, self.btbg_light, 0, "登录", self.log_font)
        login_button.add_img(self.btbg_light_pressed)
        self.loaded = {'img': None, 'label': [id_label, password_label], 'box': boxL,
                       'button': [register_button, login_button]}

    def show(self, screen):
        screen.fill((10, 10, 10))
        pygame.draw.rect(screen, (46, 46, 46), (300, 150, 600, 400), border_radius=15)
        self.draw_elements(screen)
        pygame.display.flip()
