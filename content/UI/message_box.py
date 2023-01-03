import pygame
import pygame.freetype
from content.UI.label_class import Label
from content.UI.button_class import Button
from content.scene.scene_player_class import ScenePlayer
from content.scene.scene_font import SceneFont
import sys
import os


class MessageBox:

    def __init__(self, relative_xy, title='', msg='', warning_img='', ctrlrs=[], has_ctrlrs=False, msg_align=0):
        """
        msg_box会根据屏幕自适应来自动居中
        relative_xy: msg (消息内容) 在 box(弹窗内部) 的相对left、top的比例
        title: 弹窗的标题
        msg: 弹窗的内容
        warning_img: 弹窗可能会有的错误提示图片路径
        ctrlrs: 可能有的按钮
        has_ctrlrs: 默认False，即默认没有按钮
        msg_align: 提示消息的位置，默认0为居中，如果是 1，则将采用relative_xy来决定文本的位置
        一般来说，如果提示消息的内容较短，则采取默认的 msg_align=0 就好
        """
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'

        self.txt_color = SceneFont.white_font_msgbox['tc']  # 字体颜色
        self.font_txt = SceneFont.white_font_msgbox['font']  # 正文字体
        self.font_title = SceneFont.white_font_msgbox_title['font']  # 标题字体
        self.has_ctrlrs = has_ctrlrs
        self.msg_align = msg_align
        if title is not None:
            self.title = title  # 标题
            print("self.title", title)
            self.title_rect = pygame.freetype.Font.get_rect(self.font_txt, self.title)

            self.title_w = self.title_rect.width  # 获取title的宽高
            self.title_h = self.title_rect.height

        if msg is not None:
            self.msg = msg  # 提示消息
            self.msg_rect = pygame.freetype.Font.get_rect(self.font_txt, self.msg)

            self.msg_w = self.msg_rect.width
            self.msg_h = self.msg_rect.height  # 获得提示内容文字的宽和高, 请不要使用msg_rect亦或是title_rect

        if warning_img != '':
            self.warn_img = pygame.image.load(warning_img)
            self.warn_img = pygame.transform.smoothscale(self.warn_img, (50, 50))

        self.txt_xy = relative_xy
        self.loaded = {'ctrlrs': ctrlrs}

        self.box_left = 0
        self.box_top = 0  # left和top会在render函数中被重置为相对于screen的绝对坐标值
        self.box_w = 400  # 提示框的宽度
        self.box_h = max(self.msg_h, 40) + 160  # 提示框的高度
        # print(self.box_w, self.box_h)
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
        box_left = 0.5 * (sc_w - self.box_w) # 提示框的left, 此时是相对于外层
        box_top = 0.5 * (sc_h - self.box_h)  # 提示框的top
        self.box_left = box_left
        self.box_top = box_top
        pygame.draw.rect(self.box_surface, self.color,
                         pygame.Rect(0, 0, self.box_w, self.box_h), border_radius=self.border_radius)

        if self.title is not None:
            # 因为是在新的surface上画，所以并不需要对left和top添加box的坐标，此时的坐标就是相对box来的
            # 一般来说title并不会很长所以不考虑换行了
            self.font_title.render_to(self.box_surface, ((self.box_w - self.title_w) / 2, 10), self.title,
                                      self.txt_color)
        if self.msg is not None:
            if self.msg_align == 1:  # 如果非居中，则按照relative_xy来画
                msg_left = self.txt_xy[0] * self.box_w
                msg_top = max(10 + self.title_h + 25, self.txt_xy[1] * self.box_h)
                single_word_rect = pygame.freetype.Font.get_rect(self.font_txt, self.msg[0])
                single_word_height = single_word_rect.height  # 获取单个字的高
                line_spaces = single_word_height + 8  # 行距
                lines = self.word_wrap()
                for line in lines:
                    self.font_txt.render_to(self.box_surface, (msg_left, msg_top), line, self.txt_color)
                    msg_top += line_spaces
            if self.msg_align == 0:  # 如果是居中的
                msg_left = (self.box_w - self.msg_w) / 2
                msg_top = max(10 + self.title_h + 25, self.txt_xy[1] * self.box_h)
                self.font_txt.render_to(self.box_surface, (msg_left, msg_top), self.msg, self.txt_color)
        if self.has_ctrlrs:
            for objs in self.loaded.values():
                for obj in objs:
                    obj.render(self.box_surface)
                    # print(obj.name, obj.rect)

        screen.blit(self.box_surface, (box_left, box_top, self.box_w, self.box_h))

    def update(self, event, scene):
        """
        重启 <rect(32, 140, 120, 40)>
        取消 <rect(252, 140, 120, 40)>
        """
        if self.check_mouse_click(event) and not self.has_ctrlrs:
            """如果没有按钮，则点击框就取消框"""
            ScenePlayer.STACK[-1].loaded['msgbox'].pop()
            scene.has_msgbox = False
            return True
        elif self.has_ctrlrs:
            if self.check_mouse_click(event):
                for bt in self.loaded['ctrlrs'][::-1]:
                    bt_rect = pygame.Rect(self.box_left + bt.rect.left,
                                          self.box_top + bt.rect.top, bt.rect.width, bt.rect.height)
                    if bt_rect.collidepoint(event.pos):
                        bt.clicked_func()
                        scene.has_msgbox = False
                        return True
            if event.type == pygame.MOUSEMOTION:
                for bt in self.loaded['ctrlrs'][::-1]:
                    bt_rect = pygame.Rect(self.box_left + bt.rect.left,
                                          self.box_top + bt.rect.top, bt.rect.width, bt.rect.height)
                    if len(bt.imgList) > 1:
                        if bt_rect.collidepoint(event.pos):
                            bt.status = 1
                        else:
                            bt.status = 0

        return False

    def check_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            box_rect = pygame.Rect(self.box_left, self.box_top, self.box_w, self.box_h)
            return box_rect.collidepoint(event.pos)

    def word_wrap(self):
        """ 将 msg 先分成若干行，便于绘制 """
        single_word_rect = pygame.freetype.Font.get_rect(self.font_txt, self.msg[0])
        single_word_width = single_word_rect.width  # 获取单个字的宽高
        msg_left = self.txt_xy[0] * self.box_w
        max_words = int(self.box_w - msg_left - 20) // single_word_width  # 一行最多的字数
        total_lines = len(self.msg) // max_words + 1
        lines = []  # 将不同的行放进去
        start = 0
        for i in range(1, total_lines):
            lines.append(self.msg[start: i * max_words + 1])
            start = i * max_words + 1
        lines.append(self.msg[start:])
        return lines
