import pygame
from label_class import Label
from button_class import Button
from inputbox_class import InputBox

"""管理所有控件的页面类，一个Page代表一个屏幕画面"""


class Page:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, self.setting.screen_width, self.setting.screen_height)
        self.buttons = {}  # 统一管理按钮组件
        self.labels = {}  # 统一管理文本组件
        self.background = None  # 页面背景图

    def set_background(self, img_file: str):
        self.background = pygame.image.load(img_file)

    def show_background(self, screen):
        screen.blit(self.background, self.rect)

    """ 添加文本控件 """
    def add_label(self, name, left, top, text, font_info):
        self.labels[name] = Label(left, top, text, font_info)

    """ 添加按钮 """
    def add_button(self, name, event_id, rect, img_file, img_sub, text, font_info=None):
        self.buttons[name] = Button(name, event_id, rect, img_file, img_sub, text, font_info)

    # TODO: 实现多选按钮，单选按钮
    """添加选择框"""
#    def add_checkbox(self, name, rect, img_file, img_sub, text, font_info=None):
