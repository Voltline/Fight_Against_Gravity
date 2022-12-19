import time

import pygame
import pygame.key
import os
from pygame.locals import SCRAP_TEXT
import platform


class InputBox:
    def __init__(self, rect: pygame.Rect, is_pw=0) -> None:
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inside_inactive = pygame.Color(31, 31, 31)
        self.color_inactive = pygame.Color(71, 71, 71)  # 未被选中的颜色
        self.color_active = pygame.Color(105, 105, 105)  # 被选中的颜色
        self.color_inside_active = pygame.Color(38, 38, 38)
        self.color = self.color_inactive  # 当前边框颜色，初始为未激活颜色
        self.color_inside = self.color_inside_inactive  # 当前填充内色
        self.active = False
        self.text = ''
        self.done = False
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\"
        self.font = pygame.font.Font(path + "assets\\font\\SourceHanSans-Normal.ttc", 18)  # 11/25 14:25 文件路径添加前缀UI
        self.font_color = pygame.Color(169, 183, 198)
        self.is_pw = is_pw
        # self.bg = pygame.Color(52, 52, 52)

    def deal_event(self, event: pygame.event.Event):
        if self.active:
            self.color = self.color_active
            self.color_inside = self.color_inside_active
        else:
            self.color = self.color_inactive
            self.color_inside = self.color_inside_inactive
        if event.type == pygame.KEYDOWN:
            # 键盘输入响应
            if self.active:
                if event.key == pygame.K_RETURN:
                    print('*'+self.text+'*')
                elif event.key == 118 and (event.mod == 64 or event.mod == 1024):
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
            width = max(self.boxBody.w, txt_surface.get_width()+10)  # 当文字过长时，延长文本框
            pygame.draw.rect(screen, self.color_inside, self.boxBody, 0, border_radius=15)
            pygame.draw.rect(screen, self.color, self.boxBody, 4, border_radius=15)
            screen.blit(txt_surface, (self.boxBody.x+10, self.boxBody.y+5))
            cursor = self.font.render('|', True, (170, 205, 255))
            w, h = txt_surface.get_size()
            if int(time.time() * 2) % 3 != 0 and self.active:
                screen.blit(cursor, (self.boxBody.x+w+12, self.boxBody.y+2))

    def switch(self):
        self.active = not self.active

    def draw_password(self, screen):
        password = ''
        for i in range(len(self.text)):
            password += '*'
        password_surface = self.font.render(password, True, self.font_color)
        width = max(325, password_surface.get_width() + 10)  # 当文字过长时，延长文本框
        self.boxBody.w = width
        pygame.draw.rect(screen, self.color_inside, self.boxBody, 0, border_radius=15)
        pygame.draw.rect(screen, self.color, self.boxBody, 4, border_radius=15)
        screen.blit(password_surface, (self.boxBody.x + 5, self.boxBody.y + 5))