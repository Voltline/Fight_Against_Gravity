class User:
    """
    玩家类 存储玩家信息 包括address name 房间号
    """

    def __init__(self, add, name: str):
        self.address = add
        self.udp_address = None
        self.name = name
        self.isready = False
        self.roomid = None

    def set_udp_address(self, add):
        self.udp_address = add

    def get_udp_address(self):
        return self.udp_address

    def set_roomid(self, roomid):
        self.roomid = roomid

    def get_roomid(self):
        return self.roomid

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_ready(self) -> bool:
        return self.isready

    def ready(self):
        self.isready = True

    def isready(self):
        return self.isready()

    def dready(self):
        self.isready = False
