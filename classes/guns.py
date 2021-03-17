# Gun class

from utility.vector import Vector
from pygame import image, transform
from VARIABLES import Game
from utility.animation import AnimationPlayer
from utility.files import load_json


class Gun:
    def __init__(self, json: dict):
        self.json = json
        self.sprite = None

        self.w = json["width"]
        self.h = json["height"]
        self.offset = json["offset"]

        self.mag_size = Game.MAG_SIZE
        self.recoil = json["recoil"]

        self.ANIMATING = False
        self.animation_player = AnimationPlayer(json["animation_path"], json["frames"], 15)

    
    def load(self):
        s = image.load(self.json["sprite_path"]).convert_alpha()
        self.sprite = [s, transform.flip(s, True, False)]
        self.animation_player.load()
    

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



# Types of guns ------------------------------------------------ #

class Pistol(Gun):
    def __init__(self):
        super().__init__(load_json("./main.json")["items"]["pistol"])
