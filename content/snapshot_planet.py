from pygame import Vector2


class SnapshotPlanet:
    """snapshot专用的简化版的planet"""
    def __init__(self, mass: float, loc: Vector2):
        self.mass = mass
        self.loc = loc.copy()
