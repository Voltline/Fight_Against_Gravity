import pygame
from content.maps.map_obj import Map
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.scrollbar import ScrollBar
from content.UI.panel_class import Panel
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.UI.hp import HP


class UIFunction:
    @staticmethod
    def new_start_logo(scene):
        """开始界面的logo"""
        start_title = pygame.image.load(scene.path + "assets\\texture\\FAGWhite.png")  # 用作画图
        start_title = pygame.transform.smoothscale(start_title, (514, 200))
        start_title = start_title.convert_alpha()
        return start_title

    @staticmethod
    def new_online_button(scene):
        """开始界面的在线游戏按钮"""
        start_font = SceneFont.start_font
        start_rect = pygame.Rect(455, 250, 290, 100)
        online_game_button = Button("onlinegame", scene.online_is_clicked, start_rect,
                                    scene.path + "assets\\Img\\start_unpressed.png", 1, '在线游戏', start_font)  # 用作画图
        online_game_button.add_img(scene.path + "assets\\Img\\start_press.png")
        return online_game_button

    @staticmethod
    def new_login_button(scene):
        """开始界面的登录按钮"""
        login_rect = pygame.Rect(1120, 20, 60, 40)
        login_button = Button("login", scene.login_is_clicked, login_rect,
                              scene.settings.btbg_light, 0, '登录', SceneFont.log_font)
        login_button.add_img(scene.settings.btbg_light_pressed)
        return login_button

    @staticmethod
    def new_local_button(scene):
        """开始界面的本地登录按钮"""
        local_rect = pygame.Rect(455, 420, 290, 100)
        local_button = Button('local game', scene.local_is_clicked, local_rect,
                              scene.path + "assets\\Img\\start_unpressed.png", 0, '本地游戏', SceneFont.start_font)
        local_button.add_img(scene.path + "assets\\Img\\start_press.png")
        return local_button

    @staticmethod
    def new_reg_labels():
        """注册界面四个输入框之前的文本提示"""
        r_email_label = Label(315, 180, 98, "请输入您的邮箱", SceneFont.white_font)
        r_id_label = Label(315, 260, 106, "请输入您的用户名", SceneFont.white_font)
        r_password_label = Label(315, 340, 42, "设置您的密码", SceneFont.white_font)
        r_check_label = Label(315, 420, 40, "验证码", SceneFont.white_font)
        labels = [r_email_label, r_id_label, r_password_label, r_check_label]
        return labels

    @staticmethod
    def new_reg_boxes():
        """注册界面的四个输入框，分别是邮箱、用户名、密码、验证码"""
        r_email_box = InputBox(pygame.Rect(450, 180, 350, 35))
        r_id_box = InputBox(pygame.Rect(450, 260, 350, 35))
        r_password_box = InputBox(pygame.Rect(450, 340, 350, 35))
        r_check_box = InputBox(pygame.Rect(450, 420, 350, 35))
        boxes = [r_email_box, r_id_box, r_password_box, r_check_box]
        return boxes

    @staticmethod
    def new_register_buttons(scene):
        """注册界面的 确认注册 和 发送验证码 按钮"""
        r_rect = pygame.Rect(650, 500, 100, 40)
        r_button = Button("r", scene.confirm_reg_clicked, r_rect,
                          scene.settings.btbg_light, 0, '确认注册', SceneFont.log_font)
        r_button.add_img(scene.settings.btbg_light_pressed)
        check_rect = pygame.Rect(430, 500, 110, 40)
        r_check_button = Button('check', scene.send_checkcode_clicked, check_rect,
                                scene.settings.btbg_light, 0, '发送验证码', SceneFont.log_font)
        r_check_button.add_img(scene.settings.btbg_light_pressed)
        buttons = [r_button, r_check_button, scene.back, scene.set_button]  # 包含了返回和设置
        return buttons


    @staticmethod
    def new_select_map_button(scene, name):
        path = scene.path + "assets\\texture\\thumbnail\\" + name + ".png"
        temp_rect = pygame.Rect(0, 0, 250, 250)
        select_map_button = Button(name, lambda: scene.select_map_button_clicked(name),
                                   temp_rect, path, 1, name, SceneFont.map_list_font)
        return select_map_button

    @staticmethod
    def new_select_map_panel(scene):  # 770 x 550
        buttons = []
        for name in Map.maps_info.keys():
            buttons.append(UIFunction.new_select_map_button(scene, name))
        buttons[0].r_xy = 0.007, 0.133
        buttons[1].r_xy = 0.338, 0.133
        buttons[2].r_xy = 0.669, 0.133
        buttons[3].r_xy = 0.007, 0.565
        buttons[4].r_xy = 0.338, 0.565
        buttons[5].r_xy = 0.669, 0.565

        close_rect = pygame.Rect(0, 0, 20, 20)
        close_button = Button('close', scene.close_is_clicked, close_rect,
                                   scene.path + 'assets\\Img\\close_unclicked.png', 0)
        close_button.r_xy = 0.968, 0.020
        close_button.add_img(scene.path + 'assets\\Img\\close_clicked.png')

        buttons.append(close_button)

        map_rect = pygame.Rect(0, 0, 770, 590)
        map_rect.center = scene.screen.get_rect().center
        map_panel = Panel(map_rect, "地图选择", 28, buttons, text_pos=0)
        return map_panel

    @staticmethod
    def new_status_bar_panel(scene, username):
        pass
