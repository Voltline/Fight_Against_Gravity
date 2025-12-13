import math


class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def copy(self):
        return Vec2(self.x, self.y)

    def update(self, other):
        self.x = other.x
        self.y = other.y
        return self

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, k: float):
        return Vec2(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __truediv__(self, k: float):
        return Vec2(self.x / k, self.y / k)

    def length(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return self / l

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"
