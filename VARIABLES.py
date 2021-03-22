class Game:

    # Misc
    FPS = 60
    ASPECT_RATIO = 560 / 320
    TILESIZE = 16

    # Gamestates
    MENU = 0
    INGAME = 1
    PAUSE = 2
    LOADING = 3

    STATE = MENU

    # Game
    HEIGHT = 320
    WIDTH = int(HEIGHT * ASPECT_RATIO)
    WALL_LOOP = True
    TILEMAP = None
    MOUSE = [0, 0]
    MOUSE_CLICKED = False
    MOUSE_RELEASED = True
    TIMER = None

    # Player 
    JUMP_HEIGHT = 7
    WALK_SPEED = 1
    GRAVITY = 0.4
    FRICTION = 0.7

    # Guns
    BULLET_SPEED = 5
    RELOAD_TIME = 4
    BULLET_CAP = 20
    GUN_RECOIL = 5
    MAG_SIZE = 10