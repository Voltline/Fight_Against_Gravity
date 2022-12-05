class OptType:
    """json格式数据包中的opt选项"""
    debug = -1
    """debug用的数据包"""
    heartBeat = 0
    """心跳检测包"""
    login = 1
    """
    用户请求登录
    {
        "opt" : 1
        "user" : "str"
        "password" : "str"
        "status" : "ACK"/"NAK"
    }
    """
    loginTransfer = 3
    """
    用户登录请求转发至验证服
    {
        "opt" : 3
        "user" : "str"
        "password" : "str"
    }
    """
    sendCheckCode = 4
    """
    用户发送用户名与密码请求发送验证码
    {
        "opt" : 4
        "user": "str",
        "email": "str"
    }
    """
    sendAllInformation = 5
    """
    用户发送所有注册信息
    {
        "opt" : 5
        "user": "str",
        "email": "str",
        "password": "str"
    }
    """
    creatRoom = 11
    """
    用户创建房间
    {
        "opt" : 11
        "user" : "str"
        "roomid" : int
        "roomname" : "str"
        "roommap" : "str" ("静止单星系统"/"静止双星系统")
        "status" : "ACK"/"NAK"
    }
    """
    joinRoom = 12
    """
    用户加入房间
    {
        "opt" : 12
        "user" : "str"
        "roomid" : "id"
        "status" : "ACK"/"NAK"
    }
    """
    leftRoom = 13
    """
    用户离开房间
    {
        "opt" : 13
        "user" : "str"
        "roomid" : "id"
        "status" : "ACK"/"NAK"
    }
    """
    deleteRoom = 14
    """
    用户删除房间
    {
        "opt" : 14
        "user" : "str"
        "roomid" : "id"
        "status" : "ACK" / "NAK"
    }
    """
    getRoom = 15
    """
    {
        "opt" : 15
        "roomlist" : [{
            "roomid" : roomid
            "owner" : user
            "size" : int #玩家人数
        }]
    }
    """
    startgame = 16
    """
    目前玩家房主没分开，且玩家start_game就是准备好了
    {
        "opt" : 16
        "user" : "str"
        "roomid" : "id"
        "status" : "ACK" / "NAK“
    }
    """

    """
    传输时,msg={
        "opt":msg_opt(int)
        "time":second(float)
        "tick":tick(int)
        "args":msg_args(list)
        "kwargs":msg_kwargs(dict)
    }
    同时不包含复杂数据结构
    """
    # 客户端接收信息：space_objs信息(以防万一放着，一般不使用)
    # msg_args=[space_objs_msg]
    SpaceObjs = 20

    # 客户端接收信息：所有星球信息
    # msg_args=[planets_msg]
    Planets = 21

    # 客户端接收信息：所有飞船信息
    # msg_args=[ships_msg, dead_players_name]
    AllShips = 22

    # 客户端接收信息：所有子弹信息
    # msg_args=[bullets_msg]
    Bullets = 23

    # 客户端接收信息：所有objs信息
    # msg_args=[planets_msg,[ships_msg, dead_players_name],bullets_msg]
    AllObjs = 24

    # 服务端接收信息：开始游戏
    # msg_args=[room_id, map_name, player_names]
    StartGame = 25

    # 服务端接收信息：结束游戏
    # msg_args=[room_id]
    StopGame = 26

    # 服务端接收信息：玩家控制信息
    # msg_args=[room_id, player_name, [is_go_ahead, is_go_back, is_turn_left, is_turn_right, is_fire]]
    PlayerCtrl = 27

    # 客户端和服务端都接收，校对时间
    # msg_args=[room_id, player_name]
    CheckClock = 28

    # 客户端接收，服务器真正开始游戏的时间
    # msg_args=[room_id]
    ServerStartGameTime = 29


if __name__ == "__main__":
    print(OptType.login)
