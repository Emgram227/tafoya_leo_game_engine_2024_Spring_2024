# this file was created by: Leo Tafoya
# this code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
from utils import *


class Player(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites
        # initialize super class
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.doorkey = doorKey
        self.powerup = powerUp
        self.hiding = hiding
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 100
        self.cooldown = Timer(self)

        self.test = True

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
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
                 self.image.fill(WHITE)
                 self.speed *= 2
                 self.hitpoints = 100
                 print("PowerUp")
                 print(hits[0].__class__.__name__)
                 self.powerup = True
            if str(hits[0].__class__.__name__) == "Key":    
                self.doorkey = True
                print(self.doorkey)
            if str(hits[0].__class__.__name__) == "Bush":
                self.hiding = True
                print(self.hiding)
            
            if str(hits[0].__class__.__name__) == "Chest":   
                if self.doorkey == True:
                    self.doorkey == False
                    self.moneybag += 10
                    kill
            if str(hits[0].__class__.__name__) == "Mob2":
                    print ("hit")
                    self.hitpoints -= 1
                    if self.powerup == True:
                        self.hitpoints += 1
                        self.moneybag += 1
                        kill
            
           


    def update(self):
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
        self.collide_with_group(self.game.bushes, False)
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
            
        
    



class Wall(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

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
        self.groups = game.all_sprites, game.bushes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Chest(pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.chests
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

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
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
        self.hiding = hiding

    def collide_with_walls(self, dir):
            if dir == 'x':
                # print('colliding on the x')
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    self.vx *= -1
                    self.rect.x = self.x
            if dir == 'y':
                # print('colliding on the y')
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    self.vy *= -1
                    self.rect.y = self.y
    def update(self):
            # self.rect.x += 1
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt
            
            if self.rect.x < self.game.player1.rect.x:
                if self.hiding == True:
                    self.vx = 0
                else:
                    self.vx = 100
            if self.rect.x > self.game.player1.rect.x:
                 if self.hiding == True:
                    self.vx = 0
                 else:
                    self.vx = -100
            if self.rect.y < self.game.player1.rect.y:
                 if self.hiding == True:
                    self.vy = 0
                 else:
                    self.vy = 100
            if self.rect.y > self.game.player1.rect.y:
                 if self.hiding == True:
                    self.vy = 0
                 else:
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
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.chase_distance = 500
        self.speed = 300
        self.chasing = True
      
        #self.hitpoints = 100
    def sensor(self):
        if abs(self.rect.x - self.game.player1.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player1.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    
    def update(self):
        #if self.hitpoints <= 0:
            #self.kill()
        # self.sensor()
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
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(WHITE)
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
      
        #self.hitpoints = 100
    def sensor(self):
        if abs(self.rect.x - self.game.player1.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player1.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    
    def update(self):
        #if self.hitpoints <= 0:
            #self.kill()
        # self.sensor()
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