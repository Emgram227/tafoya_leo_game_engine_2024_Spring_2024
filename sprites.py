# this file was created by: Leo Tafoya
# this code was inspired by Zelda and informed by Chris Bradfield
from typing import Any
import pygame as pg
from settings import *
from utils import *
from os import path
import math

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

class Player(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites
        # initialize super class
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'theBell.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.doorkey = doorKey
        self.powerup = powerUp
        self.hiding = hiding
        self.moneybag = 100
        self.speed = 300
        self.hitpoints = 100
        self.cooldown = Timer(self)
        self.current_frame = 0
        self.last_update = 0
        self.test = True
        self.weapon = False
        self.holding_object = False
        self.max_hitpoints = 100
        self.get_mouse()
        self.shop_open = False
        self.paused = False
        self.npctalk = False
    
    def get_mouse(self):
        if pg.mouse.get_pressed()[0]:
            print("Left Click")
        if pg.mouse.get_pressed()[1]:
            print("Middle Click")
        if pg.mouse.get_pressed()[2]:
            print("Right Click")


    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.shop_open = False
            global hiding
            hiding = False 
            if self.npctalk == True:
                global npctalk
                npctalk = True
            else:
                npctalk = False

        if keys[pg.K_p]:
            hiding = True
        if keys[pg.K_e]:
            hiding = True
        if self.paused == False: 
            hiding = False
            if self.shop_open == False:
                if keys[pg.K_LEFT] or keys[pg.K_a]:
                    self.vx = -self.speed
                if keys[pg.K_RIGHT] or keys[pg.K_d]:
                    self.vx = self.speed
                if keys[pg.K_UP] or keys[pg.K_w]:
                    self.vy = -self.speed
                if keys[pg.K_DOWN] or keys[pg.K_s]:
                    self.vy = self.speed
                if self.vx != 0 and self.vy != 0:
                    self.vx *= 0.7071
                    self.vy *= 0.7071
    
    # def move(self,dx=0,dy=0):
    #     self.x += dx
    #     self.y += dy
        
    

    def collide_with_walls(self, dir):
        if dir == 'x':
           hits = pg.sprite.spritecollide(self, self.game.walls, False)
           if hits:
               if self.vx > 0:
                   self.x = hits[0].rect.left - self.rect.width
               if self.vx < 0:
                   self.x = hits[0].rect.right
               self.vx = 0
               self.rect.x = self.x
        if dir == 'y':
           hits = pg.sprite.spritecollide(self, self.game.walls, False)
           if hits:
               if self.vy > 0:
                   self.y = hits[0].rect.top - self.rect.height
               if self.vy < 0:
                   self.y= hits[0].rect.bottom
               self.vy = 0
               self.rect.y= self.y
    
    # made possible by Aayush's question!
    def collide_with_group(self,group,kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                #  self.image.fill(WHITE)
                 self.speed *= 2
                 self.hitpoints = 100
                 print("PowerUp")
                 print(hits[0].__class__.__name__)
                 self.powerup = True
            if str(hits[0].__class__.__name__) == "Key":    
                self.doorkey = True
                print(self.doorkey)
            if str(hits[0].__class__.__name__) == "Bush":
                global hiding
                hiding = True
                print(hiding)
            else:
                hiding = False
            
            if str(hits[0].__class__.__name__) == "Chest":   
                if self.doorkey == True:
                    self.doorkey = False
                    self.moneybag += 10
                    self.game.ammo += 10
                    if self.hitpoints > 100:
                        pass
                    else:
                        self.hitpoints += 5
                    kill
            if str(hits[0].__class__.__name__) == "Mob2":
                    print ("hit")
                    self.hitpoints -= 1
                    if self.powerup == True:
                        self.hitpoints += 1
                        self.moneybag += 1
                        kill
            if str(hits[0].__class__.__name__) == "Mob":
                    print ("hit")
                    self.hitpoints -= 1
                    if self.powerup == True:
                        self.hitpoints += 1
                        self.moneybag += 1
                        kill
            if str(hits[0].__class__.__name__) == "Ghost":
                    print ("hit")
                    self.hitpoints -= 1
                    if self.powerup == True:
                        self.hitpoints += 1
                        self.moneybag += 1
                        kill
            if str(hits[0].__class__.__name__) == "Shop":
                self.shop_open = True
                hiding = True
                self.paused = True
            
            if str(hits[0].__class__.__name__) == "Npc":
                self.npctalk =  True
            

                        

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            
    # def draw_health(self):
    #     if self.hitpoints > 100:
    #         color = GREEN
    #     else: 
    #         if self.hitpoints > 50:
    #             color = GREEN
    #         else:
    #             if self.hitpoints > 20:
    #                 color = YELLOW
    #             else:
    #                 if self.hitpoints > 0:
    #                     color = RED
    #     width = int(self.rect.width * self.hitpoints / self.max_hitpoints)
    #     self.health_bar = pg.Rect(0, 0, width, 7)
    #     # if self.hitpoints < self.max_hitpoints:
    #     pg.draw.rect(self.image, color, self.health_bar)


    

    def update(self):
        # self.draw_health()
        self.animate()
        self.rect.x = self.x
        self.rect.y = self.y
         # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        

        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y 
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.walkthroughs, False)
        if self.cooldown.cd < 1:
                self.cooling = False
                if not self.cooling:
                    self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
            
        if self.collide_with_group(self.game.power_ups, True):
            powerUp = True
        if self.collide_with_group(self.game.keys, True):
            doorKey = True
        if self.doorkey == True:
            self.collide_with_group(self.game.chests, True)
            if self.collide_with_group(self.game.chests, True):
                self.moneybag += 20
        if self.powerup == True:
            self.collide_with_group(self.game.mobs, True)
    
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
            
        
    


#Wall Classes
class Wall(pg.sprite.Sprite):
    #Basic wall
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'wall.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]

class Stone(pg.sprite.Sprite):
    #Used for cliffs or caves
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'Stone.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        
class Water(pg.sprite.Sprite):
    #Used for bodies of water (collision is on to show that you can't swim)
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walkthroughs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'water.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]

class Wood(pg.sprite.Sprite):
    #Used for bodies of water (collision is on to show that you can't swim)
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'wood.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]


class Coin(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'coin.png'))
        self.load_images()
        self.last_update = 0
        self.current_frame = 4
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 5) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
    def update(self):
        self.animate()


class PowerUp(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Bush(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walkthroughs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'bush.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]

class Chest(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.chests
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'chest.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]


class Key(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.keys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
vec = pg.math.Vector2
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'zombie.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.health = 10
        self.max_health = 10
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
        self.hiding = hiding

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
    def collide_with_walls(self, dir):
        if dir == 'x':
           hits = pg.sprite.spritecollide(self, self.game.walls, False)
           if hits:
               if self.vx > 0:
                   self.x = hits[0].rect.left - self.rect.width
               if self.vx < 0:
                   self.x = hits[0].rect.right
               self.vx = 0
               self.rect.x = self.x
        if dir == 'y':
           hits = pg.sprite.spritecollide(self, self.game.walls, False)
           if hits:
               if self.vy > 0:
                   self.y = hits[0].rect.top - self.rect.height
               if self.vy < 0:
                   self.y= hits[0].rect.bottom
               self.vy = 0
               self.rect.y= self.y
            
   
    def update(self):
            # self.rect.x += 1
            if self.health < 1:
                self.kill()
            if hiding == False:
                self.x += self.vx * self.game.dt
                self.y += self.vy * self.game.dt
                
                if self.rect.x < self.game.player1.rect.x:
            
                        self.vx = 100
                if self.rect.x > self.game.player1.rect.x:
                
                        self.vx = -100
                if self.rect.y < self.game.player1.rect.y:
                
                        self.vy = 100
                if self.rect.y > self.game.player1.rect.y:
                    
                        self.vy = -100
                self.rect.x = self.x
                self.collide_with_walls('x')
                self.rect.y = self.y
                self.collide_with_walls('y')


class MobSpawner(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.mobspawner
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'mob_spawner.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]

class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'skull.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.health = 10
        self.max_health = 10
        self.chase_distance = 500
        self.speed = 300
        self.hiding = hiding 
    # def sensor(self):
    #     if self.hiding == True:
    #         self.chasing = False
    #     else:
    #          self.chasing = True

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]

    
    def update(self):
        # self.sensor()
        if self.health < 1:
            self.kill()
        if hiding == False:
            self.rot = (self.game.player1.rect.center - self.pos).angle_to(vec(1, 0))
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # equation of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # hit_rect used to account for adjusting the square collision when image rotates
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

    
class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'ghost.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        # added
        self.speed = 300
        self.chasing = True
        self.health = 10
        self.max_health = 10
      
        #self.hitpoints = 100
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
    def sensor(self):
        if abs(self.rect.x - self.game.player1.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player1.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    

    def update(self):
        #if self.hitpoints <= 0:
            #self.kill()
        # self.sensor()
        if hiding == False:
            if self.chasing:
                self.rot = (self.game.player1.rect.center - self.pos).angle_to(vec(1, 0))
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.acc = vec(self.speed, 0).rotate(-self.rot)
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                # equation of motion
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                # hit_rect used to account for adjusting the square collision when image rotates
                # self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.game.walls, 'x')
                # self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.game.walls, 'y')
                # self.rect.center = self.hit_rect.center

class HealthBar(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, target, pct):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.w = w
        self.h = h
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x
        self.rect.y = y
        self.target = target
        self.pct = pct
    def update(self):
        self.rect.x = self.target.rect.x
        self.rect.y = self.target.rect.y

#ChatGPT
# class GameObject(pg.sprite.Sprite):
#     def __init__(self, player1, game):
#         super().__init__()
#         self.groups = game.all_sprites
#         self.image = pg.Surface((5, 50))
#         self.image.fill(BLACK)
#         self.rect = self.image.get_rect()
#         self.player1 = player1
#         self.offset = (50, 0)  # Offset from the player
#         self.following = True  # Flag to indicate if the object is following the player

#     def update(self):
#         if self.following:
#             # Set object's position relative to the player
#             self.rect.center = (self.player1.rect.centerx + self.offset[0], self.player1.rect.centery + self.offset[1])


class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bosses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((40,50))
        self.spritesheet = Spritesheet(path.join(img_folder, 'boss2.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0,0,48,66).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.chase_distance = 500
        self.speed = 300
        self.hitpoints = 100

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 48, 66), 
                                self.spritesheet.get_image(32,0, 48, 66)]

    
    def update(self):
        if self.hitpoints <= 0:
            self.kill()
        if hiding == False:
            self.rot = (self.game.player1.rect.center - self.pos).angle_to(vec(1, 0))
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # equation of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # hit_rect used to account for adjusting the square collision when image rotates
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
    def collide_with_group(self,group,kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Bullet":
                self.hitpoints -= 1


#Modified from ChatGPT
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, start_x, start_y, target_x, target_y):
        super().__init__()
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.speed = 10
        distance = math.sqrt((target_x - start_x) ** 2 + (target_y - start_y) ** 2)
        self.dx = self.speed * (target_x - start_x) / distance
        self.dy = self.speed * (target_y - start_y) / distance


    def update(self):
        self.collide_with_group(self.game.mobs, True)
        self.collide_with_group(self.game.bosses, True)
        # self.collide_with_walls('x')
        # self.collide_with_walls('y')
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Remove bullet if it goes out of screen
        # if not pg.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
        #     self.kill()

    def collide_with_group(self,group,kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob2":
                    print ("shot")
                    kill
                    self.kill()

            if str(hits[0].__class__.__name__) == "Mob":
                    print ("shot")
                    kill
                    self.kill()

            if str(hits[0].__class__.__name__) == "Ghost":
                    print ("shot")
                    kill
                    self.kill()
            if str(hits[0].__class__.__name__) == "Boss":
                    print ("shot")
                    self.kill()

    # def collide_with_walls(self, dir):
    #     if dir == 'x':
    #        hits = pg.sprite.spritecollide(self, self.game.walls, False)
    #        if hits:
    #            if self.dx > 0:
    #                self.x = hits[0].rect.left - self.rect.width
    #            if self.dx < 0:
    #                self.x = hits[0].rect.right
    #            self.vx = 0
    #            self.rect.x = self.x
    #     if dir == 'y':
    #        hits = pg.sprite.spritecollide(self, self.game.walls, False)
    #        if hits:
    #            if self.dy > 0:
    #                self.y = hits[0].rect.top - self.rect.height
    #            if self.dy < 0:
    #                self.y= hits[0].rect.bottom
    #            self.vy = 0
    #            self.rect.y= self.y
    
class Shop(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walkthroughs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'shop.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 96, 64), 
                                self.spritesheet.get_image(64,0, 96, 64)]

class Npc(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walkthroughs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'bush.png'))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
