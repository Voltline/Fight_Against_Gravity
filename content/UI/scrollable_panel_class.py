import pygame
import os
import sys
from content.scene.scene_font import SceneFont
from content.UI.scrollbar import ScrollBar
from content.UI.panel_class import Panel


class ScrollablePanel(Panel):
    def __init__(self, rect, text, font_size, ctrlrs, boxes, others, relative_pos, text_pos=1):
        """
        rect: 一个四元组，text:panel要显示的文字，
        buttons: panel里的按钮组件，列表形式
        boxes: panel里的输入框组件，列表形式,
        relative_pos: 组件相对于panel的比例,值为二维列表的字典形式.二维数组第一个值为横向比例，第二个值为纵向比例
        text_pos: 文字在panel中的位置，0靠上，1居中，2靠下
        """
        # todo: 判断是否点到panel，涉及到一个panel是否active，如果panel被点击了，再让panel里的东西进行响应
        # 在panel里面画一个surface，把panel的surface画到
        # 把东西画到panel上，再把panel画到screen上。
        super().__init__(rect, None, 0, '', None)
        self.rect = pygame.Rect(rect)
        self.surface = pygame.Surface(self.rect.width, self.rect.height)
        self.surface.set_colorkey((0, 0, 0))  # 默认黑色为透明
        self.text_pos = text_pos
        self.color = (43, 43, 43)  # 65；如果需要panel背景透明就把color设成（0,0,0）
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'
        self.font = pygame.font.Font(path + "assets\\font\\SourceHanSans-Normal.ttc", font_size)
        if text is not None:
            self.text_surface = self.font.render(text, True, SceneFont.white_font['tc'], SceneFont.white_font['bc'])
        self.loaded = {'button': ctrlrs, 'box': boxes, 'others': others}
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

    def render(self, screen, rect=pygame.Rect(0, 0, 0, 0)):
        self.surface.fill((0, 0, 0))
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=15)
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
                if self.rect.top < self.loaded['box'][j].rect.top < self.rect.top + self.rect.height - self.loaded['box'][j].rect.height:
                    self.loaded['box'][j].render(screen)
        if self.has_scrollbar:
            self.scrollbar.render(screen)

    def update(self, event, pos_offset=(0, 0)) -> bool:
        pos_offset = (self.rect[0]+pos_offset[0], self.rect[1]+pos_offset[1])
        if self.loaded['button'] is not None:
            for bt in self.loaded['button']:
                bt.update(event, pos_offset)
        if self.loaded['box'] is not None and self.box_is_able:
            for i in range(len(self.loaded['box'])):
                if self.loaded['box'][i].check_click(event, pos_offset):  # 若按下鼠标且位置在文本框
                    self.loaded['box'][i].switch()
                    self.switcher = i
                else:
                    self.loaded['box'][i].active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    for m in self.loaded['box']:
                        m.active = False
                    self.switcher = (self.switcher + 1) % len(self.loaded['box'])
                    self.loaded['box'][self.switcher].active = True
            for bx in self.loaded['box']:
                bx.deal_event(event)
        if self.has_scrollbar:
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and self.scrollbar.ratio >= 0:
                    if self.loaded['button'] is not None:
                        for i in range(1, len(self.loaded['button'])):
                            self.loaded['button'][i].rect.top += 20
                    if self.loaded['box'] is not None:
                        for j in range(len(self.loaded['box'])):
                            self.loaded['box'][j].rect.top += 20
                elif event.y < 0 and self.scrollbar.ratio <= 1:
                    if self.loaded['button'] is not None:
                        for i in range(1, len(self.loaded['button'])):
                            self.loaded['button'][i].rect.top -= 20
                    if self.loaded['box'] is not None:
                        for j in range(len(self.loaded['box'])):
                            self.loaded['box'][j].rect.top -= 20

            self.scrollbar.deal_event(event, pos_offset)
