# Animation class for one play only

from pygame import image
from VARIABLES import Game

class EffectAnimation:
    pool_size = 10

    def __init__(self, json: dict) -> None:
        self.frames = []
        self.framerate = None
        self.num_frames = None
        self.pool = []
        self.json = json
    

    def load(self):
        for frame in self.json["frames"]:
            self.frames.append(image.load(frame))
        
        self.framerate = self.json["fps"]
        self.num_frames = len(self.frames)

        for n in range(EffectAnimation.pool_size):
            self.pool.append(Effect())


    def update(self, win: object):
        # Update every effect currently playing
        for effect in self.pool:
            if effect.live:
                # incrementing tick first because 0 % fps == 0
                effect.tick += 1

                if effect.tick % int(Game.FPS / self.framerate) == 0:
                    effect.onframe += 1

                if effect.onframe == self.num_frames:
                    effect.die()

                else:
                    win.blit(self.frames[effect.onframe], effect.pos)

    
    def play_effect(self, pos: tuple) -> None:
        self.pool[0].use(pos)
        self.pool = self.pool[1:] + self.pool[:1]


class Effect:
    def __init__(self):
        self.pos = (0, 0)
        self.tick = 0
        self.onframe = 0
        self.live = False

    
    def use(self, pos):
        self.pos = pos
        self.live = True
        self.tick = 0
        self.onframe = 0
        
    
    def die(self):
        self.live = False
        self.tick = 0
        self.onframe = 0