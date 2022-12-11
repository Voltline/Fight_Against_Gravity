import pygame
from scene_font import SceneFont


class Panel:
    def __init__(self, rect, text, font_size, clicked_function):
        """rect:一个四元组，text:panel要显示的文字，is_clicked，panel被点击后要执行的函数名"""
        self.rect = pygame.Rect(rect)
        self.color = (46, 46, 46)
        self.font = pygame.font.Font("UI/Font/SourceHanSans-Normal.ttc", font_size)
        if text is not None:
            self.text_surface = self.font.render(text, True, SceneFont.r_font['tc'], SceneFont.r_font['bc'])
        self.is_clicked = clicked_function

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        width, height = self.text_surface.get_size()
        left = self.rect.left + int((self.rect.width-width)/2)
        top = self.rect.top + int(height/2)
        screen.blit(self.text_surface, (left, top))

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN:
            pass

    def update(self, event):
        if self.check_click(event):
            self.is_clicked()

