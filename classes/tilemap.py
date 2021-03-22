# Tilemap class

from utility.files import load_json
from pygame import image
from VARIABLES import Game

class Tilemap:

    tilesize = Game.TILESIZE

    def __init__(self, filename: str) -> None:
        self.tilemap = load_json(filename)
        self.tile_images = [image.load(x[1]) for x in self.tilemap]


    def update(self, win):
        for t in range(len(self.tilemap)):
            win.blit(self.tile_images[t], (self.tilemap[t][2], self.tilemap[t][3]))
