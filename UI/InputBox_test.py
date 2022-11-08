import pygame
from all_settings import Settings
from InputBox_Class import InputBox
import sys
pygame.init()
s = Settings()
screen = pygame.display.set_mode((s.screen_width, s.screen_height))
inputbox = InputBox(pygame.Rect(100, 100, 140, 32))
box2 = InputBox(pygame.Rect(100, 150, 140, 32))
boxL = [inputbox, box2]
running = True
while running:
    screen.fill(s.bg_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        inputbox.deal_event(event)
        box2.deal_event(event)
    inputbox.draw(screen)
    box2.draw(screen)
    pygame.display.flip()

