class ObjMsg:
    """传输的太空对象信息"""

    R = 4  # 保留的小数位数

    def __init__(self, obj=None, msg=None):
        """
        obj:SpaceObj 各类太空对象，从太空对象中获取数据
        msg:list 传输的消息，从消息中获取数据
        """
        if obj:
            self.locx = obj.loc.x
            self.locy = obj.loc.y
            self.spdx = obj.spd.x
            self.spdy = obj.spd.y
            self.accx = obj.acc.x
            self.accy = obj.acc.y
            if hasattr(obj, 'angle'):  # 如果是飞船消息(这样子判断是为了避免循环import)
                self.angle = obj.angle
                self.hp = obj.hp
                self.player_name = obj.player_name

        elif msg:
            self.locx = msg[0]
            self.locy = msg[1]
            self.spdx = msg[2]
            self.spdy = msg[3]
            self.accx = msg[4]
            self.accy = msg[5]
            if len(msg) == 9:  # 如果是飞船消息
                self.angle = msg[6]
                self.hp = msg[7]
                self.player_name = msg[8]

    @staticmethod
    def init(settings):
        ObjMsg.R = settings.obj_msg_r

    def make_msg(self):
        """生成用于传输的消息"""
        msg = []
        for num in self.locx, self.locy, self.spdx, self.spdy, self.accx, self.accy:
            msg.append(round(num, ObjMsg.R))
        # msg = [locx, locy, spdx, spdy, accx, accy]
        try:
            msg.append(round(self.angle, ObjMsg.R))
            msg.append(self.hp)
            msg.append(self.player_name)
        except AttributeError as e:
            pass
        finally:
            return msg


if __name__ == '__main__':
    msg = [0, 1, 2, 3, 4, 5]
    obj_msg = ObjMsg(msg=msg)
    print(obj_msg)
