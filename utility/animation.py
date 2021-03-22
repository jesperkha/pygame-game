# Animation player for easy animations

from pygame import image, transform
from VARIABLES import Game

class AnimationPlayer:
    def __init__(self, json: dict) -> None:
        self.num_frames = json["num_frames"]
        self.path = json["path"]
        self.frames = []
        
        self.framerate = int(60 / json["fps"])
        self.tick = 0
        self.on_frame = 0

    
    def load(self):
        # Adds pygame images to frames list
        for n in range(self.num_frames):
            s = image.load(f"{self.path}{n}.png").convert_alpha()
            self.frames.append(s)

    
    def animate(self, dir: int, stop_when_done: bool = False, no_flip: bool = False) -> object:
        # incrementing tick first because 0 % fps == 0
        self.tick += 1

        if self.tick % self.framerate == 0:
            self.on_frame += 1

        if self.on_frame == self.num_frames:
            self.reset()
            if stop_when_done:
                return None

        if no_flip:
            dir = 1

        if dir == -1:
            # Return flipped version for direction
            return transform.flip(self.frames[self.on_frame], True, False) 
        else:
            return self.frames[self.on_frame]


    def reset(self):
        self.on_frame = 0
        self.tick = 0


# EFFECTS --------------------------------------------------------- #

# Animation class for one play only

def update_effects(win):
    for e in EffectAnimation.effects:
        e.update(win)
        

class EffectAnimation:
    pool_size = 10
    effects = []

    def __init__(self, json: dict) -> None:
        self.frames = []
        self.framerate = None
        self.num_frames = None
        self.pool = []
        self.json = json

        EffectAnimation.effects.append(self)
    

    def load(self):
        for n in range(self.json["num_frames"]):
            self.frames.append(image.load(f"{self.json['path']}{n}.png"))
        
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