# -*- coding: utf-8 -*-
import pygame

'''Label 控件，用于显示文字'''
'''使用label时，创建好label对象，render即可'''


class Label:
    def __init__(self, left: int, top: int, width: int, text: str, font_info=None):
        """
        left,top: 指定文本的起始坐标
        text: 文本内容
        font_info（可选参数）: 文字设定，初始化时传入一个字典:
        这个字典包含了"font"（字体），"tc"（字体颜色），"bc"（背景颜色），"align"（ 水平模式，0,1,2分别对应靠左、居中、靠右），"valign"（垂直模式，0,1,2分别代表）
        align和valign用于调整对齐
        """
        if font_info is None:
            font_info = {
                'font': pygame.font.Font("Font/SourceHanSans-Normal.ttc", 21),
                'tc': (169, 183, 198),
                'bc': None,
                'align': 0,
                'valign': 0
            }
            self.font = font_info["font"]
            self.tc = font_info["tc"]
            self.bc = font_info["bc"]
            self.align = font_info["align"]
            self.valign = font_info["valign"]
        else:
            self.font = font_info["font"]
            self.tc = font_info["tc"]
            self.bc = font_info["bc"]
            self.align = font_info["align"]
            self.valign = font_info["valign"]
        self.is_show = True  # 默认显示

        self.left = left
        self.top = top
        self.width = width  # 背景板的宽度，方便计算居中
        self.text = text

        self.display_x = left
        self.display_y = top

        if text == '':
            self.text_surface = None
        else:
            self.set_text(text)  # 此处会创建一个Surface对象用于之后的显示

    def render(self, surface: pygame.surface):
        """接受一个surface对象，在其上方显示文字"""
        if self.text != '' and self.is_show:
            self.set_align(self.align)
            surface.blit(self.text_surface, (self.display_x, self.display_y))

    def set_text(self, text, tc=None, bc=None):
        """设置(或修改）文字内容，并重新建立Surface对象，默认不修改原有颜色"""
        self.text = text
        if tc is not None:
            self.tc = tc
        if bc is not None:
            self.bc = bc
        self.text_surface = self.font.render(self.text, True, self.tc, self.bc)
        print(self.text, ",文字大小为", self.text_surface.get_size())  # 测试用
        # pygame.font.render方法，返回一个surface对象

    def __get_size(self):
        """返回文字surface对象的大小，宽和高，与背景无关"""
        if self.text_surface is None:
            return 0, 0
        else:

            return self.text_surface.get_size()
            # pygame.surface.get_size()

    def set_align(self, align: int):
        """设置水平对齐方式，0：靠左（也就是不变），1：居中，2：靠右"""
        width, height = self.__get_size()
        if align == 2:
            self.display_x = self.left - width
        elif align == 1:
            self.display_x = self.left + int((self.width-width) / 2)
        elif align == 0:
            self.display_x = self.left

    def set_valign(self, valign: int):
        """设置水平对齐方式，0：靠上，1：居中，2：靠下（也就是不变）"""
        width, height = self.__get_size()
        if valign == 2:
            self.display_x = self.top - height
        elif valign == 1:
            self.display_x = self.top - int(height / 2)
        elif valign == 0:
            self.display_x = self.top

    def set_pos(self, left, top, align=None, valign=None):
        """
        设置（更改）文本显示的位置，传入的参数是左和上
        对齐如果不更改仍然沿用
        """
        self.left = left
        self.top = top
        if align is not None:
            self.align = align
        if valign is not None:
            self.valign = valign

        self.set_align(self.align)
        self.set_valign(self.valign)

    def hide(self, flag: bool):
        if flag:
            self.is_show = False
        else:
            self.is_show = True
