# This file was created by: Leo Tafoya

#import everything 
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

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
        game_folder = path.dirname(__file__)
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
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # runs the game
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.bushes = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.keys = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
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
                    Door(self,col,row)

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
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0) , (x,HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y) , (WIDTH, y))

    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.player1.image.fill(RED)
                if event.key == pg.K_g:
                    self.player1.image.fill(GREEN)
                if event.key == pg.K_b:
                    self.player1.image.fill(BLUE)
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
                    
            


    

# Instantiates the game...
g = Game()
# use game method run to run
while True:
    g.new()
    g.run()
    #g.show_start_screen()
