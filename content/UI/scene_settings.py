import pygame
import os

from content.UI.scene_font import SceneFont


class SceneSetting:
    def __init__(self):
        self.fag_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # FAG文件夹路径
        self.fag_directory = os.path.dirname(self.fag_directory) + "\\"
        print(self.fag_directory)

        """字体路径"""
        self.font_path_light = self.fag_directory + "assets\\font\\SourceHanSans-Light.ttc"
        self.font_path_normal = self.fag_directory + "assets\\font\\SourceHanSans-Normal.ttc"
        """按钮背景路径"""
        self.btbg_light = self.fag_directory + "assets\\Img\\light_butbg_unpressed.png"  # 按钮浅灰底，未按版
        self.btbg_light_pressed = self.fag_directory + "assets\\Img\\light_butbg.png"  # 鼠标移动反响
        SceneFont.init(self)
