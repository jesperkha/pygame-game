# Bullet class

from utility.vector import Vector
from VARIABLES import Game
from pygame import image

def load():
    s1 = image.load("./src/bullet/bullet-left.png").convert_alpha()
    s2 = image.load("./src/bullet/bullet-right.png").convert_alpha()
    Bullet.sprites = [s1, s2]


def update_bullets(win):
    for b in Bullet.bullets:
        b.update(win)


def init_bullets():
    for _ in range(Game.BULLET_CAP):
        Bullet((0, 0), 1)


class Bullet:
    # Using pool method because of lag when deleting bullets
    bullets = []
    sprites = []
    live_bullets = 0

    w = 16
    h = 16

    def __init__(self, pos: tuple, dir: int) -> None:
        self.pos = Vector(pos[0], pos[1])
        self.dir = dir

        self.state = False
        Bullet.bullets.append(self)


    def update(self, win):
        if self.state:
            self.pos.x += Game.BULLET_SPEED * self.dir

            if self.pos.x > Game.WIDTH or self.pos.x < 0:
                self.die()
            
            if self.dir == -1:
                win.blit(Bullet.sprites[0], (self.pos.x, self.pos.y))
            else:
                win.blit(Bullet.sprites[1], (self.pos.x, self.pos.y))
    

    def die(self):
        self.state = False
        Bullet.live_bullets -= 1


    @staticmethod
    def new(pos, size, dir, offset) -> None:
        if Bullet.live_bullets < Game.BULLET_CAP:
            # Set values
            Bullet.bullets[0].state = True

            x = (pos.x - Bullet.w/2 + size.x/2) + ((offset + Bullet.w) * dir)
            y = pos.y - Bullet.h/2 + size.y/2 - 3 # ajusting for where the barrel is
            Bullet.bullets[0].pos = Vector(x, y)
            Bullet.bullets[0].dir = dir

            Bullet.rotate()
            Bullet.live_bullets += 1

        
    @staticmethod
    def rotate():
        # Rotates list bakwards
        Bullet.bullets = Bullet.bullets[1:] + Bullet.bullets[:1]


load()
init_bullets()
