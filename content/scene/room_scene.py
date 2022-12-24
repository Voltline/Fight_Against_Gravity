from content.scene.scene_class import Scene
from content.UI.button_class import Button
# from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.UI.panel_class import Panel
from content.scene.scene_player_class import ScenePlayer
import pygame


class RoomScene(Scene):

    def __init__(self, isowner: bool = False):
        super().__init__()
        self.roomname = "默认房间名"
        self.roommap = "地月系统"
        self.is_owner = isowner  # 是否是房主
        self.is_ready = False
        self.client.creatroom("test", self.roommap)
        # TODO:测试用 创建了个房间

        r_roomname_lable = Label(100, 160, 800, "房间名："+ self.roomname, SceneFont.white_font)
        # 房间名
        r_roommap_lable = Label(100, 200, 800, "房间地图：" + self.roommap, SceneFont.white_font)
        self.labels = [r_roomname_lable, r_roommap_lable]
        self.boxes = []
        r_rect = pygame.Rect(600, 700, 300, 50)
        self.r_ready_button = Button("ready", self.ready_is_clicked, r_rect, self.settings.btbg_light, 0, "准备", SceneFont.log_font)
        if self.is_owner:
            self.r_ready_button = Button("start", self.start_is_clicked, r_rect, self.settings.btbg_light, 0, "开始游戏", SceneFont.log_font)
        r_change_map_button = Button("changemap", self.change_map_is_clicked, pygame.Rect(100, 470, 200, 50),
                                     self.settings.btbg_light, 0, "更改地图", SceneFont.log_font)
        r_roommap_button = Button("roommap", lambda: 1, pygame.Rect(100, 240, 200, 200),
                                  self.path + "/assets/texture/thumbnail/" + self.roommap + ".png", 0, "", SceneFont.log_font)
        r_change_name_button = Button("changename", self.change_name_is_clicked, pygame.Rect(100, 570, 200, 50),
                                     self.settings.btbg_light, 0, "更改房间名", SceneFont.log_font)
        self.buttons = [self.back, self.r_ready_button, r_change_map_button, r_roommap_button, r_change_name_button]

        # pause_panel_components_relative_pos = {'button': [[0.88, 0.1]], 'box': [[]]}
        # self.not_allready_panel = Panel(self.reminder_panel_rect_small, '有玩家未准备', 22,
        #                                 [self.close_button], [], pause_panel_components_relative_pos)
        self.panel = []
        self.loaded = {'label': self.labels, 'box': self.boxes, 'button': self.buttons, 'panel': self.panel}

    def show(self):
        self.screen.fill((10, 10, 10))
        pygame.draw.rect(self.screen, (46, 46, 46), (400, 150, 700, 500), border_radius=15)
        pygame.draw.rect(self.screen, (46, 46, 46), (80, 150, 250, 500), border_radius=15)
        self.draw_elements()
        pygame.display.flip()

    def back_is_clicked(self):
        if self.is_owner:
            res = self.client.deleteroom()
            if not res:
                # 没有成功删除房间
                return False
        else:
            print("user left room")
            self.client.leftroom()
        ScenePlayer.pop()

    def close_is_clicked(self):
        self.loaded['panel'] = []
        self.box_is_able = True

    def ready_is_clicked(self):
        if self.is_ready:
            res = self.client.dready()
            print("dready is clicked", res)
            if res:
                self.r_ready_button.set_text("准备")
                self.is_ready = False

        else:
            res = self.client.ready()
            print("ready is clicked", res)
            if res:
                self.r_ready_button.set_text("取消准备")
                self.is_ready = True

    def start_is_clicked(self):
        res = self.client.start()
        if not res:
            self.loaded['panel'] = [self.not_allready_panel]

    def change_map_is_clicked(self):
        pass

    def change_name_is_clicked(self):
        pass