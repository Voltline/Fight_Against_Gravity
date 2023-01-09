import sys
import os

path = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(path)
from Server import server_main
from settings.all_settings import Settings
import content.game_modules.game_function as gf
from content.space_objs.ship import Ship

settings = Settings(path)  # 初始化设置类
_debug_ = "--debug" in sys.argv
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dsp'
gf.init_pygame_window()
Ship.init(settings)
s = server_main.ServerMain(game_settings=settings, path=path, _debug_=_debug_)
# try:
s.start()
# except Exception as err:
#     print(err)
#     raise Exception(err)
del os.environ['SDL_VIDEODRIVER']
del os.environ['SDL_AUDIODRIVER']

"""
记一下启动脚本
frpc -
python3.py server.py --nogui
"""