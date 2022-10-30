# -*- coding: utf-8 -*-
from turtle import width
import pygame
from Label_Class import Label

'''
按钮控件，主体是一个承载图像的surface和一个承载文字的Label控件
本质上是一个响应鼠标点击的矩形区域
使用方法，制定好参数创建好一个Button，然后render即可
'''


class Control:
    def __init__(self, rect, img_file: str, img_sub: int, text, font_info):
        '''
        rect: rect对象,决定控制组件的位置,也用于创建label, img_file: 图片文件路径,img_sub: 一个整数,表示这个图要被切成几张,text:文本内容,font_info: 字体设置
        '''
        '''
        属性：is_show: 是否显示这个控件，is_active:控件是否被激活，__img: 被加载好的图像，img_width:底图的长度，subimg_width:子图宽度
        status:用于标记这个按钮可用还是不可用。
        '''
        self.is_show = 1
        self.is_active = 0
        self.status = 1
        self.rect = rect
        self.img_sub = img_sub
        self.text = text
        self.font_info = font_info

        # 下面来处理控制组建的图像，加载进去并形成一个list
        if img_file is None:
            self.__img = None
            self.img_width = 0
        else:
            self.__img = pygame.image.load(img_file)
            self.__imgList = []

        # sub_width是指单独一个小按钮的宽度，整个img是一串连续的小按钮，我只在这里进行裁剪
        img_rect = self.__img.get_rect()
        sub_width = int(img_rect.width / img_sub)
        x = 0
        for i in range(self.img_sub):
            self.__imgList.append(self.__img.subsurface(x, 0), (sub_width, img_rect.height))
        self.subimg_width = sub_width

        # 下面设定Label对象
        if (text == None):
            self.label = None
        else:
            self.label = Label(rect.left, rect.top, text, font_info)

    def render(self, surface):
        if self.is_show:
            if self.__img is not None:
                if self.status < self.img_sub:
                    surface.blit(self.__imgList[self.status], (self.rect.left, self.rect.top))
            if self.label is not None:
                self.label.render(surface)

    def is_over(self, point) -> bool:
        if self.status <= 0:
            bflag = False
        else:
            bflag = self.rect.collidepoint(point)
        return bflag

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.is_over(event.pos)

    def disable(self):
        self.status = 0

    def enable(self):
        self.status = 1

    def hide(self):
        self.is_show = 0
