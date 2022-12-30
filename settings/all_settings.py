"""保存游戏的各类设置"""
import pygame
import json
from content.maps.map_obj import Map
from content.online.obj_msg import ObjMsg
from content.space_objs.bullet import Bullet


class Settings:
    """保存游戏的各类设置"""

    def __init__(self, path: str):
        # TODO：最后要把这里的变量都放进json
        with open(path + "settings/game_settings.json", "r") as f:
            inf = json.load(f)
        # 窗口设置
        window = inf["Window"]
        self.screen_width, self.screen_height = window["screen_resolution"]
        self.bg_color = window["bg_color"]
        self.game_title = window["game_title"]
        self.max_fps = window["max_fps"]  # 最大帧率
        self.path = path
        self.full_screen = window["full_screen"] # 是否全屏，1为是，0为否
        del window

        # 开场设置
        opening = inf["Opening"]
        self.title_time_sec = opening["title_time_sec"]  # 标题显示时间
        self.icon_img_path = opening["icon_img_path"]  # 图标图片路径
        del opening

        # SpaceObj
        self.space_obj_image_path = self.path + inf["SpaceObj"]["space_obj_image_path"]  # space_obj图片路径

        # 物理
        physics = inf["Physics"]  # 物理模拟计算每次的delta_t
        self.physics_dt = physics["physics_dt"]
        del physics

        # Bullet
        bullet = inf["Bullet"]
        self.bullet_color_key = bullet["bullet_color_key"]  # bullet的透明色
        self.bullet_color = bullet["bullet_color"]  # bullet的颜色
        self.bullet_radius = bullet["bullet_radius"]  # bullet的圆的半径
        self.bullet_image = self.make_bullet_image()
        self.bullet_spd = bullet["bullet_spd"]  # 子弹相对于飞船的初速度的模,用的时候要乘以方向向量
        self.bullet_damage = bullet["bullet_damage"]  # 每颗子弹造成的伤害
        del bullet

        # Planet
        self.planet_image_path = inf["Planet"]["planet_image_path"]

        # Ships
        ships = inf["Ships"]
        self.ship_image_path = self.path + ships["ship_image_path"]  # 飞船图片路径
        self.ship_explosion_image_path = self.path + ships["ship_explosion_image_path"]
        self.ship_hp = ships["ship_hp"]  # 飞船初始血量
        self.ship_go_acc = ships["ship_go_acc"]  # 飞船前进/后退的加速度
        self.ship_turn_spd = ships["ship_turn_spd"]  # 飞船转弯的角速度(弧度制)
        del ships

        # Ship1
        ship1 = inf["Ship1"]
        self.ship1_k_go_ahead = ship1["k_go_ahead"]
        self.ship1_k_go_back = ship1["k_go_back"]
        self.ship1_k_turn_left = ship1["k_turn_left"]
        self.ship1_k_turn_right = ship1["k_turn_right"]
        self.ship1_k_fire = ship1["k_fire"]
        self.ship1_keys = {"前进": self.ship1_k_go_ahead, "后退": self.ship1_k_go_back,
                           "左转": self.ship1_k_turn_left, "右转": self.ship1_k_turn_right,
                           "开火": self.ship1_k_fire}
        del ship1

        # Ship2
        ship2 = inf["Ship2"]
        self.ship2_k_go_ahead = ship2["k_go_ahead"]
        self.ship2_k_go_back = ship2["k_go_back"]
        self.ship2_k_turn_left = ship2["k_turn_left"]
        self.ship2_k_turn_right = ship2["k_turn_right"]
        self.ship2_k_fire = ship2["k_fire"]
        self.ship2_keys = {"前进": self.ship2_k_go_ahead, "后退": self.ship2_k_go_back,
                           "左转": self.ship2_k_turn_left, "右转": self.ship2_k_turn_right,
                           "开火": self.ship2_k_fire}
        del ship2

        # Camera
        camera = inf["Camera"]
        self.camera_move_speed = camera['camera_move_speed']  # 视角移动速度系数
        self.camera_zoom_speed = camera['camera_zoom_speed']  # 视角缩放速度系数
        self.camera_zoom_max = camera['camera_zoom_max']  # 视角缩放倍数上限
        self.camera_k_change_mode = camera['camera_k_change_mode']  # 视角模式切换按键
        # self.camera_k_move =
        del camera

        # Trace
        trace = inf['Trace']
        self.trace_life_sec = trace['trace_life_sec']  # 尾迹保留时间
        self.trace_color = trace['trace_color']  # 尾迹颜色
        del trace

        # net
        self.net_clock_check_num = 10  # 校时的次数

        # ObjMsg
        self.obj_msg_r = 4  # ObjMsg中float保留的小数位数

        # FagGame
        self.snapshots_len = 80

        """字体路径"""
        self.font_path_light = self.path + "assets\\font\\SourceHanSans-Light.ttc"
        self.font_path_normal = self.path + "assets\\font\\SourceHanSans-Normal.ttc"
        """按钮背景路径"""
        self.btbg_light = self.path + "assets\\Img\\light_butbg_unpressed.png"  # 按钮浅灰底，未按版
        self.btbg_light_pressed = self.path + "assets\\Img\\light_butbg.png"  # 鼠标移动反响
        # 滚动条图片
        self.thumb = self.path + "assets/Img/thumb_unpressed.png"
        self.thumb_pressed = self.path + "assets/Img/thumb_pressed.png"
        self.bar = self.path + "assets/Img/bar.png"

        del inf

        # 有需要初始化类变量的类的初始化
        Map.load_maps()  # 加载maps_info
        ObjMsg.init(self)
        Bullet.init(self)

    def make_bullet_image(self):
        image = pygame.Surface((2 * self.bullet_radius + 1, 2 * self.bullet_radius + 1))
        image.set_colorkey(self.bullet_color_key)  # 设置透明色
        image.fill(self.bullet_color_key)  # 用透明色填充图片
        pygame.draw.circle(image, self.bullet_color,  # 用实际色画实心圆
                           (self.bullet_radius + 1, self.bullet_radius + 1), self.bullet_radius)
        return image

    @staticmethod
    def make_planet_image_path(index: int) -> str:
        return "assets/texture/planet" + str(index) + ".png"

    def make_ship_explosion_image_path(self, index: int) -> str:
        """根据index返回爆炸的图片。index范围：[0,9]"""
        return self.ship_explosion_image_path + str(index) + '.png'

    def change_window(self, new_width: int, new_height: int, new_fps: int):
        """修改分辨率
        :参数：new_width：宽度，new_height：高
        :返回：无返回值
        """
        self.screen_width = new_width
        self.screen_height = new_height
        self.max_fps = new_fps
        with open(self.path + "settings/game_settings.json", "r") as f:
            inf = json.load(f)
            inf["Window"]["screen_width"] = new_width
            inf["Window"]["screen_height"] = new_height
            inf["Window"]["max_fps"] = new_fps
        with open(self.path + "game_settings.json", "w") as g:
            json.dump(inf, g, indent = 1)

    def change_full_screen(self):
        """修改分辨率
        :参数：new_full_screen 0为非全屏，1为全屏
        :返回：无返回值
        """
        self.full_screen = self.full_screen ^ 1
        with open(self.path + "settings/game_settings.json", "r") as f:
            inf = json.load(f)
            inf["Window"]["full_screen"] = self.full_screen
        with open(self.path + "settings/game_settings.json", "w") as g:
            json.dump(inf, g, indent = 1)

    def change_key(self, sector: str, target_key: str, new_key: pygame.key):
        """修改键位
        :参数：sector：修改的部分(Ship1/Ship2)
              target_key：目标键位：{
                "k_go_ahead": 前进,
                "k_go_back": 后退,
                "k_turn_left": 左转,
                "k_turn_right": 右转,
                "k_fire": 开火
              }
              new_key：新键位（pygame.key对象）
        :返回：无返回值
        """
        with open(self.path + "settings/game_settings.json", "r") as f:
            inf = json.load(f)
            inf[sector][target_key] = new_key
        with open(self.path + "settings/game_settings.json", "w") as g:
            json.dump(inf, g, indent = 1)
        self.__init__(self.path)  # 重新调用初始化函数改变键位参数
