# Vector class

from math import sqrt

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y

    def mult(self, other):
        self.x *= other.x
        self.y *= other.y

    def div(self, other):
        self.x /= other.x
        self.y /= other.y

    def normalize(self):
        hyp = sqrt(self.x**2 + self.y**2)
        self.x /= hyp
        self.y /= hyp

    def zero(self):
        self.x = 0
        self.y = 0

    def get_mag(self):
        return sqrt(self.x**2 + self.y**2)

    @staticmethod
    def dist(a, b):
        dx = a.x - b.x
        dy = a.y - b.y
        return sqrt(dx * dx + dy * dy)