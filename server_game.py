from online_game import OnlineGame


class ServerGame(OnlineGame):
    def __init__(self, settings, net, room_id, map_name, player_names):
        super().__init__(settings, net, room_id, map_name, player_names)
