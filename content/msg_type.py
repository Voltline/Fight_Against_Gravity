import enum


class MsgType(enum.Enum):
    """
    传输时,msg={
        "type":msg_type(int)
        "args":msg_args(list)
        "kwargs":msg_kwargs(dict)
    }
    同时不包含复杂数据结构
    """
    # 客户端接收信息
    # msg_args=[space_objs_msg]
    SpaceObjs = 0

    # 客户端接收信息
    # msg_args=[planets_msg]
    Planets = 1

    # 客户端接收信息
    # msg_args=[ships_msg, dead_ships_msg]
    Ships = 2

    # 客户端接收信息
    # msg_args=[bullets_msg]
    Bullets = 3

    # 客户端接收信息
    # msg_kwargs={'planets':planets_msg,'ships':ships_msg,'dead_ships':dead_ships_msg,'bullets':bullets_msg}
    AllObjs = 4

    # 服务端接收信息
    # msg_args=[room_id, map_name, player_names]
    StartGame = 5

    # 服务端接收信息
    # msg_args=[room_id, player_name, is_go_ahead, is_go_back, is_turn_left, is_turn_right, is_fire]
    PlayerControl = 6
