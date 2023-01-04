import sys

import pygame
from content.scene.local_game_scene import LocalGameScene
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.UI.label_class import Label
from content.UI.message_box import MessageBox
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.login_scene_class import LogInScene
from content.scene.room_scene import RoomScene
from content.scene.room_list_scene_class import RoomListScene
from content.UI.ui_function import UIFunction
from content.online.player_info import PlayerInfo


class StartScene(Scene):
    def __init__(self):
        """准备开始界面的组件"""
        super().__init__()

        start_title = UIFunction.new_start_logo(self)
        login_button = UIFunction.new_login_button(self)
        online_game_button = UIFunction.new_online_button(self)
        local_button = UIFunction.new_local_button(self)
        exit_button = UIFunction.new_exit_button(self)
        version_label = UIFunction.new_version_label(self, Scene.settings.version)

        """集合组件，loaded"""
        self.loaded = {'img': start_title, 'label': [version_label], 'box': None,
                       'button': [login_button, online_game_button, local_button, self.set_button, exit_button],
                       'panel': [], 'msgbox': []}

    def online_is_clicked(self):
        try:
            if not self.client.get_start():
                self.client.start_client()
            if PlayerInfo.player_name == '':
                ScenePlayer.push(LogInScene())
            else:
                ScenePlayer.push(RoomListScene())
        except:
            offline_msg_box = MessageBox((0.5, 0.5), "提示", "您可能已经离线，正在尝试重新连接")
            self.loaded['msgbox'] = [offline_msg_box]
            self.has_msgbox = True
            self.client.start_client()

    def login_is_clicked(self):
        if not self.client.get_start():
            self.client.start_client()
        if PlayerInfo.player_name == '':
            ScenePlayer.push(LogInScene())
        else:
            self.loaded['button'][0].set_text('已登录')

    def local_is_clicked(self):
        self.loaded['panel'].append(UIFunction.new_select_map_panel(self))

    def exit_is_clicked(self):
        pygame.quit()
        sys.exit()

    def select_map_button_clicked(self, name: str):
        self.loaded['panel'] = []
        ScenePlayer.push(LocalGameScene(name))

    def show(self):
        self.screen.fill((10, 10, 10))
        self.screen.blit(self.loaded['img'], (10, 10))
        if PlayerInfo.player_name != '':
            self.loaded['button'][0].set_text('已登录')
        self.draw_elements()
        pygame.display.flip()
