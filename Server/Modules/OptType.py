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
        “id” : 1/2/3 tcp连接,udp连接,登陆成功
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
        "user": "str"
        "email": "str"
    }
    """
    sendAllInformation = 5
    """
    用户发送所有注册信息
    {
        "opt" : 5
        "user": "str"
        "email": "str"
        "password": "str"
    }
    """
    resetSendEmail = 6
    """
    用户重置密码请求发送验证码
    {
        "opt" ：6
        "user" : "str"
        "email" : "str"
    }
    """
    resetSendPassword = 7
    """
    用户重置密码修改密码
    {
        "opt" ：7
        "user" : "str"
        "email" : "str"
        "password" : "str"
    }
    """
    logout = 10
    """
    用户登出游戏
    {
        "opt" = 10
        "user" : str
        "roomid" : str
        "status" : "ACK"/"NAK"
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
        "roomid" : "str"
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
    getRoomlist = 15
    """
    {
        "opt" : 15
        "length" : int
        "id" : int
        "roomlist" : {
            "roomid": uuid(str),
            "owner": 房主名(str),
            "size": 玩家人数(int),
            "started": 是否在游戏中(True/False),
            "roommap" : 地图名(str),
            "roomname" : 房间名(str)
        }
    }
    """
    startgame = 16
    """
    {
        "opt" : 16
        "user" : "str"
        "roomid" : "id"
        "status" : "ACK" / "NAK“
    }
    """
    changemap = 17
    """
    房主更改游戏地图
    {
        "opt" : 17
        "user" : "str"
        "roomid" : "id"
        “roommap” : "str"
        "status" : "ACK" / "NAK“
    }
    """
    userready = 18
    """
    玩家准备完毕/取消准备
    {
        “opt” ： 18
        "user" : "str"
        "roomid" : "id"
        "ready" : "YES" / “NO”
        "status" : "ACK" / "NAK“
    }
    """
    getRoom = 19
    """
    获取单个房间信息
    {
        "opt" : 19
        "user" : "str"
        "roomid" : "id“
        "status" : "ACK" / "NAK"
        "room" : {
            roomid : "str"
            roomname : "str"
            owner: "str"
            roommap: "str"
            is_run: bool
            userlist : {
                user:ready
            }
        }
    }
    """
    changeroomname = 41
    """
    用户更改房间名
    {
        "opt" : 41
        "user" : "str"
        "roomid" : "id"
        "new_roomname" : "str"
        "status" : "ACK"/”NAK“
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
    # msg_args=space_objs_msg
    SpaceObjs = 20

    # 客户端接收信息：所有星球信息
    # msg_args=planets_msg
    Planets = 21

    # 客户端接收信息：所有飞船信息
    # msg_args=[ships_msg, dead_players_name]
    AllShips = 22

    # 客户端接收信息：所有子弹信息
    # msg_args=bullets_msg
    Bullets = 23

    # 客户端接收信息：要增删的子弹信息
    # msg_args=[new_bullets_msg, dead_bullets_msg]
    AddDelBullets = 24

    # 客户端接收信息：所有objs信息
    # msg_args=[[ships_msg, dead_players_name],[new_bullets_msg, dead_bullets_msg]]
    AllObjs = 25

    # 服务端接收信息：开始游戏
    # msg_args=[room_id, map_name, player_names]
    StartGame = 26

    # 服务端接收信息：结束游戏
    # msg_args=[room_id]
    StopGame = 27

    # 服务端接收信息：玩家控制信息
    # msg_args=[room_id, player_name, [is_go_ahead, is_go_back, is_turn_left, is_turn_right, is_fire]]
    PlayerCtrl = 28

    # 客户端和服务端都接收，校对时间
    # msg_args=[room_id, player_name]
    CheckClock = 29

    # 客户端接收，服务器真正开始游戏的时间
    # 服务器接收，给客户端发送服务器开始游戏的时间
    # msg_args=[room_id]
    ServerStartGameTime = 30

    # 客户端接收，在线游戏结束与获胜者
    # msg_args=[win_player]
    GameWin = 31

    # 客户端接收，记录发出与接收时的时间差作为延迟
    # 服务器接收，给客户端发回这个包
    # msg_args=[]
    PingTest = 32


if __name__ == "__main__":
    print(OptType.login)
