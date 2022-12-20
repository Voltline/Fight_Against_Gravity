from content.maps.map_obj import Map
from Server.Modules.safeserver import SocketServer
from content.games.server_game import ServerGame


class GameRoom:
    """服务端的游戏房间"""
    def __init__(self, settings, net: SocketServer, room_id, map_name, player_names):
        self.settings = settings
        self.net = net
        self.id = room_id
        self.map_name = map_name
        self.map = Map(map_name)
        self.player_names = player_names
        self.addresses = {}  # {player_name: address}
        self.game = ServerGame(self.settings, self.net, self.id, self.map_name, self.player_names)
