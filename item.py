# Item class

from pygame import image
from utility.vector import Vector
from VARIABLES import Game
from random import randrange


def update_items(win):
    for i in Item.items:
        i.update(win)


def create_item():
    if Item.collision_map and not Item.items[0].LIVE:
        Item.items[0].spawn()
        # rotate list
        Item.items = Item.items[1:] + Item.items[:1]


def load_items():
    for n in range(1):
        Item(f"./src/items/item{n}.png", n + 1)


class Item:

    items = []
    collision_map = None

    def __init__(self, img_src, type) -> None:
        self.sprite = image.load(img_src)
        self.type = type
        self.pos = Vector(0, 0)

        self.grv = 0.15
        self.vel = 0

        self.landing_spot = 0
        self.bounce = 0

        self.LIVE = False
        Item.items.append(self)
    

    # Finds the ground beneath to stop at instead of searching all tiles
    def find_landing_spot(self):
        legal_tiles = [
            "./src/collisionmap/0.png",
            "./src/collisionmap/1.png",
            "./src/collisionmap/2.png",
        ]

        possible_locations = []

        # Finds all legal spwaning loacations
        for tile in Item.collision_map:
            if tile[1] in legal_tiles:
                possible_locations.append((tile[2], tile[3]))
        
        # Returns a random tile from list
        random_index = randrange(0, len(possible_locations))
        return possible_locations[random_index]

    
    def spawn(self):
        self.LIVE = True
        self.vel = 2
        self.bounce = 0

        new_location = self.find_landing_spot()
        self.landing_spot = new_location[1]

        self.pos.x = new_location[0]
        self.pos.y = new_location[1]

        self.pos.y -= Game.TILESIZE * 4

    
    def die(self):
        self.LIVE = False
        self.pos.x = -100

    
    def update(self, win):
        if self.LIVE:
            self.pos.y += self.vel
            self.vel += self.grv

            if self.pos.y + Game.TILESIZE > self.landing_spot:
                if self.bounce < 3:
                    self.vel *= -0.7
                    self.bounce += 1
                else:
                    self.pos.y = self.landing_spot - Game.TILESIZE
                
            
            win.blit(self.sprite, (self.pos.x, self.pos.y))


load_items()