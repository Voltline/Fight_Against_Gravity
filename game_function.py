import sys
import pygame


def check_events_keydown(event):
    """处理按下按键"""


def check_events_keyup(event):
    """处理松开按键"""


def check_events(settings, gm):
    """响应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        elif event.type == pygame.KEYDOWN:
            check_events_keydown(event)
        elif event.type == pygame.KEYUP:
            check_events_keyup(event)


def update_screen(settings, screen, gm):
    """更新屏幕"""
    # 重新绘制
    screen.fill(settings.bg_color)

    # 刷新屏幕
    pygame.display.flip()

