import pygame
from Label_Class import Label
from Button_class import Button
from all_settings import Settings
import sys

settings = Settings()
pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
screen.fill((0, 0, 0))
font_info1 = {
    'font': pygame.font.Font("Font/SourceHanSans-Normal.ttc", 30),
    'tc': (255, 255, 255),
    'bc': None,
    'align': 0,
    'valign': 0
}
BACK = pygame.event.custom_type()
my_label = Label(100, 100, "First 我的label", font_info1)
btn_rect = pygame.Rect(10, 10, 30, 30)
my_button = Button("back", BACK, btn_rect, "Img/b4.png", 1)
img_test = pygame.image.load("Img/b4.png").convert_alpha()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif my_button.check_click(event):
            print("back is clicked")
        screen.blit(img_test, (60, 60))
        my_label.render(screen)
        my_button.render(screen)
        pygame.display.flip()
