import pygame
from content.UI.label_class import Label
from content.UI.button_class import Button
from content.scene.scene_font import SceneFont
import sys
import os


class MessageBox:

    def __init__(self, box_xy, relative_xy, title='', msg='', warning_img='', ctrlrs=[]):
        """
        box_xy: 弹窗的起始left、top的比例
        relative_xy: msg在弹窗的相对left、top的比例
        title: 弹窗的标题
        msg: 弹窗的内容
        warning_img: 弹窗可能会有的错误提示图片路径
        ctrls: 可能有的按钮
        """
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'

        self.txt_color = SceneFont.white_font_msgbox['tc']  # 字体颜色
        self.font = SceneFont.white_font_msgbox['font']  # 字体
        if title is not None:
            self.title = title  # 标题
            self.title_surface = self.font.render(self.title, True, self.txt_color, None)
            self.title_w, self.title_h = self.title_surface.get_size()
            print(title, self.title_w, self.title_h)

        if msg is not None:
            self.msg = msg  # 提示消息
            self.msg_suface = self.font.render(self.msg, True, self.txt_color, None)
            self.msg_w, self.msg_h = self.msg_suface.get_size()  # 获得提示内容文字的宽和高
            print(msg, self.msg_w, self.msg_h)
        if warning_img != '':
            self.warn_img = pygame.image.load(warning_img)
            self.warn_img = pygame.transform.smoothscale(self.warn_img, (50, 50))

        self.box_xy = box_xy
        self.txt_xy = relative_xy
        self.loaded = {'ctrlrs': ctrlrs}

        self.box_w = self.msg_w + 100  # 提示框的宽度
        self.box_h = max(self.msg_h, 40) + 60  # 提示框的高度
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
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(box_left, box_top, self.box_w, self.box_h), border_radius=self.border_radius)
        if self.title is not None:
            screen.blit(self.title_surface, (box_left+(self.box_w-self.title_w)/2, box_top+10))
        if self.msg is not None:
            msg_left = box_left + self.txt_xy[0] * self.box_w
            msg_top = max(box_top + 10 + self.title_h + 5, self.txt_xy[1] * self.box_h)
            screen.blit(self.msg_suface, (msg_left, msg_top))
        # for objs in self.loaded.values():
        #     for obj in objs:
        #         obj.render(self.box_surface)
        # screen.blit(self.box_surface, (box_left, box_top, self.box_w, self.box_h))
    def update(self, e):
        pass