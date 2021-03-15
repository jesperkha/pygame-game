import pygame
from utility.controller import update_controllers, Controller
from VARIABLES import Game

pygame.init()
clock = pygame.time.Clock()

# Window and window buffer
START_SCALE = 1.3
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
window = pygame.display.set_mode((int(800 * START_SCALE), int(450 * START_SCALE)), pygame.RESIZABLE)
buffer = pygame.Surface((Game.WIDTH, Game.HEIGHT))
buffer_scale = [int(window.get_height() * Game.ASPECT_RATIO), window.get_height()]
buffer_pos = [(window.get_width() - buffer.get_width()) / 2, 0]
fullscreen = False

# ---------------- TEST ZONE ----------------

from player import Player, update_players
from bullet import update_bullets
from guns import Gun
from utility.files import load_json
from tilemap import Tilemap
from item import update_items, create_item, Item
from timer import GameTimer

LEVEL = 2

gun = Gun(load_json("./main.json")["items"]["pistol"])
gun.animation_player.init()

level_json = load_json(f"./levels/level{LEVEL}.json")
Game.WALL_LOOP = level_json["screen_loop"]

background = pygame.image.load(level_json["background"])

player = Player((20, 0), (16, 16), [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], gun)
player.collision_map = Tilemap(level_json["collision_map"])

Game.TILEMAP = Tilemap(level_json["tilemap"])
Item.collision_map = load_json(level_json["collision_map"])

c = Controller()
c.listen(pygame.K_k, "keypressed", create_item)

t = GameTimer()

# -------------------------------------------

def resize(w, h):
    if not fullscreen:
        pygame.display.set_mode((w, h), pygame.RESIZABLE)
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
            resize(int(800 * START_SCALE), int(450 * START_SCALE))

        if event.type == pygame.VIDEORESIZE:
            resize(event.w, event.h)

    pygame.display.update()
    buffer.fill((0, 0, 0))

    update_controllers()
    
    if Game.STATE == Game.INGAME:
        buffer.blit(background, (0, 0))
        if Game.TILEMAP:
            Game.TILEMAP.update(buffer)
        update_bullets(buffer)
        update_players(buffer)
        update_items(buffer)
        t.update(buffer)

        
    # Window rendering and buffer sizing
    window.fill((0, 0, 0))
    buffer_width = int(window.get_height() * Game.ASPECT_RATIO)
    buffer_height = window.get_height()
    if buffer_width > monitor_size[0]:
        buffer_width = monitor_size[0]
        buffer_height = int(monitor_size[0] / Game.ASPECT_RATIO)

    buffer_scale = [buffer_width, buffer_height]
    buffer_pos = [int((window.get_width() - buffer_width) / 2), int((window.get_height() - buffer_height) / 2)]
    window.blit(pygame.transform.scale(buffer, buffer_scale), buffer_pos)


pygame.quit()