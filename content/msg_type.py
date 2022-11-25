import enum


class MsgType(enum.Enum):
    # msg_args=[msg_type, room_id, space_objs_msg]
    SpaceObjs = 0

    # msg_args=[msg_type, room_id, planets_msg]
    Planets = 1

    # msg_args=[msg_type, room_id, ships_msg, dead_ships_msg]
    Ships = 2

    # msg_args=[msg_type, room_id, bullets_msg]
    Bullets = 3

    # msg_args=[msg_type, room_id]
    # msg_kwargs={'planets':planets_msg,'ships':ships_msg,'dead_ships':dead_ships_msg,'bullets':bullets_msg}
    AllObjs = 4

    # msg_args=[msg_type, room_id, map_name, player_names]
    StartGame = 5
