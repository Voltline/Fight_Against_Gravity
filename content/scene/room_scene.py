import pygame
import time
from content.scene.scene_class import Scene
from content.UI.button_class import Button
from content.UI.label_class import Label
from content.scene.scene_font import SceneFont
from content.UI.panel_class import Panel
from content.scene.scene_player_class import ScenePlayer
from content.UI.ui_function import UIFunction as UIF
from content.scene.client_game_scene_class import ClientGameScene
from Server.Modules.OptType import OptType
from content.maps.map_obj import Map


class RoomScene(Scene):

    def __init__(self, is_owner: bool = False):
        super().__init__()
        self.confirm_quit_bool = False
        self.last_update_time = 0
        self.last_update_loading_time = 0
        self.last_update_loading_message_time = 0
        self.last_update_loading_id = 0
        self.last_update_loading_message_id = 0
        self.roomname = "默认房间名"
        self.roommap = "地月系统"
        self.userlist = []
        self.is_owner = is_owner  # 是否是房主
        self.is_ready = False
        self.is_start = False
        # 左侧房间信息初始化
        self.r_roomname_lable = Label(0.0833 * self.width, 0.2 * self.height, 800, "房间名：" + self.roomname,
                                      SceneFont.white_font)
        self.r_roomname_lable.r_xy = 0.1, 1 / 10 * 0.8
        """房间名"""
        self.r_roommap_lable = Label(0.0833 * self.width, 0.25 * self.height, 800, "房间地图：" + self.roommap,
                                     SceneFont.white_font)
        self.r_roommap_lable.r_xy = 0.1, 1 / 10 * 1.3
        """房间地图名"""
        self.r_roomnum_lable = Label(0.0833 * self.width, 0.25 * self.height, 800, "房间人数：0/0" + self.roommap,
                                     SceneFont.white_font)
        self.r_roomnum_lable.r_xy = 0.1, 1 / 10 * 1.8
        "房间人数"
        self.not_allready_lable = Label(0.475 * self.width, 0.8875 * self.height, 800, "有玩家未准备",
                                        SceneFont.red_font)
        self.not_allready_lable.is_show = False
        self.user_name_lable = {}
        self.user_ready_lable = {}
        self.user_dready_lable = {}
        for i in range(8):
            self.user_name_lable[i] = Label(0.1417 * self.width, 0.2 * self.height + 0.0625 * self.height * i, 200,
                                            "玩家" + str(i), SceneFont.user_name_font)
            self.user_name_lable[i].r_xy = 0.1, 0.05 + 1 / 10 * i
            self.user_name_lable[i].is_show = False
            self.user_ready_lable[i] = Label(0.3917 * self.width, 0.2 * self.height + 0.0625 * self.height * i, 200,
                                             "已准备", SceneFont.ready_font)
            self.user_ready_lable[i].r_xy = 0.6, 0.05 + 1 / 10 * i
            self.user_ready_lable[i].is_show = False
            self.user_dready_lable[i] = Label(0.3917 * self.width, 0.2 * self.height + 0.0625 * self.height * i, 200,
                                              "未准备", SceneFont.dready_font)
            self.user_dready_lable[i].r_xy = 0.6, 0.05 + 1 / 10 * i
            self.user_dready_lable[i].is_show = False
        self.labels = [self.not_allready_lable]
        self.room_lables = [self.r_roomname_lable, self.r_roommap_lable, self.r_roomnum_lable]
        """左侧房间信息"""
        self.user_lables = []
        """右侧玩家名"""
        for i in range(8):
            self.user_lables.append(self.user_name_lable[i])
            self.user_lables.append(self.user_ready_lable[i])
            self.user_lables.append(self.user_dready_lable[i])
        r_rect = pygame.Rect(0.5 * self.width, 0.895 * self.height, 0.25 * self.width, 0.0725 * self.height)
        self.ready_button = Button("ready", self.ready_is_clicked, r_rect, self.settings.btbg_light, 0, "准备",
                                   SceneFont.log_font)
        self.start_button = Button("start", self.start_is_clicked, r_rect, self.settings.btbg_light, 0,
                                   "开始游戏", SceneFont.log_font)
        self.ready_button.add_img(self.settings.btbg_light_pressed)
        self.start_button.add_img(self.settings.btbg_light_pressed)
        self.ready_button.is_show = self.ready_button.is_able = False
        self.start_button.is_show = self.start_button.is_able = False
        self.r_change_map_button = Button("changemap", self.change_map_clicked,
                                          pygame.Rect(0.0833 * self.width, 0.5875 * self.height, 0.1667 * self.width,
                                                      0.0625 * self.height),
                                          self.settings.btbg_light, 0, "更改地图", SceneFont.log_font)
        self.r_change_map_button.add_img(self.settings.btbg_light_pressed)
        self.r_change_map_button.r_xy = 0.1, 1 / 10 * 7
        self.r_roommap_button = Button("roommap", lambda: 1,
                                       pygame.Rect(0.0833 * self.width, 0.2 * self.height, 0.1667 * self.width,
                                                   0.1667 * self.width),
                                       self.path + "/assets/texture/thumbnail/" + self.roommap + ".png", 0, "",
                                       SceneFont.log_font)

        self.r_roommap_button.r_xy = 0.1, 1 / 10 * 2.6
        self.r_change_name_button = Button("changename", self.change_name_clicked,
                                           pygame.Rect(0.0833 * self.width, 0.7125 * self.width, 0.1667 * self.width,
                                                       0.0625 * self.height),
                                           self.settings.btbg_light, 0, "更改房间名", SceneFont.log_font)
        self.r_change_name_button.add_img(self.settings.btbg_light_pressed)
        self.r_change_name_button.r_xy = 0.1, 1 / 10 * 8.55
        if self.is_owner:
            self.start_button.is_show = self.start_button.is_able = True
        else:
            self.ready_button.is_show = self.ready_button.is_able = True
            self.r_change_map_button.is_show = self.r_change_map_button.is_able = False
            self.r_change_name_button.is_show = self.r_change_name_button.is_able = False
        r_confirm_button = Button("changename", self.confirm_quit_is_clicked, pygame.Rect(0, 0, 100, 50),
                                  self.settings.btbg_light, 0, "确认", SceneFont.log_font)
        r_confirm_button.add_img(self.settings.btbg_light_pressed)
        r_confirm_button.r_xy = 0.1, 0.55
        r_dconfirm_button = Button("changename", self.dconfirm_quit_is_clicked, pygame.Rect(0, 0, 100, 50),
                                   self.settings.btbg_light, 0, "取消", SceneFont.log_font)
        r_dconfirm_button.add_img(self.settings.btbg_light_pressed)
        r_dconfirm_button.r_xy = 0.6, 0.55
        r_confirm_button_ = Button("changename", self.confirm__is_clicked, pygame.Rect(0, 0, 100, 50),
                                   self.settings.btbg_light, 0, "确认", SceneFont.log_font)
        r_confirm_button_.add_img(self.settings.btbg_light_pressed)
        r_confirm_button_.r_xy = 0.4, 0.55
        self.buttons = [self.back, self.ready_button, self.start_button]
        self.room_buttons = [self.r_change_map_button, self.r_change_name_button]
        self.room_lables.append(self.r_roommap_button)
        user_panel = Panel(
            pygame.Rect(0.333 * self.width, 0.1275 * self.height, 0.5833 * self.width, 0.725 * self.height), "", 28,
            others=self.user_lables)
        """用户信息"""
        room_panel = Panel(
            pygame.Rect(0.0667 * self.width, 0.1275 * self.height, 0.2083 * self.width, 0.725 * self.height), "", 28,
            others=self.room_lables, ctrlrs=self.room_buttons)
        """房间信息"""
        self.user_confirm_quit_panel = Panel(
            pygame.Rect(0.375 * self.width, 0.375 * self.height, 0.25 * self.width, 0.225 * self.height), "确认退出?",
            28,
            ctrlrs=[r_confirm_button, r_dconfirm_button], text_pos=0.5)
        self.owner_quit_warning_panel = Panel(
            pygame.Rect(0.375 * self.width, 0.375 * self.height, 0.333 * self.width, 0.225 * self.height),
            "有玩家未退出，无法退出房间", 25,
            ctrlrs=[r_confirm_button_], text_pos=0.5)
        self.loading_message = [
            "游戏加载中 loading...      |",
            "游戏加载中 loading...      /",
            "游戏加载中 loading...      -",
            "游戏加载中 loading...      \\",
        ]
        self.r_wating_start_lable = Label(1 * self.width, 0.5 * self.height, 200,
                                          self.loading_message[self.last_update_loading_id], SceneFont.wating_font)
        self.r_wating_start_lable.r_xy = 0.4, 0.25
        self.wating_message = [
            "游戏操作按键可以在设置里进行修改",
            "想要全屏畅快战斗？去设置看看吧",
            "悄悄告诉你，这个游戏在github开源了 QAQ",
            "想要改变运动轨迹？想想高中学的卫星变轨 qwq",
            "发射子弹虽然是不限量的，但很可能击中自己",
            "子弹虽然不限量，但还是有冷却时间的",
            "飞不到对方的轨道上？那就把子弹发射过去！",
            "你知道吗？树莓派版的Minecraft是开源的",
            "操控飞船，击败对手，取得胜利！QWQ",
            "凝胶：好吃又易燃        ——泰拉瑞亚",
            "想度过第一天？挖三填一        ——MC",
            "自然选择,前进四",
            "水滴!攻击物是水滴!!!",
            "向着星辰与深渊",
            "在低点与高点加减速最有效率",
            "不要距离战场太远，太远会星际迷航(0v0)",
            "欢迎报考东中国正常大学",
            "游戏中点击鼠标中键可以锁定视角在飞船上",
            "在线游戏点鼠标左键就能发射子弹哦",
            "游戏中鼠标右键拖动和鼠标滚轮滚动可以调整视角",
            "在线游戏死亡后会自动进入观战模式哦",
            "锟斤拷锟斤拷锟斤拷",
            "烫烫烫",
            # "现在时间是：" + str(time.strftime("%Y-%m-%d %H:%M",time.gmtime())),
            "Exception in thread \"main\" java.lang.NullPointerException",
            "按E送雷电将军",
            "有时候你的对手手感火热，挡也挡不住",
            "再渺小的心愿,银河系都有它的容身之所",
            "我是布洛特亨德尔",
            "刀客塔,您还有许多事要处理,现在还不能休息哦",
            "泠鸢yousa没有腿",
            "说坏话会被hanser大小姐雇人砍了手脚",
            "心脏要逃走了     ——Lycoris Recoil",
            "少女祈祷中"
        ]
        self.r_wating_start_message_lable = Label(1 * self.width, 0.5 * self.height, 200,
                                                  self.wating_message[self.last_update_loading_id],
                                                  SceneFont.wating_message_font)
        self.r_wating_start_message_lable.r_xy = 0.4, 0.65
        self.wating_start_panel = Panel(pygame.Rect(0 * self.width, 0 * self.height, 1 * self.width, 1 * self.height),
                                        "", 30, others=[self.r_wating_start_lable, self.r_wating_start_message_lable],
                                        text_pos=0.5, border_radius=0)
        self.user_confirm_quit_panel.color = (13, 13, 13)
        self.owner_quit_warning_panel.color = (13, 13, 13)
        self.user_confirm_quit_panel.is_show = False
        self.user_confirm_quit_panel.is_able = False
        self.owner_quit_warning_panel.is_show = False
        self.owner_quit_warning_panel.is_able = False
        self.wating_start_panel.is_show = False
        self.wating_start_panel.is_able = False
        self.select_map_panel = UIF.new_select_map_panel(self)
        self.select_map_panel.is_able = self.select_map_panel.is_show = False
        self.change_room_name_panel = UIF.new_change_room_name_panel(self)
        self.change_room_name_panel.is_able = self.change_room_name_panel.is_show = False
        self.panel = [user_panel, room_panel, self.user_confirm_quit_panel, self.owner_quit_warning_panel,
                      self.select_map_panel, self.change_room_name_panel, self.wating_start_panel]
        self.update_user()
        self.loaded = {'label': self.labels, 'box': [], 'button': self.buttons, 'panel': self.panel, 'msgbox': []}
        self.bgm_id = 1
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
        self.select_map_panel.is_show = False
        self.select_map_panel.is_able = False

    def ready_is_clicked(self):
        if self.is_ready:
            res = self.client.dready()
            # print("dready is clicked", res)
            if res:
                self.ready_button.set_text("准备")
                self.is_ready = False

        else:
            res = self.client.ready()
            # print("ready is clicked", res)
            if res:
                self.ready_button.set_text("取消准备")
                self.is_ready = True

    def update_ready_button(self):
        if self.is_ready:
            self.ready_button.set_text("取消准备")
        else:
            self.ready_button.set_text("准备")

    def start_is_clicked(self):
        self.not_allready_lable.is_show = False
        res = self.client.startgame()
        if not res:
            self.not_allready_lable.is_show = True
        else:
            self.wating_start_panel.is_show = True
            pass

    def change_map_clicked(self):
        """点击房间中的切换地图按钮"""
        self.select_map_panel.is_show = True
        self.select_map_panel.is_able = True

    def select_map_button_clicked(self, name: str):
        """点击选择地图panel上的地图按钮"""
        self.select_map_panel.is_show = False
        self.select_map_panel.is_able = False
        self.client.changemap(name)

    def change_name_clicked(self):
        """点击房间中的更改房间名按钮"""
        self.change_room_name_panel.is_show = True
        self.change_room_name_panel.is_able = True

    def change_room_name_confirm_button_clicked(self):
        """点击更改房间名panel上的确定按钮"""
        self.client.changeroomname(self.change_room_name_panel.loaded['boxes'][0].text)
        self.change_room_name_panel.is_show = False
        self.change_room_name_panel.is_able = False

    def change_room_name_cancel_button_clicked(self):
        """点击更改房间名panel上的取消按钮"""
        self.change_room_name_panel.is_show = False
        self.change_room_name_panel.is_able = False

    def update_user(self):
        if time.time() - self.last_update_time > 1:
            # print("update at", time.time())
            self.last_update_time = time.time()
            self.client.getroom()

    def update_loading(self):
        stm = time.time()
        if stm - self.last_update_loading_time > 0.25:
            self.last_update_loading_time = stm
            self.last_update_loading_id += 1
            self.r_wating_start_lable.set_text(
                self.loading_message[self.last_update_loading_id % len(self.loading_message)])
        if stm - self.last_update_loading_message_time > 3.5:
            self.last_update_loading_message_time = stm
            import random
            self.last_update_loading_message_id += random.randint(1, len(self.wating_message))
            self.last_update_loading_message_id = self.last_update_loading_message_id % len(self.wating_message)
            self.r_wating_start_message_lable.set_text(
                self.wating_message[self.last_update_loading_message_id])

    def deal_msgs(self):
        """非阻塞接收并处理消息"""
        msg_list = self.client.client.get_message_list() + self.client.udp_client.get_message_list()
        for msg in msg_list:
            opt = msg['opt']
            if opt == OptType.getRoom:
                res = msg['room']
                if res:
                    self.is_owner = (res["owner"] == self.client.local_get_user())
                    if self.is_owner:
                        self.ready_button.is_show = self.ready_button.is_able = False
                        self.start_button.is_show = self.start_button.is_able = True
                        self.r_change_map_button.is_show = True
                        self.r_change_map_button.is_able = True
                        self.r_change_name_button.is_show = True
                        self.r_change_name_button.is_able = True

                    else:
                        self.ready_button.is_show = self.ready_button.is_able = True
                        self.start_button.is_show = self.start_button.is_able = False
                        self.r_change_map_button.is_show = False
                        self.r_change_map_button.is_able = False
                        self.r_change_name_button.is_show = False
                        self.r_change_name_button.is_able = False
                    self.roommap = res["roommap"]
                    self.roomname = res["roomname"]
                    self.r_roommap_lable.set_text('地图：' + self.roommap)
                    self.r_roomname_lable.set_text('房间名：' + self.roomname)
                    self.r_roommap_button.change_new_image(
                        self.path + "/assets/texture/thumbnail/" + self.roommap + ".png")
                    owner = res["owner"]
                    self.userlist = res["userlist"]
                    self.r_roomnum_lable.set_text(
                        "房间人数：" + str(len(self.userlist)) + "/" + str(len(Map(self.roommap).ships_info)))
                    self.user_ready_lable[0].set_text("房  主")
                    self.user_ready_lable[0].is_show = True
                    self.user_dready_lable[0].is_show = False
                    self.user_name_lable[0].set_text(owner)
                    self.user_name_lable[0].is_show = True
                    now = 1
                    has_dready = False
                    for user, ready in self.userlist:
                        if user == owner:
                            continue
                        if user == self.client.local_get_user():
                            self.is_ready = ready
                            self.update_ready_button()
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
                    if res['is_run'] and not self.is_start:
                        # 开始游戏
                        self.wating_start_panel.is_show = self.wating_start_panel.is_able = True
                    self.is_start = res['is_run']
            elif opt == OptType.ServerStartGameTime:
                self.wating_start_panel.is_show = self.wating_start_panel.is_able = False
                ScenePlayer.push(ClientGameScene(self.roommap, [u[0] for u in self.userlist], msg['time']))

    def update(self):
        self.update_user()
        self.deal_msgs()
        self.deal_events()
        self.update_loading()

    def confirm_quit_is_clicked(self):
        if self.is_owner:
            res = self.client.deleteroom()
            # print(res)
            if res:
                self.client.deleteroom()
                ScenePlayer.pop()
            else:
                self.user_confirm_quit_panel.is_show = False
                self.user_confirm_quit_panel.is_able = False
                self.owner_quit_warning_panel.is_show = True
                self.owner_quit_warning_panel.is_able = True
        else:
            # print("user left room")
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
