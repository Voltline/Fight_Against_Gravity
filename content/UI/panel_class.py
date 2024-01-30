import pygame
import os
import sys
from content.scene.scene_font import SceneFont
from content.UI.button_class import Control


class Panel(Control):
    def __init__(self, rect, text, font_size, ctrlrs=[], boxes=[], others=[], text_pos=1, border_radius=15):
        """
        rect: 一个四元组，text:panel要显示的文字，
        ctrlrs: panel里的能点击的控件，列表形式(如button)
        boxes: panel里的输入框组件，列表形式,
        others：panel里不能点击的控件，如label
        relative_pos: 组件相对于panel的比例,值为二维列表的字典形式.二维数组第一个值为横向比例，第二个值为纵向比例
        text_pos: 文字在panel中的位置，0靠上，1居中，2靠下
        """
        # 在panel里面画一个surface，把panel的surface画到screen
        super().__init__(rect, None, 0, '', None)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.color_key = (1, 1, 1)
        self.surface.set_colorkey(self.color_key)  # 默认(1,1,1)为透明
        self.surface.fill(self.color_key)
        self.text_pos = text_pos
        self.border_radius = border_radius
        self.color = (43, 43, 43)  # 65；如果需要panel背景透明就把color设成（0,0,0）
        if hasattr(sys, 'frozen'):
            path = os.path.dirname(sys.executable) + '/'
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '/'
        self.font = pygame.font.Font(path + "assets/font/SourceHanSans-Normal.ttc", font_size)
        if text is not None:
            self.text_surface = self.font.render(text, True, SceneFont.white_font['tc'], SceneFont.white_font['bc'])
        self.loaded = {'ctrlrs': ctrlrs, 'boxes': boxes, 'others': others}
        # 计算组件相对位置
        for objs in self.loaded.values():
            for obj in objs:
                obj.rect.left = obj.r_xy[0]*self.rect.width
                obj.rect.top = obj.r_xy[1]*self.rect.height
        # 协调控制输入框
        self.box_is_able = True
        self.switcher = 0

    def render(self, screen: pygame.Surface):
        """把东西画到panel上，再把panel画到screen上"""
        if self.is_show:
            pygame.draw.rect(self.surface, self.color,
                             pygame.Rect(0, 0, self.rect.width, self.rect.height), border_radius=self.border_radius)
            width, height = self.text_surface.get_size()
            if self.text_pos == 1:
                left = int((self.rect.width - width) / 2)
                top = int((self.rect.height - height) / 2)
            else:  # self.text_pos == 0
                left = int((self.rect.width - width) / 2)
                top = 20
            self.surface.blit(self.text_surface, (left, top))
            for objs in self.loaded.values():
                for obj in objs:
                    obj.render(self.surface)
            screen.blit(self.surface, self.rect)

    def update(self, event, pos_offset=(0, 0)) -> bool:
        if not self.is_able:
            return False
        pos_offset0 = pos_offset  # 判断自己时的偏移量
        pos_offset = (self.rect[0]+pos_offset[0], self.rect[1]+pos_offset[1])  # 判断自己的元素时的偏移量
        if self.deal_event_mouse(event, pos_offset, pos_offset0):
            return True
        self.deal_event_key(event)
        return False

    def deal_event_mouse(self, event, pos_offset=(0, 0), pos_offset0=(0, 0)) -> bool:
        """处理鼠标事件"""
        if self.is_able and self.is_over(pygame.mouse.get_pos(), pos_offset0):
            for bt in self.loaded['ctrlrs'][::-1]:
                if bt.update(event, pos_offset):
                    return True
            if self.box_is_able and event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.loaded['boxes'])):
                    if self.loaded['boxes'][i].check_click(event, pos_offset):  # 若按下鼠标且位置在文本框
                        self.loaded['boxes'][i].active = True
                        self.switcher = i
                    else:
                        self.loaded['boxes'][i].active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        self.update_mouse_motion(event, pos_offset0)
        return False

    def update_mouse_motion(self, event, pos_offset=(0, 0)):
        pos_offset = (self.rect[0]+pos_offset[0], self.rect[1]+pos_offset[1])
        for bt in self.loaded['ctrlrs'][::-1]:
            if hasattr(bt, 'update_mouse_motion'):
                bt.update_mouse_motion(event, pos_offset)

    def deal_event_key(self, event):
        """处理键盘事件"""
        if self.loaded['boxes'] is not None and self.box_is_able:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    for m in self.loaded['boxes']:
                        m.active = False
                    self.switcher = (self.switcher + 1) % len(self.loaded['boxes'])
                    self.loaded['boxes'][self.switcher].active = True
            for bx in self.loaded['boxes']:
                bx.deal_event(event)
