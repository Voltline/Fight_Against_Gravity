from content.online.snapshot_planet import SnapshotPlanet as SPlanet


class Snapshot:
    """
    用于本地预测而保存的过去一段时间每一tick的游戏状态
    存planets,player_ctrl_msg是为了方便计算
    存ships和bullets是为了方便比对
    """
    def __init__(self, gm, tick: int):
        self.tick = tick
        self.splanets = []  # 所有星球
        self.ships_loc = {}  # 所有活着的飞船位置 {player_name:loc}
        self.ships_angle = {}  # 所有活着的飞船角度 {player_name:angle}
        self.ships_hp = {}  # 所有活的飞船的血量 {player_name:angle}
        self.ships_ctrl_msg = {}  # 所有活着的飞船的控制信息 {player_name:ctrl_msg}
        self.bullets_loc = {}  # 所有子弹 {id:loc}
        for planet in gm.planets:
            self.splanets.append(SPlanet(planet.mass, planet.loc))
        for ship in gm.ships:
            self.ships_loc[ship.player_name] = ship.loc.copy()
            self.ships_angle[ship.player_name] = ship.angle
            self.ships_hp[ship.player_name] = ship.hp
            self.ships_ctrl_msg[ship.player_name] = ship.make_ctrl_msg()
        for bullet in gm.bullets:
            self.bullets_loc[bullet.id] = bullet.loc.copy()
