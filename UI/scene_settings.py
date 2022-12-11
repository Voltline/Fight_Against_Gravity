import pygame
import os

from scene_font import SceneFont


class SceneSetting:
    def __init__(self):
        self.UI_current_directory = os.getcwd()  # UI文件夹路径
        print(self.UI_current_directory)
        self.fag_directory = os.path.dirname(self.UI_current_directory)  # FAG文件夹路径
        print(self.fag_directory)

        """字体路径"""
        self.font_path_light = "UI/Font/SourceHanSans-Light.ttc"
        self.font_path_normal = "UI/Font/SourceHanSans-Normal.ttc"
        """按钮背景路径"""
        self.btbg_light = "UI/Img/light_butbg_unpressed.png"  # 按钮浅灰底，未按版
        self.btbg_light_pressed = "UI/Img/light_butbg.png"  # 鼠标移动反响
        os.chdir(self.fag_directory)
        SceneFont.init(self)
