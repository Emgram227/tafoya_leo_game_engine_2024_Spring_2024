# This file was created by: Leo Tafoya
''' 
BETA Goals:

Better Textures

Moving Camera

Open World

Release version:
Shop
Weapons
Bosses + More Enemies


'''

#import everything
from utils import *
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path
from scratch import *




#makes Game a class
class Game:
    # initializes the game
    def __init__(self):
        #initializes the game (pygame)
        pg.init()
        # sets the window (width, height and title)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # turns on time
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        # with open(path.join(game_folder, 'map2.txt'), 'rt') as f:
        #     for line in f:
        #         print(line)
        #         self.map_data.append(line)
        self.img_folder = path.join(self.game_folder, 'images')
    # runs the game
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.bushes = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.keys = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobspawner = pg.sprite.Group()
        self.mob_timer = Timer(self)
        self.cooldown = Timer(self)
        self.camera = Camera(WIDTH, HEIGHT, game_map)
        self.round_number = 1
        self.mob_timer.cd = 10 
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row)
                if tile == '2':
                    Stone(self,col,row)
                if tile == 'P':
                    self.player1 = Player(self, col, row)
                if tile == 'C':
                    Coin(self,col,row)
                if tile == 'B':
                    Bush(self,col,row)
                if tile == 'U':
                    PowerUp(self,col,row)
                if tile == 'K':
                    Key(self,col,row)
                if tile == 'D':
                    Chest(self,col,row)
                if tile == 'M':
                    MobSpawner(self,col,row)
                    # if self.cooldown.cd < 1:
                    #     self.cooling = False
                    # if not self.cooling:
                    #        print ("Working")
                    Mob2(self,col,row) 
                                         


    def run(self):
        # creates "while" loop that triggers when running = true
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()
           
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self): 
        self.random = randint(0,3)
        self.cooldown.ticking()
        self.mob_timer.ticking()
        self.all_sprites.update()
        self.camera.update(self.player1)
        if self.mob_timer.cd < 1:
            self.mob_timer.cd = 10
            self.round_number += 1 
            for row, tiles in enumerate(self.map_data):
                for col, tile in enumerate(tiles):
                    if tile == 'M':
                        if self.random == 1:
                                Mob2(self,col,row) 
                        if self.random == 2:
                                Mob(self,col,row)
                        if self.random == 3:        
                                Ghost(self,col,row)         

                        
        
        

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0) , (x,HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y) , (WIDTH, y))
    
    def draw_text(self,surface,text,size,color,x,y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface,text_rect)


    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            # self.all_sprites.draw(self.screen)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            self.draw_text(self.screen, "Round", 24, WHITE, WIDTH/2.3 - 32, 2)
            self.draw_text(self.screen, str(self.round_number), 24, WHITE, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, "Health", 24, WHITE, WIDTH/2.5 - 32, 30)
            self.draw_text(self.screen, str(self.player1.hitpoints), 24, WHITE, WIDTH/2 - 32, 30)
            self.draw_text(self.screen, "Money", 24, WHITE, WIDTH/2.5 - 32, 60)
            self.draw_text(self.screen, str(self.player1.moneybag), 24, WHITE, WIDTH/2 - 32, 60)
            pg.display.flip()
    

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if self.player1.hitpoints < 0:
                self.quit()
            if event.type == pg.KEYDOWN:
                # if event.key == pg.K_r:
                #     self.player1.image.fill(RED)
                # if event.key == pg.K_g:
                #     self.player1.image.fill(GREEN)
                # if event.key == pg.K_b:
                #     self.player1.image.fill(BLUE)
                if event.key == pg.K_r:
                    self.player1.weapon = True
                    print("Weapon Equiped")
                if event.key == pg.K_ESCAPE:
                    self.quit()

            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player1.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player1.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player1.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player1.move(dy=1)
            #     if event.key == pg.K_a:
            #         self.player1.move(dx=-1)
            #     if event.key == pg.K_d:
            #         self.player1.move(dx=1)
            #     if event.key == pg.K_w:
            #         self.player1.move(dy=-1)
            #     if event.key == pg.K_s:
            #         self.player1.move(dy=1)
            #     if event.key == pg.K_SPACE:
            #         self.player1.image.fill == (RED)
            #         pass
    def show_start_screen(self):
        self.screen.fill(BLUE)
        self.draw_text(self.screen,"this is the start screen",100 ,WHITE, WIDTH/6, HEIGHT/2-32)
        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting: 
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.quit:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
            

   


    

# Instantiates the game...
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()

          
    #g.show_start_screen()

