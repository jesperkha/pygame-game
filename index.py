import pygame
from utility.controller import update_controllers
from VARIABLES import Game

pygame.init()
clock = pygame.time.Clock()

# Window and window buffer
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
window = pygame.display.set_mode((800, 450), pygame.NOFRAME)
buffer = pygame.Surface((Game.WIDTH, Game.HEIGHT))
buffer_scale = [int(window.get_height() * Game.ASPECT_RATIO), window.get_height()]
buffer_pos = [(window.get_width() - buffer.get_width()) / 2, 0]
fullscreen = False

# ---------------- TEST ZONE ----------------

from player import Player, update_players
from platform import update_platforms, Platform
from bullet import update_bullets
from guns import Gun
from utility.files import load_json
from tilemap import Tilemap

# plat = Platform((100, Game.HEIGHT - 30), (50, 10))
# plat2 = Platform((200, Game.HEIGHT - 30), (50, 10), True)

g = load_json("./main.json")["items"]["pistol"]
gun = Gun(g["size"], g["offset"], g["sprite_path"], g["animation_path"], g["frames"], g["recoil"])
gun.animation_player.init()

player = Player((20, 0), (16, 16), [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], gun)

# tm = Tilemap("./_.json")
tm = Tilemap("./col.json")

# -------------------------------------------

def resize(w, h):
    if not fullscreen:
        pygame.display.set_mode((w, h), pygame.NOFRAME)
    else:
        pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)


# Gameloop (very cool)
run = True
while run:
    # Key controls for window and resizing
    clock.tick(Game.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            fullscreen = not fullscreen
            resize(800, 450)

        if event.type == pygame.VIDEORESIZE:
            resize(event.w, event.h)

    pygame.display.update()
    buffer.fill((0, 0, 0))

    # Update environment and entities
    update_controllers()

    tm.update(buffer)
    
    if Game.STATE == Game.INGAME:
        update_platforms(buffer)
        update_bullets(buffer)
        update_players(buffer)
        
        player.do_tile_collision(tm)

    # Window rendering and buffer sizing
    window.fill((100, 100, 100))
    buffer_width = int(window.get_height() * Game.ASPECT_RATIO)
    buffer_height = window.get_height()
    if buffer_width > monitor_size[0]:
        buffer_width = monitor_size[0]
        buffer_height = int(monitor_size[0] / Game.ASPECT_RATIO)

    buffer_scale = [buffer_width, buffer_height]
    buffer_pos = [(window.get_width() - buffer_width) / 2, (window.get_height() - buffer_height) / 2]
    window.blit(pygame.transform.scale(buffer, buffer_scale), buffer_pos)


pygame.quit()