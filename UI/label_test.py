import pygame
from Label_Class import Label
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 0))
font_info1 = {
    'font': pygame.font.Font("Fight_Against_Gravity/UI/Font/SourceHanSans-Normal.ttc", 50),
    'tc': (255, 255, 255),
    'bc': (0, 0, 0),
    'align': 0,
    'valign': 0
}
mylabel = Label(100, 100, "First 我的label", font_info1)

print("获取系统中所有可用字体", pygame.font.get_fonts())
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        mylabel.render(screen)
        pygame.display.flip()
