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
        "status" : "ACK"/"ACK"
        "roomid" : int
    }
    """


if __name__ == "__main__":
    print(OptType.login)
