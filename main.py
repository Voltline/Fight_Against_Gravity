"""程序入口"""
import sys
import os

path = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(path)
from Server import server_main
from Server import client_main
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
settings = Settings(path)  # 初始化设置类
if len(sys.argv) >= 2:
    _debug_ = "--debug" in sys.argv
    if sys.argv[1] == "--server":
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        s = server_main.ServerMain(game_settings=settings, path=path, _debug_=_debug_)
        s.start()
        del os.environ['SDL_VIDEODRIVER']
    elif sys.argv[1] == "--client":
        s = client_main.ClientMain(path, _debug_=_debug_)
        s.start()
        # check_code = s.register_get_checkcode("test_1", "541665621@qq.com")
        # input_check_code = input()
        # ps = input()
        # s.register_push_password("test_1", "541665621@qq.com", check_code, input_check_code, ps)
else:
    screen = gf.init_pygame_window(settings)
    game = LocalGame(settings, screen, '征途')
    game.main()
