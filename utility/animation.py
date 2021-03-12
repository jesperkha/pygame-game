# Animation player for easy animations

from pygame import image, transform

class AnimationPlayer:
    def __init__(self, animation_frames_path: str, num_frames: int, fps: int) -> None:
        self.num_frames = num_frames
        self.path = animation_frames_path
        self.frames = []
        
        self.framerate = int(60 / fps)
        self.tick = 0
        self.on_frame = 0

    
    def init(self):
        # Adds pygame images to frames list
        for n in range(self.num_frames):
            s = image.load(f"{self.path}{n}.png").convert_alpha()
            self.frames.append(s)

    
    def animate(self, dir: int, stop_when_done: bool = False) -> object:
        # incrementing tick first because 0 % fps == 0
        self.tick += 1

        if self.tick % self.framerate == 0:
            self.on_frame += 1

        if self.on_frame == self.num_frames:
            self.reset()
            if stop_when_done:
                return None

        if dir == -1:
            # Return flipped version for direction
            return transform.flip(self.frames[self.on_frame], True, False) 
        else:
            return self.frames[self.on_frame]


    def reset(self):
        self.on_frame = 0
        self.tick = 0