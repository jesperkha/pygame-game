# menu related rendering

from classes.font import Font
from pygame import mouse, draw
from utility.signals import Signal
from VARIABLES import Game

# TITLE, SETTINGS, GAME_SELECT, INGAME, CREDITS
MENU_STATE = "TITLE"
font = None

def load_menu():
    global font
    font = Font("./src/font_sheet.png")
    font.load()


def button(win, name: str, state: str, pos: tuple, scale: int = 1) -> None:
    size = font.render(win, pos, name, 2, scale)
    if Game.MOUSE[0] > size[0] and Game.MOUSE[1] > size[1] and Game.MOUSE[0] < size[0] + size[2] and Game.MOUSE[1] < size[1] + size[3]:
        # Click
        if Game.MOUSE_CLICKED:
            global MENU_STATE
            MENU_STATE = state

        # Hover
        else:
            draw.rect(win, (255, 255, 255), size)


def update_menu(win):
    win.fill((0, 0, 0))

    if MENU_STATE == "TITLE":
        font.render(win, (50, 75), "SHOOTOUT", 2, 3)
        button(win, "PLAY", "INGAME", (50, 130))
        button(win, "SETTINGS", "INGAME", (50, 150))
        button(win, "CREDITS", "INGAME", (50, 170))

    elif MENU_STATE == "INGAME":
        Game.STATE = Game.INGAME