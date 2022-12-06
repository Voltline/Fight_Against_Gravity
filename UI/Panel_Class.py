import pygame


class Panel:
    def __init__(self):
        self.rect = (300, 150, 600, 400)
        self.color = (46, 46, 46)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
