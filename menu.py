# menu related rendering

from classes.font import Font

MENU_SATE = "main"
font = Font("./src/chars/charmap.png")
font.load()

def update_main_menu(win):
    win.fill((0, 0, 0))
    font.render(win, (0, 0), "ABC")