# IMPORTS --------------------------------------------- #
import pygame

from VARIABLES import Game
from menu import update_menu, load_menu

import classes.tilemap as tilemap
import classes.bullet as bullet
import classes.player as player
import classes.timer as timer
import classes.item as item
import classes.guns as guns

import utility.controller as controller
import utility.animation as animation
import utility.files as files


# Set path for imports (root)
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Window and window buffer
pygame.init()
clock = pygame.time.Clock()
START_SCALE = 1
fullscreen = False
background = pygame.Surface((Game.WIDTH, Game.HEIGHT))
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
window = pygame.display.set_mode((int(800 * START_SCALE), int(450 * START_SCALE)), pygame.RESIZABLE)
buffer = pygame.Surface((Game.WIDTH, Game.HEIGHT))
buffer_scale = [int(window.get_height() * Game.ASPECT_RATIO), window.get_height()]
buffer_pos = [(window.get_width() - buffer.get_width()) / 2, 0]

pygame.display.set_caption("18.03.21")
pygame.display.set_icon(pygame.image.load("./src/items/item1.png").convert_alpha())


# resize window
def resize(w, h):
    if not fullscreen:
        pygame.display.set_mode((w, h), pygame.RESIZABLE)
    else:
        pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)


# load game assets all at once
def load_assets():
    load_menu()
    item.load_items()
    bullet.load_bullets()

    level_json = files.load_json("./levels/level2.json")
    Game.WALL_LOOP = level_json["screen_loop"]

    global background
    background = pygame.image.load(level_json["background"])

    bullet.Bullet.collision_map = files.load_json(level_json["collision_map"])
    item.Item.collision_map = files.load_json(level_json["collision_map"])

    Game.TILEMAP = tilemap.Tilemap(level_json["tilemap"])
    Game.TIMER = timer.GameTimer()

    gun = guns.Pistol()
    gun.load()
    p1 = player.Player((150, 0), (16, 16), [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], gun)
    p1.collision_map = tilemap.Tilemap(level_json["collision_map"])

    # gun2 = guns.Pistol()
    # gun2.load()
    # p2 = player.Player((Game.WIDTH - 166, 0), (16, 16), [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], gun2)
    # p2.collision_map = tilemap.Tilemap(level_json["collision_map"])


# GAME LOOP ----------------------------------------------------------------------------- #

# Loads assets first
load_assets()

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

    controller.update_controllers()


    # INGAME LOOP ---------------------------------------------------------------------- #
    if Game.STATE == Game.INGAME:
        buffer.blit(background, (0, 0))
        if Game.TILEMAP:
            Game.TILEMAP.update(buffer)
        if Game.TIMER:
            Game.TIMER.update(buffer)
        bullet.update_bullets(buffer)
        player.update_players(buffer)
        item.update_items(buffer)
        animation.update_effects(buffer)


    # MENU LOOP ------------------------------------------------------------------------ #
    if Game.STATE == Game.MENU:
        update_menu(buffer)


    # LOADING GAME --------------------------------------------------------------------- #
    if Game.STATE == Game.LOADING:
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
    window.blit(pygame.transform.scale(buffer, buffer_scale), buffer_pos)
    pygame.display.update()

    # Set mouse position relative to screen
    ratio_x = (window.get_width() / buffer.get_width())
    ratio_y = (window.get_height() / buffer.get_height())
    mouse_pos = pygame.mouse.get_pos()
    Game.MOUSE = [mouse_pos[0] / ratio_x, mouse_pos[1] / ratio_y]

    # Toggle mouse press
    btn = pygame.mouse.get_pressed(num_buttons=3)[0]
    if btn:
        if Game.MOUSE_RELEASED:
            Game.MOUSE_CLICKED = True
            Game.MOUSE_RELEASED = False
        else:
            Game.MOUSE_CLICKED = False
    else:
        Game.MOUSE_CLICKED = False
        Game.MOUSE_RELEASED = True



pygame.quit()