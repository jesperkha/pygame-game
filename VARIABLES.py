class Game:

    # Misc
    FPS = 60
    ASPECT_RATIO = 560 / 320

    # Gamestates
    MENU = 0
    INGAME = 1
    PAUSE = 2

    # Game
    HEIGHT = 320
    WIDTH = int(HEIGHT * ASPECT_RATIO)
    STATE = INGAME
    WALL_LOOP = True

    # Player
    JUMP_HEIGHT = 7
    WALK_SPEED = 1
    GRAVITY = 0.4
    FRICTION = 0.7

    # Guns
    BULLET_SPEED = 5
    BULLET_CAP = 20
    GUN_RECOIL = 5
    RELOAD_TIME = 2
    MAG_SIZE = 999