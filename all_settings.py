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
        self.space_obj_img_path = 'assets/texture/space_obj.png'  # space_obj图片路径
