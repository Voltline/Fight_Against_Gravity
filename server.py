import sys
import os

path = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(path)
from Server import server_main
from settings.all_settings import Settings

settings = Settings(path)  # 初始化设置类
_debug_ = "--debug" in sys.argv
os.environ['SDL_VIDEODRIVER'] = 'dummy'
s = server_main.ServerMain(game_settings=settings, path=path, _debug_=_debug_)
# try:
s.start()
# except Exception as err:
#     print(err)
#     raise Exception(err)
del os.environ['SDL_VIDEODRIVER']
