# 保存游戏的各类设置
import pygame
import json


class Settings:
    """保存游戏的各类设置"""
    def __init__(self):
        with open("game_settings.json", "r") as f:
            inf = json.load(f)
        # 窗口设置
        window = inf["Window"]
        self.screen_width = window["screen_width"]
        self.screen_height = window["screen_height"]
        self.bg_color = eval(window["bg_color"])
        self.game_title = window["game_title"]
        self.max_fps = window["max_fps"]  # 最大帧率
        del window

        # 开场设置
        opening = inf["Opening"]
        self.title_time_sec = opening["title_time_sec"]  # 标题显示时间
        self.icon_img_path = opening["icon_img_path"]  # 图标图片路径
        del opening

        # SpaceObj
        self.space_obj_image_path = inf["SpaceObj"]["space_obj_image_path"]  # space_obj图片路径

        # Bullet
        bullet = inf["Bullet"]
        self.bullet_color_key = eval(bullet["bullet_color_key"])  # bullet的透明色
        self.bullet_color = eval(bullet["bullet_color"])  # bullet的颜色
        self.bullet_radius = bullet["bullet_radius"]  # bullet的圆的半径
        self.bullet_image = self.make_bullet_image()
        self.bullet_spd = bullet["bullet_spd"]  # 子弹相对于飞船的初速度的模,用的时候要乘以方向向量
        self.bullet_damage = bullet["bullet_damage"]  # 每颗子弹造成的伤害
        del bullet

        # Ships
        ships = inf["Ships"]
        self.ship_image_path = ships["ship_image_path"]  # 飞船图片路径
        self.ship_hp = ships["ship_hp"]  # 飞船初始血量
        self.ship_go_acc = ships["ship_go_acc"]  # 飞船前进/后退的加速度
        self.ship_turn_spd = ships["ship_turn_spd"]  # 飞船转弯的角速度(弧度制)
        del ships

        # Ship1
        ship1 = inf["Ship1"]
        self.ship1_k_go_ahead = eval(ship1["k_go_ahead"])
        self.ship1_k_go_back = eval(ship1["k_go_back"])
        self.ship1_k_turn_left = eval(ship1["k_turn_left"])
        self.ship1_k_turn_right = eval(ship1["k_turn_right"])
        self.ship1_k_fire = eval(ship1["k_fire"])
        del ship1

        # Ship2
        ship2 = inf["Ship2"]
        self.ship2_k_go_ahead = eval(ship2["k_go_ahead"])
        self.ship2_k_go_back = eval(ship2["k_go_back"])
        self.ship2_k_turn_left = eval(ship2["k_turn_left"])
        self.ship2_k_turn_right = eval(ship2["k_turn_right"])
        self.ship2_k_fire = eval(ship2["k_fire"])
        del ship2

        del inf

    def make_bullet_image(self):
        image = pygame.Surface((2*self.bullet_radius+1, 2*self.bullet_radius+1))
        image.set_colorkey(self.bullet_color_key)  # 设置透明色
        image.fill(self.bullet_color_key)  # 用透明色填充图片
        pygame.draw.circle(image, self.bullet_color,  # 用实际色画实心圆
                           (self.bullet_radius+1, self.bullet_radius+1), self.bullet_radius)
        return image

    def change_window(self, new_width: int, new_height: int, new_fps: int):
        """修改分辨率
        :参数：new_width：宽度，new_height：高
        :返回：无返回值
        """
        self.screen_width = new_width
        self.screen_height = new_height
        self.max_fps = new_fps
        with open("game_settings.json", "r") as f:
            inf = json.load(f)
            inf["Window"]["screen_width"] = new_width
            inf["Window"]["screen_height"] = new_height
            inf["Window"]["max_fps"] = new_fps
        with open("game_settings.json", "r") as g:
            json.dump(inf, g)

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
        with open("game_settings.json", "r") as f:
            inf = json.load(f)
            inf[sector][target_key] = str(new_key)
        with open("game_settings.json", "r") as g:
            json.dump(inf, g)
        self.__init__() # 重新调用初始化函数改变键位参数

