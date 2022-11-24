"""地图类"""
import json
"""
map_info:{
    'planets_info': {
        [{
            'locx': float
            'locy': float
            'spdx': float
            'spdy': float
        },
        {
            'locx': float
            'locy': float
            'spdx': float
            'spdy': float
        }]
    }
    'spawns_info': {
        [{
            'locx': float
            'locy': float
            'spdx': float
            'spdy': float
        },
        {
            'locx': float
            'locy': float
            'spdx': float
            'spdy': float
        },
        {
            'locx': float
            'locy': float
            'spdx': float
            'spdy': float
        }]
    }
}
"""


class Map:
    """游戏地图"""
    maps = dict()

    def __init__(self, map_name: str):
        map_info = Map.maps[map_name]
        planets_info = map_info['planets_info']


    @staticmethod
    def load_maps():
        with open('maps.json', 'r') as f:
            Map.maps = json.load(f)
