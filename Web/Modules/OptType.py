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
    creatRoom = 11
    """
    用户创建房间
    {
        "opt" : 11
        "user" : "str"
        "status" : "ACK"/"NAK"
        "roomid" : int
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


if __name__ == "__main__":
    print(OptType.login)
