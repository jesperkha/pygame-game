# Platform class

from utility.vector import Vector
from pygame import draw, Rect


def update_platforms(win):
    for p in Platform.platforms:
        p.update(win)


class Platform:
    platforms = [] # List of platforms

    def __init__(self, pos: tuple, size: tuple, jump_through: bool = False) -> None:
        self.pos = Vector(pos[0], pos[1])
        self.size = Vector(size[0], size[1])
        self.jump_through = jump_through

        Platform.platforms.append(self)

    
    def update(self, win):
        draw.rect(win, (0, 255, 0), (self.pos.x, self.pos.y, self.size.x, self.size.y))