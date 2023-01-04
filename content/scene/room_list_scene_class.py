import pygame
from pygame import Rect
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.scene.scene_player_class import ScenePlayer
from content.scene.register_scene_class import RegScene
from content.UI.ui_function import UIFunction as UIF
from content.online.player_info import PlayerInfo
from content.scene.room_scene import RoomScene


class RoomListScene(Scene):
    """服务器大厅(房间列表)的场景"""
    def __init__(self):
        super().__init__()
        screen_rect = self.screen.get_rect()
        search_box_rect = Rect(screen_rect.width-300, 30, 120, 35)
        self.search_box = InputBox(search_box_rect)
        search_label_rect = Rect(screen_rect.width-400, 30, 50, 35)
        self.search_label = Label(search_label_rect.left, search_label_rect.top, search_label_rect.width, '搜索房间：')
        refresh_button_rect = Rect(screen_rect.width-150, 30, 100, 35)
        self.refresh_button = Button('刷新', self.refresh_button_clicked, refresh_button_rect,
                                     self.settings.btbg_light, 0, '刷新', SceneFont.log_font)
        self.refresh_button.add_img(self.settings.btbg_light_pressed)
        create_room_button_rect = Rect(0, 30, 100, 35)
        create_room_button_rect.centerx = screen_rect.centerx

        self.create_room_button = Button('创建房间', self.create_room_button_clicked, create_room_button_rect,
                                         self.settings.btbg_light, 0, '创建房间', SceneFont.log_font)
        self.create_room_button.add_img(self.settings.btbg_light_pressed)
        self.all_room_list_panel = UIF.new_all_room_list_panel(self)
        self.join_fail_panel = UIF.new_join_fail_panel(self)
        self.loaded = {'img': None, 'label': [self.search_label], 'box': [self.search_box],
                       'button': [self.back, self.refresh_button, self.create_room_button],
                       'panel': [self.all_room_list_panel, self.join_fail_panel], 'msgbox': []}
        self.refresh_button_clicked()
        self.bgm_id = 1
    def refresh_button_clicked(self):
        """点击刷新按钮"""
        room_list = self.client.getroomlist()
        self.all_room_list_panel.loaded['ctrlrs'][0] = UIF.new_room_list_panel(self, room_list, self.search_box.text)
        self.all_room_list_panel.loaded['ctrlrs'][0].rect.y =\
            self.all_room_list_panel.loaded['ctrlrs'][0].r_xy[1]*self.all_room_list_panel.rect.height

    def create_room_button_clicked(self):
        """点击创建房间按钮"""
        if self.client.creatroom(PlayerInfo.player_name+'的房间', '虚空'):
            ScenePlayer.push(RoomScene(True))

    def room_bar_clicked(self, room_id):
        """点击房间，加入房间"""
        if self.client.joinroom(room_id):
            ScenePlayer.push(RoomScene(False))
        else:
            self.join_fail_panel.is_show = True
            self.join_fail_panel.is_able = True

    def join_fail_panel_button_clicked(self):
        """点击加入房间失败panel上的确定按钮"""
        self.join_fail_panel.is_show = False
        self.join_fail_panel.is_able = False

    def show(self):
        self.screen.fill((10, 10, 10))
        self.draw_elements()
        pygame.display.flip()
