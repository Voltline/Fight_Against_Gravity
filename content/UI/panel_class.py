import pygame
import os
import sys
from content.scene.scene_font import SceneFont
from content.UI.scrollbar import ScrollBar
from settings.all_settings import Settings


class Panel:
    def __init__(self, rect, text, font_size, buttons, boxes, relative_pos, text_pos=1, has_scrollbar=False):
        """
        rect: 一个四元组，text:panel要显示的文字，
        buttons: panel里的按钮组件，列表形式
        boxes: panel里的输入框组件，列表形式,
        relative_pos: 组件相对于panel的比例,值为二维列表的字典形式.二维数组第一个值为横向比例，第二个值为纵向比例
        text_pos: 文字在panel中的位置，0靠上，1居中，2靠下
        """
        self.rect = pygame.Rect(rect)
        self.text_pos = text_pos
        self.color = (43, 43, 43)  # 65
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'
        self.font = pygame.font.Font(path + "assets\\font\\SourceHanSans-Normal.ttc", font_size)
        if text is not None:
            self.text_surface = self.font.render(text, True, SceneFont.white_font['tc'], SceneFont.white_font['bc'])
        self.loaded = {'button': buttons, 'box': boxes}
        self.components_relative_pos = relative_pos
        self.abs_pos = relative_pos  # 控制滚轮别把控件滚到有的没的地方
        """计算组件相对位置"""
        if self.loaded['button'] is not None:
            for i in range(len(self.loaded['button'])):
                self.loaded['button'][i].rect.left = self.rect.left + \
                                                     self.components_relative_pos['button'][i][0] * self.rect.width
                self.loaded['button'][i].rect.top = self.rect.top + self.components_relative_pos['button'][i][1] * self.rect.height
        if self.loaded['box'] is not None:
            for j in range(len(self.loaded['box'])):
                self.loaded['box'][j].boxBody.left = self.rect.left + self.components_relative_pos['box'][j][0] * self.rect.width
                self.loaded['box'][j].boxBody.top = self.rect.top + self.components_relative_pos['box'][j][1] * self.rect.height
        # 协调控制输入框
        self.box_is_able = True
        self.switcher = 0

        # 滚动条协调
        self.has_scrollbar = has_scrollbar
        if self.has_scrollbar:
            settings = Settings(path)
            sb_left = self.rect.left + self.rect.width - 15
            print(self.rect.top, self.rect.height)
            self.scrollbar = ScrollBar([sb_left, self.rect.top, self.rect.height], settings)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        width, height = self.text_surface.get_size()
        if self.text_pos == 1:
            left = self.rect.left + int((self.rect.width - width) / 2)
            top = self.rect.top + int((self.rect.height - height) / 2)
        elif self.text_pos == 0:
            left = self.rect.left + int((self.rect.width - width) / 2)
            top = self.rect.top + 20
        screen.blit(self.text_surface, (left, top))
        if self.loaded['button'] is not None:
            self.loaded['button'][0].render(screen)
            for i in range(len(self.loaded['button'])):
                if self.rect.top < self.loaded['button'][i].rect.top < self.rect.top + self.rect.height - self.loaded['button'][i].rect.height:
                    self.loaded['button'][i].render(screen)
        if self.loaded['box'] is not None:
            for j in range(len(self.loaded['box'])):
                if self.rect.top < self.loaded['box'][j].boxBody.top < self.rect.top + self.rect.height - self.loaded['box'][j].boxBody.height:
                    self.loaded['box'][j].render(screen)
        if self.has_scrollbar:
            self.scrollbar.render(screen)

    def update(self, e):
        if self.loaded['button'] is not None:
            for bt in self.loaded['button']:
                bt.update(e)
        if self.loaded['box'] is not None and self.box_is_able:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button != 4 and e.button != 5:
                for i in range(len(self.loaded['box'])):
                    if self.loaded['box'][i].boxBody.collidepoint(e.pos):  # 若按下鼠标且位置在文本框
                        self.loaded['box'][i].switch()
                        self.switcher = i
                    else:
                        self.loaded['box'][i].active = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    for m in self.loaded['box']:
                        m.active = False
                    self.switcher = (self.switcher + 1) % len(self.loaded['box'])
                    self.loaded['box'][self.switcher].active = True
            for bx in self.loaded['box']:
                bx.deal_event(e)
        if self.has_scrollbar:
            if e.type == pygame.MOUSEWHEEL:
                if e.y > 0 and self.scrollbar.ratio >= 0:
                    if self.loaded['button'] is not None:
                        for i in range(1, len(self.loaded['button'])):
                            self.loaded['button'][i].rect.top += 20
                    if self.loaded['box'] is not None:
                        for j in range(len(self.loaded['box'])):
                            self.loaded['box'][j].boxBody.top += 20
                elif e.y < 0 and self.scrollbar.ratio <= 1:
                    if self.loaded['button'] is not None:
                        for i in range(1, len(self.loaded['button'])):
                            self.loaded['button'][i].rect.top -= 20
                    if self.loaded['box'] is not None:
                        for j in range(len(self.loaded['box'])):
                            self.loaded['box'][j].boxBody.top -= 20

            self.scrollbar.deal_event(e)
