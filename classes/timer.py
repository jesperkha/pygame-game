# Timer object
from pygame import image
from VARIABLES import Game

class GameTimer:
    def __init__(self) -> None:
        self.time = 0
        self.tick = 0

        self.nums = {}
        for n in range(10):
            self.nums[str(n)] = image.load(f"./src/chars/{n}.png")

        self.colon = image.load("./src/chars/colon.png")

    
    def update(self, win):
        self.tick += 1

        if self.tick == Game.FPS:
            self.tick = 0
            self.time += 1 # seconds

        display_time = self.convert_to_minutes_and_seconds()
        space = 7

        pos = [Game.WIDTH - 5*space - 16, 16]
        
        # Display minutes
        if len(display_time[0]) == 1:
            win.blit(self.nums["0"], pos)
            pos[0] += space

        for min in display_time[0]:
            win.blit(self.nums[min], pos)
            pos[0] += space

        # Display seperation colon
        win.blit(self.colon, pos)
        pos[0] += space

        # Display seconds
        if len(display_time[1]) == 1:
            win.blit(self.nums["0"], pos)
            pos[0] += space

        for sec in display_time[1]:
            win.blit(self.nums[sec], pos)
            pos[0] += space
        
    
    def convert_to_minutes_and_seconds(self):
        seconds = self.time % 60
        minutes = int(self.time // 60)
        return (str(minutes), str(seconds))