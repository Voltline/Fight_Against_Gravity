"""地图类"""
import json
from pygame import Vector2

from content.maps.spawn_info import SpawnInfo
"""
map_info:{
    'planets_info':[
        {
            'locx' : float
            'locy' : float
            'spdx' : float
            'spdy' : float
            'mass' : float
            'index': int
            'ratio': float
        },
        {
            'locx' : float
            'locy' : float
            'spdx' : float
            'spdy' : float
            'mass' : float
            'index': int
            'ratio': float
        }
    ],
    'ships_info': [
        {
            'locx' : float
            'locy' : float
            'spdx' : float
            'spdy' : float
        }, 
        { 
            'locx' : float
            'locy' : float
            'spdx' : float
            'spdy' : float
        }, 
        { 
            'locx' : float
            'locy' : float
            'spdx' : float
            'spdy' : float
        }
    ]
}
"""


class Map:
    """游戏地图"""
    maps_info = dict()  # 需要调用load_maps()初始化

    def __init__(self, map_name: str):
        map_info = Map.maps_info[map_name]
        self.name = map_name
        self.planets_info = []  # 里面的元素是SpawnInfo对象
        self.ships_info = []
        for planet_info in map_info['planets_info']:
            loc = Vector2(planet_info['locx'], planet_info['locy'])
            spd = Vector2(planet_info['spdx'], planet_info['spdy'])
            mass = planet_info['mass']
            index = planet_info['index']
            ratio = planet_info['ratio']
            self.planets_info.append(SpawnInfo(loc, spd, mass=mass, index=index, ratio=ratio))
        for ship_info in map_info['ships_info']:
            loc = Vector2(ship_info['locx'], ship_info['locy'])
            spd = Vector2(ship_info['spdx'], ship_info['spdy'])
            angle = ship_info['angle']
            self.ships_info.append(SpawnInfo(loc, spd, angle=angle))

    @staticmethod
    def load_maps():
        with open('./content/maps/maps.json', 'r', encoding='utf-8') as f:
            Map.maps_info = json.load(f)
