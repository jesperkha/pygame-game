# Player class

from utility.methods import set_timeout
from pygame import draw
from functools import partial

from utility.vector import Vector
from utility.controller import Controller
from utility.collision import check_collision_rect_points
from utility.files import load_json
from utility.animation import AnimationPlayer

from VARIABLES import Game
from .bullet import Bullet
from .item import Item


def update_players(win):
    for p in Player.players:
        p.update(win)


class Player:
    players = []

    def __init__(self, pos: tuple, size: tuple, keys: list, gun: object) -> None:
        self.pos = Vector(pos[0], pos[1])
        self.vel = Vector(0, 0)
        self.grv = Game.GRAVITY
        self.frc = Game.FRICTION
        self.speed = Game.WALK_SPEED
        self.jump_height = Game.JUMP_HEIGHT
        self.jumping = False
        self.terminal_velocity = Game.JUMP_HEIGHT

        self.direction = -1 # -1: Left, 1: Right

        self.size = Vector(size[0], size[1])
        self.hurtbox_radius = self.size.y/1.5
        self.grab_range = Game.TILESIZE

        # if img:
        #     self.image = image.load(img).convert_alpha()
        #     self.image = transform.scale(self.image, (self.size.x, self.size.y))
        # else:
        self.image = None
        self.collision_map = None

        # Key controls
        self.controller = Controller()
        self.controller.listen(keys[0], "keypressed", self.jump)
        self.controller.listen(keys[1], "keypressed", self.shoot)
        self.controller.listen(keys[2], "keydown", partial(self.move, -1))
        self.controller.listen(keys[3], "keydown", partial(self.move, 1))

        # Guns
        self.gun = gun
        self.mag_size = self.gun.mag_size
        self.ammo = self.mag_size
        self.reload_animation = AnimationPlayer(load_json("./json/reload_animation.json"))
        self.reload_animation.load() # ----- REMOVE ----- #

        # Flags
        self.SHOW_HURTBOX = False
        self.INVINCIBLE = False
        self.RELOADING = False

        Player.players.append(self)


    # Called from update_players() 
    def update(self, win):
        # Falling checks self.jumping flag to prevent double jump
        if self.vel.y > 0:
            self.jumping = True

        # Velocity is added to position (gravity and friction too)
        self.vel.x *= self.frc
        self.vel.y += self.grv

        # Set fall speed if its too high
        if self.vel.y > self.terminal_velocity:
            self.vel.y = self.terminal_velocity

        self.pos.add(self.vel)

        # ------------------------------------------------------

        # Bullet collision
        hit = False
        dir = 0
        if not self.INVINCIBLE:
            for b in Bullet.bullets:
                if Vector.dist(self.pos, b.pos) < self.hurtbox_radius and b.state:
                    hit = True
                    dir = b.dir
                    b.explode()
            
            if hit:
                self.got_hit(dir)


        # Ground and wall collision
        if self.pos.y + self.size.y >= Game.HEIGHT:
            self.pos.y = Game.HEIGHT - self.size.y
            self.jumping = False
            self.vel.y = 0

        if not Game.WALL_LOOP:
            if self.pos.x < 0:
                self.pos.x = 0
            elif self.pos.x + self.size.x > Game.WIDTH:
                self.pos.x = Game.WIDTH - self.size.x

        else:
            if self.pos.x < 0:
                self.pos.x = Game.WIDTH - self.size.x
            elif self.pos.x + self.size.x > Game.WIDTH:
                self.pos.x = 0
        
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -0.5


        # Platform collision
        # for p in Platform.platforms:
        #     if check_collision_rect(self, p):
        #         side = self.find_collision(p)
        #         self.handle_collision(side, p)
            
        
        # Tilemap collision
        if self.collision_map:
            self.do_tile_collision(self.collision_map)

        
        # Check for item collision
        self.check_for_items()

        # Check fot reload
        if not self.RELOADING and self.ammo == 0:
            self.reload_gun()

        # ------------------------------------------------------

        if self.RELOADING:
            win.blit(self.reload_animation.animate(self.direction, False, True), (self.pos.x, self.pos.y - Game.TILESIZE))
            

        # Render gun
        if self.gun:
            self.gun.update(self.size, self.pos, self.direction, win)

        if self.image:
            win.blit(self.image, (self.pos.x, self.pos.y))
        else:
            draw.rect(win, (235, 26, 109), (self.pos.x, self.pos.y, self.size.x, self.size.y))

        if self.SHOW_HURTBOX:
            draw.circle(win, (0, 0, 250), (self.pos.x + self.size.x/2, self.pos.y + self.size.y/2), self.hurtbox_radius)

    
    # Find collision side on THIS player
    # Called from update()
    def find_collision(self, p: object) -> str:
        collision_threshold = self.terminal_velocity

        # Relative to THIS
        if abs(p.pos.y - (self.pos.y + self.size.y)) <= collision_threshold and self.vel.y >= 0:
            return "bottom"
        elif abs((p.pos.x + p.size.x) - self.pos.x) <= collision_threshold and self.vel.x < 0:
            return "left"
        elif abs(p.pos.x - (self.pos.x + self.size.x)) <= collision_threshold and self.vel.x > 0:
            return "right"
        elif abs((p.pos.y + p.size.y) - self.pos.y) <= collision_threshold and self.vel.y < 0:
            return "top"


    # Called after finding collision
    # Resolves based on where collision is located (platforms only)
    # Called from update()
    def handle_collision(self, side: str, p: object) -> None:
        if side == "bottom":
            self.vel.y = 0
            self.pos.y = p.pos.y - self.size.y
            self.jumping = False
        if side == "top" and not p.jump_through:
            self.pos.y = p.pos.y + p.size.y
            self.vel.y *= -0.5
        if side == "right":
            self.vel.x = 0
            self.pos.x = p.pos.x - self.size.x
        if side == "left":
            self.vel.x = 0
            self.pos.x = p.pos.x + p.size.x


    # Jump when ARROW_UP is pressed
    # Called from self.controller class
    def jump(self):
        if not self.jumping:
            self.vel.y -= self.jump_height
            self.jumping = True

    
    # Moves player when either left or right arrow is pressed
    # Called from self.controller class
    def move(self, dir: int):
        self.vel.x += self.speed * dir
        self.direction = dir

    
    # Applies force to player
    def apply_force(self, x: int, y: int):
        self.vel.x += x
        self.vel.y += y


    # Shoots when DOWN_ARROW is pressed
    # Called from self.controller class
    def shoot(self):
        if self.gun and self.ammo != 0:
            Bullet.new(self.pos, self.size, self.direction, self.gun.offset)
            self.gun.shoot()
            self.apply_force(self.gun.recoil * self.direction * -1, 0)
            self.ammo -= 1
        elif self.ammo == 0 and not self.RELOADING:
            self.reload_gun()

    
    # Called when player is shot
    # Called from update()
    def got_hit(self, dir):
        self.apply_force(20 * dir, 0)
        # self.health -= 10


    # Called when player tries to shoot with no ammo left
    # Called from shoot()
    def reload_gun(self):
        self.RELOADING = True
        set_timeout(self.finish_reload, Game.RELOAD_TIME)


    # Stops reloading process
    # Called from reload_gun()
    def finish_reload(self):
        self.ammo = self.mag_size
        self.RELOADING = False
        self.reload_animation.reset()

    
    # Do collision for tile
    # Called from do_tile_collision()
    def tile_collision_side(self, x: int, y: int, tilesize: int, type: int) -> None:
        collision_threshold = self.terminal_velocity

        # Top of tile
        if abs(y - (self.pos.y + self.size.y)) <= collision_threshold and self.vel.y >= 0:
            if type == 2 or type == 0 or type == 1:
                self.vel.y = 0
                self.pos.y = y - self.size.y
                self.jumping = False

        # Right of tile
        elif abs((x + tilesize) - self.pos.x) <= collision_threshold and self.vel.x <= 0:
            if type == 5 or type == 0 or type == 1:
                self.vel.x = 0
                self.pos.x = x + tilesize

        # Left of tile
        elif abs(x - (self.pos.x + self.size.x)) <= collision_threshold and self.vel.x >= 0:
            if type == 4 or type == 0 or type == 1:
                self.vel.x = 0
                self.pos.x = x - self.size.x

        # Bottom of tile
        elif abs((y + tilesize) - self.pos.y) <= collision_threshold and self.vel.y < 0:
            if type == 3 or type == 0:
                self.pos.y = y + tilesize
                self.vel.y *= -0.5

    
    # Handles collision with a tilemap
    # Called from update()
    def do_tile_collision(self, tilemap):
        for tile in tilemap.tilemap:
            # ALL - 0
            # JUMP THROUGH - 1
            # TOP ONLY - 2
            # BOTTOM ONLY - 3
            # LEFT ONLY - 4
            # RIGHT ONLY - 5
            if check_collision_rect_points(self.pos.x, self.pos.y, self.size.x, self.size.y, tile[2], tile[3], tilemap.tilesize, tilemap.tilesize):
                if tile[0] < 6: # Indexes more than 5 are deco
                    self.tile_collision_side(tile[2], tile[3], tilemap.tilesize, tile[0])
    

    # Checks to see if player is in grab range of item
    # Called from update()
    def check_for_items(self):
        for i in Item.items:
            distance = Vector.dist(self.pos, i.pos)
            if distance < self.grab_range:
                self.pick_up_item(i)


    # Handles item pickup
    # Called from check_for_items()
    def pick_up_item(self, item):
        item.die()
