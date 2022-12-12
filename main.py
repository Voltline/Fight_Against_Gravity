"""程序入口"""
import sys
import os
path = os.path.dirname(os.path.realpath(__file__)) + '\\'
sys.path.append(path)

from Server import server_main
import content.game.game_function as gf
from content.game.local_game import LocalGame
from settings.all_settings import Settings

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
#TODO:path
if len(sys.argv) == 2 and sys.argv[1] == "--server":
    s = server_main.ServerMain()
    s.start()
else:
    settings = Settings(path)  # 初始化设置类
    screen = gf.init_pygame_window(settings)
    game = LocalGame(settings, screen, '征途')
    game.main()
