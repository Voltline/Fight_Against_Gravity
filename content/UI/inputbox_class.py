import time

import pygame
import pygame.key
import os
import sys
from pygame.locals import SCRAP_TEXT
import platform


class InputBox:
    def __init__(self, rect: pygame.Rect, is_pw=0) -> None:
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.rect: pygame.Rect = rect
        self.r_xy = (0, 0)
        self.color_inside_inactive = pygame.Color(31, 31, 31)
        self.color_inactive = pygame.Color(71, 71, 71)  # 未被选中的颜色
        self.color_active = pygame.Color(105, 105, 105)  # 被选中的颜色
        self.color_inside_active = pygame.Color(38, 38, 38)
        self.color = self.color_inactive  # 当前边框颜色，初始为未激活颜色
        self.color_inside = self.color_inside_inactive  # 当前填充内色
        self.active = False
        self.text = ''
        self.done = False

        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'

        self.font = pygame.font.Font(path + "assets\\font\\SourceHanSans-Normal.ttc", 18)  # 11/25 14:25 文件路径添加前缀UI
        self.font_color = pygame.Color(169, 183, 198)
        self.is_pw = is_pw
        # self.bg = pygame.Color(52, 52, 52)

    def deal_event(self, event: pygame.event.Event):
        pygame.scrap.init()
        if self.active:
            self.color = self.color_active
            self.color_inside = self.color_inside_active
        else:
            self.color = self.color_inactive
            self.color_inside = self.color_inside_inactive
        if event.type == pygame.KEYDOWN:
            # 键盘输入响应
            if self.active:
                key_name = pygame.key.name(event.key)
                print(key_name, event.mod)
                if event.key == pygame.K_RETURN:
                    print('*'+self.text+'*')
                elif event.key == 118 and (event.mod == 4160 or event.mod == 4224):
                    scrap_text = pygame.scrap.get(SCRAP_TEXT)
                    if scrap_text:
                        if 'Windows' in platform.platform():
                            scrap_text = scrap_text.decode('gbk').strip('\x00')
                        self.text = self.text + scrap_text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_TAB:
                    pass
                else:
                    self.text += event.unicode

    def render(self, screen: pygame.surface.Surface):
        if self.is_pw:
            self.draw_password(screen)
        else:
            txt_surface = self.font.render(self.text, True, self.font_color)  # 文字转换为图片
            width = max(self.rect.w, txt_surface.get_width() + 10)  # 当文字过长时，延长文本框
            pygame.draw.rect(screen, self.color_inside, self.rect, 0, border_radius=15)
            pygame.draw.rect(screen, self.color, self.rect, 4, border_radius=15)
            screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 5))
            cursor = self.font.render('|', True, (170, 205, 255))
            w, h = txt_surface.get_size()
            if int(time.time() * 2) % 3 != 0 and self.active:
                screen.blit(cursor, (self.rect.x + w + 12, self.rect.y + 2))

    def switch(self):
        self.active = not self.active

    def draw_password(self, screen):
        password = ''
        for i in range(len(self.text)):
            password += '*'
        password_surface = self.font.render(password, True, self.font_color)
        width = max(0.2708*screen.get_rect().width, password_surface.get_width() + 10)  # 当文字过长时，延长文本框
        self.rect.w = width
        pygame.draw.rect(screen, self.color_inside, self.rect, 0, border_radius=15)
        pygame.draw.rect(screen, self.color, self.rect, 4, border_radius=15)
        screen.blit(password_surface, (self.rect.x + 5, self.rect.y + 5))
        cursor = self.font.render('|', True, (170, 205, 255))
        w, h = password_surface.get_size()
        if int(time.time() * 2) % 3 != 0 and self.active:
            screen.blit(cursor, (self.rect.x + w + 12, self.rect.y + 2))

    def is_over(self, point, pos_offset=(0, 0)) -> bool:
        """检测鼠标位置是否在按钮上，并检测按钮是否可用"""
        flag = self.rect.collidepoint(point[0]-pos_offset[0], point[1]-pos_offset[1])
        return flag

    def check_click(self, event, pos_offset=(0, 0)):
        """每次点击完返回鼠标位置"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_over(event.pos, pos_offset)
        return False
