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

        start_title = UIFunction.new_start_logo(self)
        login_button = UIFunction.new_login_button(self)
        online_game_button = UIFunction.new_online_button(self)
        local_button = UIFunction.new_local_button(self)

        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': [], 'box': None, 'button': [login_button, online_game_button, local_button, self.set_button], 'panel': []}

    def online_is_clicked(self):
        ScenePlayer.push(RoomScene())

    def login_is_clicked(self):
        ScenePlayer.push(LogInScene())

    def local_is_clicked(self):
        self.loaded['panel'].append(UIFunction.new_select_map_panel(self))

    def select_map_button_clicked(self, name: str):
        self.loaded['panel'] = []
        ScenePlayer.push(LocalGameScene(name))

    def show(self):
        self.screen.fill((10, 10, 10))
        self.screen.blit(self.loaded['img'], (10, 10))
        self.draw_elements()
        pygame.display.flip()



