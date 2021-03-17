# Bullet class

from utility.vector import Vector
from utility.files import load_json
from VARIABLES import Game
from pygame import image
from classes.animation import EffectAnimation

explosion_effect = EffectAnimation(load_json("./src/effects/bullet_explosion.json"))

def load():
    explosion_effect.load()
    s1 = image.load("./src/bullet/bullet-left.png").convert_alpha()
    s2 = image.load("./src/bullet/bullet-right.png").convert_alpha()
    Bullet.sprites = [s1, s2]


def update_bullets(win, collision_map):
    for b in Bullet.bullets:
        b.update(win, collision_map)


def init_bullets():
    for _ in range(Game.BULLET_CAP):
        Bullet((0, 0), 1)


class Bullet:
    # Using pool method because of lag when deleting bullets
    bullets = []
    sprites = []
    live_bullets = 0

    w = Game.TILESIZE
    h = Game.TILESIZE

    def __init__(self, pos: tuple, dir: int) -> None:
        self.pos = Vector(pos[0], pos[1])
        self.dir = dir

        self.state = False
        Bullet.bullets.append(self)


    def update(self, win, collision_map):
        if self.state:
            self.pos.x += Game.BULLET_SPEED * self.dir

            if self.pos.x > Game.WIDTH or self.pos.x < 0:
                self.die()
            
            if self.dir == -1:
                win.blit(Bullet.sprites[0], (self.pos.x, self.pos.y))
            else:
                win.blit(Bullet.sprites[1], (self.pos.x, self.pos.y))
            
            # check collision with collision map
            for tile in collision_map:
                if tile[0] != 2:
                    if abs(self.pos.x - tile[2]) < Game.TILESIZE and abs(self.pos.y - tile[3]) < Game.TILESIZE:
                        explosion_effect.play_effect((self.pos.x + Game.TILESIZE/2 * self.dir, self.pos.y))
                        self.die()
    

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
