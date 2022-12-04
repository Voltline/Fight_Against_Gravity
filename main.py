"""程序入口"""
import pygame

import content.game_function as gf
from fight_against_gravity import local_game
from local_game import LocalGame
from all_settings import Settings

"""
游戏操作：
wasd：玩家1的移动
e：玩家1的发射子弹
ijkl：玩家2的移动
u：玩家2的发射子弹u

按住鼠标右键并拖动：移动视角（视角自由移动模式下可用）
鼠标中键：切换视角模式（自由移动模式or跟随飞船模式）
鼠标滚轮：视角缩放
"""

# local_game()

settings = Settings()  # 初始化设置类
screen = gf.init_pygame_window(settings)
game = LocalGame(settings, screen, '静止双星系统')
game.main()
