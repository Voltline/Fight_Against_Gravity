import pygame
import pygame.freetype
from content.UI.label_class import Label
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
import sys
import os


class MessageBox:

    def __init__(self, box_xy, relative_xy, title='', msg='', warning_img='', ctrlrs=[], has_ctrlrs=False):
        """
        box_xy: 弹窗的起始left、top的比例
        relative_xy: msg在弹窗的相对left、top的比例
        title: 弹窗的标题
        msg: 弹窗的内容
        warning_img: 弹窗可能会有的错误提示图片路径
        ctrlrs: 可能有的按钮
        has_ctrlrs: 默认False，即默认没有按钮
        """
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'

        self.txt_color = SceneFont.white_font_msgbox['tc']  # 字体颜色
        self.font = SceneFont.white_font_msgbox['font']  # 字体
        if title is not None:
            self.title = title  # 标题
            print("self.title", title)
            self.title_rect = pygame.freetype.Font.get_rect(self.font, self.title)

            self.title_w = self.title_rect.width  # 获取title的宽高
            self.title_h = self.title_rect.height

        if msg is not None:
            self.msg = msg  # 提示消息
            self.msg_rect = pygame.freetype.Font.get_rect(self.font, self.msg)

            self.msg_w = self.msg_rect.width
            self.msg_h = self.msg_rect.height  # 获得提示内容文字的宽和高, 请不要使用msg_rect亦或是title_rect

        if warning_img != '':
            self.warn_img = pygame.image.load(warning_img)
            self.warn_img = pygame.transform.smoothscale(self.warn_img, (50, 50))

        self.box_xy = box_xy
        self.txt_xy = relative_xy
        self.loaded = {'ctrlrs': ctrlrs}

        self.box_w = 300  # 提示框的宽度
        self.box_h = max(self.msg_h, 40) + 120  # 提示框的高度
        print(self.box_w, self.box_h)
        # 计算组件相对位置
        for objs in self.loaded.values():
            for obj in objs:
                obj.rect.left = obj.r_xy[0] * self.box_w
                obj.rect.top = obj.r_xy[1] * self.box_h

        self.box_surface = pygame.Surface((self.box_w, self.box_h))
        self.color = (26, 26, 28)
        self.color_key = (1, 1, 1)
        self.box_surface.set_colorkey(self.color_key)
        self.box_surface.fill(self.color_key)
        self.border_radius = 16

    def render(self, screen):
        sc_w, sc_h = screen.get_size()  # 获取屏幕宽高
        box_left = self.box_xy[0] * sc_w  # 提示框的left
        box_top = self.box_xy[1] * sc_h  # 提示框的top
        pygame.draw.rect(self.box_surface, self.color,
                         pygame.Rect(0, 0, self.box_w, self.box_h), border_radius=self.border_radius)

        if self.title is not None:
            # 因为是在新的surface上画，所以并不需要对left和top添加box的坐标，此时的坐标就是相对box来的
            self.font.render_to(self.box_surface, pygame.Rect((self.box_w-self.title_w)/2, 10, 200, 100), self.title, self.txt_color)
        if self.msg is not None:
            msg_left = self.txt_xy[0] * self.box_w
            msg_top = max(10 + self.title_h + 5, self.txt_xy[1] * self.box_h)
            self.font.render_to(self.box_surface, pygame.Rect(msg_left, msg_top, 200, 100), self.msg, self.txt_color)

        screen.blit(self.box_surface, (box_left, box_top, self.box_w, self.box_h))
        # for objs in self.loaded.values():
        #     for obj in objs:
        #         obj.render(self.box_surface)

    def update(self, e):
        pass