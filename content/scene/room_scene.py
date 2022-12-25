from content.scene.scene_class import Scene
from content.UI.button_class import Button
# from content.UI.inputbox_class import InputBox
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.UI.panel_class import Panel
from content.scene.scene_player_class import ScenePlayer
import pygame
import time


class RoomScene(Scene):

    def __init__(self, isowner: bool = False, roomid = None):
        super().__init__()
        self.confirm_quit_bool = False
        self.last_update_time = 0
        self.roomname = "默认房间名"
        self.roommap = "地月系统"
        self.is_owner = isowner  # 是否是房主
        self.is_ready = False
        self.client.creatroom("test", self.roommap)
        self.is_owner = True
        # self.client.joinroom("f0699daa-8449-11ed-9442-27c29e6f1d88")
        # TODO:测试用 创建了个房间

        # 左侧房间信息初始化
        r_roomname_lable = Label(100, 160, 800, "房间名：" + self.roomname, SceneFont.white_font)
        r_roomname_lable.r_xy = 0.1, 1 / 10 * 0.8
        """房间名"""
        r_roommap_lable = Label(100, 200, 800, "房间地图：" + self.roommap, SceneFont.white_font)
        r_roommap_lable.r_xy = 0.1, 1 / 10 * 1.6
        """房间地图名"""
        self.not_allready_lable = Label(570, 710, 800, "有玩家未准备", SceneFont.red_font)
        self.not_allready_lable.is_show = False
        self.user_name_lable = {}
        self.user_ready_lable = {}
        self.user_dready_lable = {}
        for i in range(8):
            self.user_name_lable[i] = Label(170, 200 + 50 * i, 200, "玩家" + str(i), SceneFont.user_name_font)
            self.user_name_lable[i].r_xy = 0.1, 0.05 + 1 / 10 * i
            self.user_name_lable[i].is_show = False
            self.user_ready_lable[i] = Label(470, 200 + 50 * i, 200, "已准备", SceneFont.ready_font)
            self.user_ready_lable[i].r_xy = 0.6, 0.05 + 1 / 10 * i
            self.user_ready_lable[i].is_show = False
            self.user_dready_lable[i] = Label(470, 200 + 50 * i, 200, "未准备", SceneFont.dready_font)
            self.user_dready_lable[i].r_xy = 0.6, 0.05 + 1 / 10 * i
            self.user_dready_lable[i].is_show = False
        self.labels = [self.not_allready_lable]
        self.room_lables = [r_roomname_lable, r_roommap_lable]
        """左侧房间信息"""
        self.user_lables = []
        """右侧玩家名"""
        for i in range(8):
            self.user_lables.append(self.user_name_lable[i])
            self.user_lables.append(self.user_ready_lable[i])
            self.user_lables.append(self.user_dready_lable[i])
        r_rect = pygame.Rect(600, 700, 300, 50)
        self.r_ready_button = Button("ready", self.ready_is_clicked, r_rect, self.settings.btbg_light, 0, "准备",
                                     SceneFont.log_font)
        if self.is_owner:
            self.r_ready_button = Button("start", self.start_is_clicked, r_rect, self.settings.btbg_light, 0,
                                         "开始游戏", SceneFont.log_font)
        r_change_map_button = Button("changemap", self.change_map_is_clicked, pygame.Rect(100, 470, 200, 50),
                                     self.settings.btbg_light, 0, "更改地图", SceneFont.log_font)
        r_change_map_button.r_xy = 0.1, 1 / 10 * 7
        r_roommap_button = Button("roommap", lambda: 1, pygame.Rect(100, 240, 200, 200),
                                  self.path + "/assets/texture/thumbnail/" + self.roommap + ".png", 0, "",
                                  SceneFont.log_font)
        r_roommap_button.r_xy = 0.1, 1 / 10 * 2.8
        r_change_name_button = Button("changename", self.change_name_is_clicked, pygame.Rect(100, 570, 200, 50),
                                      self.settings.btbg_light, 0, "更改房间名", SceneFont.log_font)
        r_change_name_button.r_xy = 0.1, 1 / 10 * 8.55
        r_confirm_button = Button("changename", self.confirm_quit_is_clicked, pygame.Rect(0, 0, 100, 50),
                                  self.settings.btbg_light, 0, "确认", SceneFont.log_font)
        r_confirm_button.r_xy = 0.1, 0.55
        r_dconfirm_button = Button("changename", self.dconfirm_quit_is_clicked, pygame.Rect(0, 0, 100, 50),
                                   self.settings.btbg_light, 0, "取消", SceneFont.log_font)
        r_dconfirm_button.r_xy = 0.6, 0.55
        r_confirm_button_ = Button("changename", self.confirm__is_clicked, pygame.Rect(0, 0, 100, 50),
                                   self.settings.btbg_light, 0, "确认", SceneFont.log_font)
        r_confirm_button_.r_xy = 0.4, 0.55
        self.buttons = [self.back, self.r_ready_button]
        self.room_buttons = [r_change_map_button, r_change_name_button]
        self.room_lables.append(r_roommap_button)
        user_panel = Panel(pygame.Rect(400, 150, 700, 500), "", 28, others=self.user_lables)
        """用户信息"""
        room_panel = Panel(pygame.Rect(80, 150, 250, 500), "", 28, others=self.room_lables, ctrlrs=self.room_buttons)
        """房间信息"""
        self.user_confirm_quit_panel = Panel(pygame.Rect(450, 300, 300, 180), "确认退出?", 28,
                                             ctrlrs=[r_confirm_button, r_dconfirm_button], text_pos=0.5)
        self.owner_quit_warning_panel = Panel(pygame.Rect(450, 300, 400, 180), "有玩家未退出，无法退出房间", 25,
                                              ctrlrs=[r_confirm_button_], text_pos=0.5)
        self.user_confirm_quit_panel.color = (13, 13, 13)
        self.owner_quit_warning_panel.color = (13, 13, 13)
        self.user_confirm_quit_panel.is_show = False
        self.user_confirm_quit_panel.is_able = False
        self.owner_quit_warning_panel.is_show = False
        self.owner_quit_warning_panel.is_able = False
        self.panel = [user_panel, room_panel, self.user_confirm_quit_panel, self.owner_quit_warning_panel]
        self.loaded = {'label': self.labels, 'box': [], 'button': self.buttons, 'panel': self.panel}

    def show(self):
        self.screen.fill((10, 10, 10))
        self.draw_elements()
        pygame.display.flip()

    def back_is_clicked(self):
        self.user_confirm_quit_panel.is_show = True
        self.user_confirm_quit_panel.is_able = True
        # if self.is_owner:
        #     res = self.client.deleteroom()
        #     if not res:
        #         # 没有成功删除房间
        #         return False
        # else:
        #     print("user left room")
        #     self.client.leftroom()
        # ScenePlayer.pop()

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
        self.not_allready_lable.is_show = False
        res = self.client.startgame()
        if not res:
            self.not_allready_lable.is_show = True

    def change_map_is_clicked(self):
        pass

    def change_name_is_clicked(self):
        pass

    def update_user(self):
        if time.time() - self.last_update_time > 1:
            print("update at", time.time())
            self.last_update_time = time.time()
            res = self.client.getroom()
            if res:
                owner = res["owner"]
                userlist = res["userlist"]
                self.user_ready_lable[0].set_text("房  主")
                self.user_ready_lable[0].is_show = True
                self.user_dready_lable[0].is_show = False
                self.user_name_lable[0].set_text(owner)
                self.user_name_lable[0].is_show = True
                now = 1
                has_dready = False
                for user, ready in userlist:
                    if user == owner:
                        continue
                    if ready:
                        self.user_ready_lable[now].is_show = True
                        self.user_dready_lable[now].is_show = False
                    else:
                        has_dready = True
                        self.user_ready_lable[now].is_show = False
                        self.user_dready_lable[now].is_show = True
                    self.user_name_lable[now].set_text(user)
                    self.user_name_lable[now].is_show = True
                    now += 1
                if not has_dready:
                    self.not_allready_lable.is_show = False
                for i in range(now, 8):
                    self.user_ready_lable[i].is_show = False
                    self.user_name_lable[i].is_show = False
                    self.user_dready_lable[i].is_show = False

    def update(self):
        self.update_user()
        self.deal_events()

    def confirm_quit_is_clicked(self):
        if self.is_owner:
            res = self.client.deleteroom()
            print(res)
            if res:
                ScenePlayer.pop()
            else:
                self.user_confirm_quit_panel.is_show = False
                self.user_confirm_quit_panel.is_able = False
                self.owner_quit_warning_panel.is_show = True
                self.owner_quit_warning_panel.is_able = True
        else:
            print("user left room")
            self.client.leftroom()
            ScenePlayer.pop()

    def confirm__is_clicked(self):
        self.owner_quit_warning_panel.is_show = False
        self.owner_quit_warning_panel.is_able = False
        self.user_confirm_quit_panel.is_show = False
        self.user_confirm_quit_panel.is_able = False

    def dconfirm_quit_is_clicked(self):
        self.user_confirm_quit_panel.is_show = False
        self.user_confirm_quit_panel.is_able = False
