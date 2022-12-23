from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.UI.panel_class import Panel
from content.scene.scene_player_class import ScenePlayer
import pygame


class RoomScene(Scene):
    r_rect = pygame.Rect(600, 700, 300, 50)

    def __init__(self, roomname="默认房间名", isowner: bool = False):
        super().__init__()
        r_roomname_lable = Label(600, 50, 800, roomname, SceneFont.white_font)
        # 房间名
        self.client.creatroom("test","地月系统")
        self.labels = [r_roomname_lable]
        self.boxes = []
        self.r_ready_button = Button("ready", self.ready_is_clicked, RoomScene.r_rect, self.settings.btbg_light, 0,
                                     "准备", SceneFont.log_font)
        self.buttons = [self.back, self.r_ready_button]
        self.panel = []
        self.is_owner = isowner  # 是否是房主
        self.is_ready = False
        self.loaded = {'label': self.labels, 'box': self.boxes, 'button': self.buttons, 'panel': self.panel}

    def show(self):
        self.screen.fill((10, 10, 10))
        pygame.draw.rect(self.screen, (46, 46, 46), (400, 150, 700, 500), border_radius=15)
        pygame.draw.rect(self.screen, (46, 46, 46), (80, 150, 250, 600), border_radius=15)
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
            self.r_ready_button.set_text("准备")
            if res:
              self.is_ready = False

        else:
            res = self.client.ready()
            print("ready is clicked", res)
            self.r_ready_button.set_text("取消准备")
            if res:
                self.is_ready = True
    def strt_is_clicked(self):
        self.client.start()
