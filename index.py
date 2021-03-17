
# Set path for imports
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

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

pygame.display.set_caption("17.03.21")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("./src/items/item1.png").convert_alpha(), (100, 100)))

# resize window
def resize(w, h):
    if not fullscreen:
        pygame.display.set_mode((w, h), pygame.RESIZABLE)
    else:
        pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)


# Load all assets at once
loading_queue = [] # append loading functions to queue
def load_game():
    for asset in loading_queue:
        asset()
    

# ---------------- TEST ZONE ---------------- #

from classes.player import Player, update_players
from classes.bullet import update_bullets
from classes.guns import Pistol
from utility.files import load_json
from classes.tilemap import Tilemap
from classes.item import update_items, create_item, Item, load_items
from classes.timer import GameTimer
from classes.animation import EffectAnimation, update_effects
from random import randrange
from menu import update_main_menu

LEVEL = 2

loading_queue.append(load_items)

level_json = load_json(f"./levels/level{LEVEL}.json")
Game.WALL_LOOP = level_json["screen_loop"]

background = pygame.image.load(level_json["background"])

gun = Pistol()
loading_queue.append(gun.load)

player = Player((20, 0), (16, 16), [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], gun)
player.collision_map = Tilemap(level_json["collision_map"])

Game.TILEMAP = Tilemap(level_json["tilemap"])
Item.collision_map = load_json(level_json["collision_map"])

c = Controller()
c.listen(pygame.K_k, "keypressed", create_item)

t = GameTimer()

cm = load_json(level_json["collision_map"])

def pause():
    if not Game.STATE == Game.PAUSE:
        Game.STATE = Game.PAUSE
    else:
        Game.STATE = Game.INGAME

c.listen(pygame.K_p, "keypressed", pause)

# ------------------------------------------- #

# Loads game assets before game loop starts
load_game()

# Gameloop
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


    # Game states ---------------------------------------------------------- #

    update_controllers()

    if Game.STATE == Game.INGAME:
        buffer.fill((0, 0, 0))
        buffer.blit(background, (0, 0))
        if Game.TILEMAP:
            Game.TILEMAP.update(buffer)
        update_bullets(buffer, cm)
        update_players(buffer)
        update_items(buffer)
        update_effects(buffer)
        t.update(buffer)

    elif Game.STATE == Game.MENU:
        update_main_menu(buffer)

    elif Game.STATE == Game.PAUSE:
        pass
        
    # Window rendering and buffer sizing
    window.fill((0, 0, 0))
    buffer_width = int(window.get_height() * Game.ASPECT_RATIO)
    buffer_height = window.get_height()
    if buffer_width > monitor_size[0]:
        buffer_width = monitor_size[0]
        buffer_height = int(monitor_size[0] / Game.ASPECT_RATIO)

    buffer_scale = [buffer_width, buffer_height]
    buffer_pos = [int((window.get_width() - buffer_width) / 2), int((window.get_height() - buffer_height) / 2)]
    window.blit(pygame.transform.smoothscale(buffer, buffer_scale), buffer_pos)
    pygame.display.update()


pygame.quit()