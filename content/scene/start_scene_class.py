import pygame
from content.scene.local_game_scene import LocalGameScene
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.login_scene_class import LogInScene
from content.scene.room_scene import RoomScene
from content.UI.ui_function import UIFunction


class StartScene(Scene):
    def __init__(self):
        """准备开始界面的组件"""
        super().__init__()
        # start_font = SceneFont.start_font
        # start_rect = pygame.Rect(455, 280, 290, 100)
        # start_title = pygame.image.load(self.path + "assets\\texture\\FAGWhite.png")  # 用作画图
        # start_title = pygame.transform.smoothscale(start_title, (514, 200))
        # start_title = start_title.convert_alpha()
        #
        # online_game_button = Button("onlinegame", self.online_is_clicked, start_rect,
        #                self.path + "assets\\Img\\start_unpressed.png", 1, '在线游戏', start_font)  # 用作画图
        # online_game_button.add_img(self.path + "assets\\Img\\start_press.png")
        #
        # login_rect = pygame.Rect(1120, 20, 60, 40)
        # login_button = Button("login", self.login_is_clicked, login_rect,
        #                       self.settings.btbg_light, 0, '登录', SceneFont.log_font)
        # login_button.add_img(self.settings.btbg_light_pressed)
        #
        # local_rect = pygame.Rect(455, 450, 290, 100)
        # local_button = Button('local game', self.local_is_clicked, local_rect,
        #                            self.path + "assets\\Img\\start_unpressed.png", 0, '本地游戏', SceneFont.start_font)
        # local_button.add_img(self.path + "assets\\Img\\start_press.png")
        start_title = UIFunction.new_start_logo(self)
        login_button = UIFunction.new_login_button(self)
        online_game_button = UIFunction.new_online_button(self)
        local_button = UIFunction.new_local_button(self)

        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': None, 'box': None, 'button': [login_button, online_game_button, local_button, self.set_button], 'panel': []}

    def online_is_clicked(self):
        ScenePlayer.push(RoomScene())
        #TODO:点了没反应

    def login_is_clicked(self):
        ScenePlayer.push(LogInScene())

    def local_is_clicked(self):
        self.loaded['panel'] = [UIFunction.new_select_map_panel(self)]

    def select_map_button_clicked(self, name: str):
        self.loaded['panel'] = []
        ScenePlayer.push(LocalGameScene(name))  # 留给游戏登录


    def show(self):
        self.screen.fill((10, 10, 10))
        self.screen.blit(self.loaded['img'], (10, 10))
        self.draw_elements()
        pygame.display.flip()



