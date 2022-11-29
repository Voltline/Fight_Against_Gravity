"""标记消息类型的类，便于维护"""


class MsgType:
    """
        传输时,msg={
            "type":msg_type(int)
            "time":second(float)
            "args":msg_args(list)
            "kwargs":msg_kwargs(dict)
        }
        同时不包含复杂数据结构
    """
    # 客户端接收信息：space_objs信息(以防万一放着，一般不使用)
    # msg_args=[space_objs_msg]
    SpaceObjs = 0

    # 客户端接收信息：所有星球信息
    # msg_args=[planets_msg]
    Planets = 1

    # 客户端接收信息：所有飞船信息
    # msg_args=[ships_msg, dead_players_name]
    AllShips = 2

    # 客户端接收信息：所有子弹信息
    # msg_args=[bullets_msg]
    Bullets = 3

    # 客户端接收信息：所有objs信息
    # msg_args=[planets_msg,[ships_msg, dead_players_name],bullets_msg]
    AllObjs = 4

    # 服务端接收信息：开始游戏
    # msg_args=[room_id, map_name, player_names]
    StartGame = 5

    # 服务端接收信息：结束游戏
    # msg_args=[room_id]
    StopGame = 6

    # 服务端接收信息：玩家控制信息
    # msg_args=[room_id, player_name, [is_go_ahead, is_go_back, is_turn_left, is_turn_right, is_fire]]
    PlayerCtrl = 7

    # 客户端和服务端都接收，校对时间
    # msg_args=[room_id, player_name]
    CheckClock = 8

    # 客户端接收，服务器真正开始游戏的时间
    # msg_args=[room_id]
    ServerStartGameTime = 9
