# 保存游戏的各类设置
import pygame


class Settings:
    """保存游戏的各类设置"""
    def __init__(self):
        # 窗口设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 10)
        self.game_title = 'Fight Against Gravity'
        self.max_fps = 120  # 最大帧率

        # 开场设置
        self.title_time_sec = 3  # 标题显示时间
        self.icon_img_path = 'assets/texture/icon1.png'  # 图标图片路径

        # SpaceObj
        self.space_obj_image_path = 'assets/texture/space_obj.png'  # space_obj图片路径

        # Bullet
        self.bullet_color_key = (0, 0, 0)  # bullet的透明色
        self.bullet_color = (180, 255, 255)  # bullet的颜色
        self.bullet_radius = 5  # bullet的圆的半径
        self.bullet_image = self.make_bullet_image()
        self.bullet_spd = 20  # 子弹相对于飞船的初速度的模,用的时候要乘以方向向量
        self.bullet_damage = 20  # 每颗子弹造成的伤害

        # Ship
        self.ship_image_path = 'assets/texture/ship.png'  # 飞船图片路径
        self.ship_hp = 100  # 飞船初始血量
        self.ship_go_acc = 10  # 飞船前进/后退的加速度
        self.ship_turn_spd = 1.7  # 飞船转弯的角速度(弧度制)
        self.ship1_k_go_ahead = pygame.K_w
        self.ship1_k_go_back = pygame.K_s
        self.ship1_k_turn_left = pygame.K_a
        self.ship1_k_turn_right = pygame.K_d
        self.ship1_k_fire = pygame.K_e
        self.ship2_k_go_ahead = pygame.K_i
        self.ship2_k_go_back = pygame.K_k
        self.ship2_k_turn_left = pygame.K_j
        self.ship2_k_turn_right = pygame.K_l
        self.ship2_k_fire = pygame.K_u

    def make_bullet_image(self):
        image = pygame.Surface((2*self.bullet_radius+1, 2*self.bullet_radius+1))
        image.set_colorkey(self.bullet_color_key)  # 设置透明色
        image.fill(self.bullet_color_key)  # 用透明色填充图片
        pygame.draw.circle(image, self.bullet_color,  # 用实际色画实心圆
                           (self.bullet_radius+1, self.bullet_radius+1), self.bullet_radius)
        return image
