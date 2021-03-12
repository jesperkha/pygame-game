# Tilemap editor

# F to open file
# S to save as file or overwrite
# A and D to switch between sprites / types
# Mouse buttons to draw and remove
# SPACE to clear all

# Add sprites to this list to be able to draw them

# Indexes:
# ALL - 0
# JUMP THROUGH - 1
# TOP ONLY - 2
# BOTTOM ONLY - 3
# LEFT ONLY - 4
# RIGHT ONLY - 5
# Indexes more than 5 are decoration

MY_BLOCKS = [
    "./src/tiles/right.png",
    "./src/tiles/bottom.png",
    "./src/tiles/left.png",
    "./src/tiles/top.png",
    "./src/tiles/corner-top-right.png",
    "./src/tiles/corner-top-left.png",
    "./src/tiles/corner-bottom-right.png",
    "./src/tiles/corner-bottom-left.png",
    "./src/tiles/inside-corner-bottom-left.png",
    "./src/tiles/inside-corner-bottom-right.png",
    "./src/tiles/inside-corner-top-left.png",
    "./src/tiles/inside-corner-top-right.png",
    "./src/tiles/fill.png",
    "./src/tiles/platform-middle.png",
    "./src/tiles/platform-right.png",
    "./src/tiles/platform-left.png",
    "./src/tiles/deco-1.png",
    "./src/tiles/deco-2.png",
    "./src/tiles/deco-3.png",
    "./src/tiles/deco-4.png",
    "./src/tiles/deco-5.png",
]

BLOCKS_SRC = [f"./src/collisionmap/{x}.png" for x in range(6)] + MY_BLOCKS

# Files are save as json in this format:
# [
#   [type, src, x, y]
# ]

# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------

import pygame
from utility.controller import Controller, update_controllers
from math import floor
from utility.files import load_json

pygame.init()

scale = 2
tilesize = 16
width = 560
height = 320
tile_width = int(width / tilesize)
tile_height = int(height / tilesize)

window = pygame.display.set_mode((width * scale, height * scale), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Blocks
BLOCKS = [pygame.transform.scale(pygame.image.load(x).convert_alpha(), (tilesize*scale, tilesize*scale)) for x in BLOCKS_SRC]

# Cursor
class cursor:
    pos = [0, 0]
    controller = Controller()
    tile = 1

    @staticmethod
    def add_tile():
        pos = screen_to_grid(cursor.pos)
        grid[pos[0]][pos[1]] = cursor.tile

    @staticmethod
    def remove_tile():
        pos = screen_to_grid(cursor.pos)
        grid[pos[0]][pos[1]] = 0
    
    @staticmethod
    def increment_tile():
        if cursor.tile < len(BLOCKS_SRC):
            cursor.tile += 1
    
    @staticmethod
    def decrement_tile():
        if cursor.tile > 1:
            cursor.tile -= 1

    @staticmethod
    def clear():
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = 0


cursor.controller.listen(pygame.K_d, "keypressed", cursor.increment_tile)
cursor.controller.listen(pygame.K_a, "keypressed", cursor.decrement_tile)
cursor.controller.listen(pygame.K_SPACE, "keypressed", cursor.clear)


# Grid math
grid = []
for w in range(tile_width):
    arr = []
    for h in range(tile_height):
        arr.append(0)
    
    grid.append(arr)


# From screen pos to grid pos
def screen_to_grid(pos) -> tuple:
    x = int(pos[0] / scale / tilesize)
    y = int(pos[1] / scale / tilesize)
    return [x, y]


def non_scale_screen_to_grid(pos):
    x = int(pos[0] / tilesize)
    y = int(pos[1] / tilesize)
    return [x, y]


# From grid to screen
def grid_to_screen(x: int, y: int) -> tuple:
    scrn_x = x * scale * tilesize
    scrn_y = y * scale * tilesize
    return [scrn_x, scrn_y]


def mouse_to_screen():
    m = pygame.mouse.get_pos()
    x = floor(m[0] / scale / tilesize)
    y = floor(m[1] / scale / tilesize)
    return [x * tilesize * scale, y * tilesize * scale]


def save_to_file():
    filename = input("Save as: ")
    if filename == "":
        return

    f = open(f"{filename}.json", "w+")
    f.write("[")

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] > 0:
                src = BLOCKS_SRC[grid[x][y] - 1]
                type = grid[x][y] - 1
                x_ = grid_to_screen(x, y)[0] / scale
                y_ = grid_to_screen(x, y)[1] / scale
                f.write(f'[{type}, "{src}", {x_}, {y_}],')

    f.write("]")
    f.close()
    global run
    run = False
    print("\nRemember to save the file!\n")


# Start of program
def open_json_file():
    f = input("Open file: ")
    if f != "":
        json = load_json(f"{f}.json")
        for n in json:
            x = int(n[2] / tilesize)
            y = int(n[3] / tilesize)
            grid[x][y] = BLOCKS_SRC.index(n[1]) + 1


cursor.controller.listen(pygame.K_s, "keypressed", save_to_file)
cursor.controller.listen(pygame.K_f, "keypressed", open_json_file)

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    
    if pygame.mouse.get_pressed()[0]:
        cursor.add_tile()
    elif pygame.mouse.get_pressed()[2]:
        cursor.remove_tile()

    clock.tick(60)
    update_controllers()
    pygame.display.update()
    window.fill((0, 0, 0))

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            pos = grid_to_screen(x, y)
            type = grid[x][y]

            if type > 0:
                window.blit(BLOCKS[type - 1], pos)

    
    cursor.pos = mouse_to_screen()
    sprite = BLOCKS[cursor.tile - 1].copy()
    sprite.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    window.blit(sprite, cursor.pos)


pygame.quit()