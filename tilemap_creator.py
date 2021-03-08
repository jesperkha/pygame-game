# tilemap

import pygame
from utility.controller import Controller, update_controllers

pygame.init()

scale = 2
tilesize = 16
tile_width = 32
tile_height = 20

width = 512
height = 320

window = pygame.display.set_mode((width * scale, height * scale), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Cursor
class cursor:
    pos = [0, 0]
    img = pygame.transform.scale(pygame.image.load("./src/cursor.png"), (tilesize * scale, tilesize * scale))
    controller = Controller()
    pause = 0
    tile = 1

    @staticmethod
    def left():
        if cursor.pos[0] != 0:
            cursor.pos[0] -= tilesize * scale
            clock.tick(cursor.pause)

    @staticmethod
    def right():
        if cursor.pos[0] != (width - tilesize) * scale:
            cursor.pos[0] += tilesize * scale
            clock.tick(cursor.pause)

    @staticmethod
    def up():
        if cursor.pos[1] != 0:
            cursor.pos[1] -= tilesize * scale
            clock.tick(cursor.pause)

    @staticmethod
    def down():
        if cursor.pos[1] != (height - tilesize) * scale:
            cursor.pos[1] += tilesize * scale
            clock.tick(cursor.pause)

    @staticmethod
    def add_tile():
        pos = screen_to_grid()
        grid[pos[0]][pos[1]] = cursor.tile

    @staticmethod
    def remove_tile():
        pos = screen_to_grid()
        grid[pos[0]][pos[1]] = 0


cursor.controller.listen(pygame.K_LEFT, "keypressed", cursor.left)
cursor.controller.listen(pygame.K_RIGHT, "keypressed", cursor.right)
cursor.controller.listen(pygame.K_UP, "keypressed", cursor.up)
cursor.controller.listen(pygame.K_DOWN, "keypressed", cursor.down)
cursor.controller.listen(pygame.K_SPACE, "keypressed", cursor.add_tile)
cursor.controller.listen(pygame.K_d, "keypressed", cursor.remove_tile)


# Grid math
grid = []
for w in range(tile_width):
    arr = []
    for h in range(tile_height):
        arr.append(0)
    
    grid.append(arr)


# From screen pos to grid pos
def screen_to_grid() -> tuple:
    x = int(cursor.pos[0] / scale / tilesize)
    y = int(cursor.pos[1] / scale / tilesize)
    return (x, y)


# From grid to screen
def grid_to_screen(x: int, y: int) -> tuple:
    scrn_x = x * scale * tilesize
    scrn_y = y * scale * tilesize
    return (scrn_x, scrn_y)


def save_tilemap_as_file():
    f = open("tilemap.json", "a")
    f.append("[")
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            f.write(f"{}")            


run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    
    clock.tick(30)
    update_controllers()
    pygame.display.update()
    window.fill((0, 0, 0))

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 1:
                pos = grid_to_screen(x, y)
                pygame.draw.rect(window, (255, 0, 0), (pos[0], pos[1], tilesize * scale, tilesize * scale))


    window.blit(cursor.img, cursor.pos)


pygame.quit()