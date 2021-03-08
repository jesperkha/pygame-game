# Gun class

from utility.vector import Vector
from pygame import image, transform
from VARIABLES import Game
from utility.animation import AnimationPlayer


class Gun:
    def __init__(self, size: tuple, offset: int, sprite_path: str, animation_path: str, num_frames: int, recoil: int):
        s = transform.scale(image.load(sprite_path).convert_alpha(), size)
        self.sprite = [s, transform.flip(s, True, False)]

        self.w = size[0]
        self.h = size[1]
        self.offset = offset

        self.mag_size = Game.MAG_SIZE
        self.recoil = recoil

        self.ANIMATING = False
        self.animation_player = AnimationPlayer(animation_path, num_frames, 15, size)
    

    def update(self, player_size, pos, dir, win):
        x = (pos.x - self.w/2 + player_size.x/2) + (self.w/self.h * self.offset) * dir
        y = pos.y - self.h/2 + player_size.y/2

        if self.ANIMATING:
            sprite = self.animation_player.animate(dir, True)
            if sprite:
                win.blit(sprite, (x, y))
            else:
                self.ANIMATING = False
        
        # New if startement to not skip over drawing after finished animation
        if not self.ANIMATING:
            if dir == 1:
                win.blit(self.sprite[0], (x, y))
            else:
                win.blit(self.sprite[1], (x, y))

    
    def shoot(self):
        self.ANIMATING = True
        self.animation_player.reset()
