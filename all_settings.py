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
