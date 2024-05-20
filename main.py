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
from camera import *




#makes Game a class
class Game:
    # initializes the game
    def __init__(self):
        #initializes the game (pygame)
        pg.init()
        pg.mixer.init()
        # sets the window (width, height and title)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # turns on time
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, CURRENT_MAP))
        # self.map = Map(path.join(game_folder, levels[self.current_level]))
        self.map_data = []
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
        self.snd_folder = path.join(self.game_folder, 'sounds')
        self.player_img = pg.image.load(path.join(self.img_folder, 'theBell.png')).convert_alpha()
    # runs the game
    def new(self):
        # self.radio1 = pg.mixer.Sound(path.join(self.snd_folder, '.wav'))
        # self.radio2 = pg.mixer.Sound(path.join(self.snd_folder, '.wav'))
        # self.radio3 = pg.mixer.Sound(path.join(self.snd_folder,'.wav'))
        # self.radio4 = pg.mixer.Sound(path.join(self.snd_folder, '.wav'))
        self.radio_name = "Nothing"
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.walkthroughs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.game_object = pg.sprite.Group()
        # self.gameobject = GameObject()
        self.keys = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        self.mobspawner = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mob_timer = Timer(self)
        self.cooldown = Timer(self)
        self.camera = Camera()
        self.round_number = 1
        self.mob_timer.cd = 10
        self.magazine = 10
        self.ammo = 50
        self.sold1 = False
        self.sold2 = False
        self.sold3 = False
        self.sold4 = False
        self.shop_timer1 = Timer(self)
        self.shop_timer1.cd = 60
        self.shop_timer2 = Timer(self)
        self.shop_timer2.cd = 60
        self.shop_timer3 = Timer(self)
        self.shop_timer3.cd = 60
        self.shop1_message = " 'I need more boolets' "
        self.shop2_message = "Completely heals you"
        self.shop3_message = "Brings up speed by tiny amount"
        self.shop4_message = "Definitely not stolen from Fallout"
        self.play_radio = False
        # self.health_bar = HealthBar(self, self.player1.rect.x, self.player1.rect.y - 20, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT, self.player1, 100)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row)
                if tile == '2':
                    Stone(self,col,row)
                if tile == '3':
                    Water(self,col,row)
                if tile == '4':
                    Wood(self,col,row)
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
                if tile == 'G':
                    Boss(self,col,row)
                if tile == "S":
                    Shop(self,col,row)
                if tile == "N":
                    Npc(self,col,row)

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
        # self.mouse_pos = pg.mouse.get_pos()
        if paused == False:
            if self.player1.shop_open == False:
                self.cooldown.ticking()
                self.mob_timer.ticking()
        if self.sold1 == True:
            self.shop1_message = (str(self.shop_timer1.cd))
            self.shop_timer1.ticking()
        if self.sold2 == True:
            self.shop2_message = (str(self.shop_timer2.cd))
            self.shop_timer2.ticking()
        if self.sold3 == True:
            self.shop3_message = (str(self.shop_timer3.cd))
            self.shop_timer3.ticking()
        if self.sold4 == True:
            self.shop4_message = "Sold Out"
        self.all_sprites.update()
        self.all_sprites.add(self.player1, self.game_object)
        self.game_object.update()
        self.camera.update(self.player1)
        
        if self.shop_timer1.cd < 1:
            self.sold1 = False
            self.shop1_message = " 'I need more boolets' "
        if self.shop_timer2.cd < 1:
            self.sold2 = False
            self.shop2_message = "Completely heals you"
        if self.shop_timer3.cd < 1:
            self.sold3 = False
            self.shop3_message = "Brings up speed by tiny amount"

        if self.mob_timer.cd < 1:
            self.mob_timer.cd = 10
            self.round_number += 1 
            for row, tiles in enumerate(self.map.data):
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
            pg.draw.line(self.screen, BGCOLOR, (x,0) , (x,HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BGCOLOR, (0,y) , (WIDTH, y))
    
    def draw_text(self,surface,text,size,color,x,y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface,text_rect)

    # def draw_health_bar(self):
    #     # calculate health ratio
    #     health_ratio = self.player1.hitpoints / self.player1.maxhitpoints
    #     # calculate width of health bar
    #     health_width = int(self.player1.rect.width * health_ratio)
    #     # create health bar
    #     health_bar = pg.Rect(0, 0, health_width, 7)
    #     # position health bar
    #     health_bar.midtop = self.player1.rect.midtop
    #     # draw health bar
    #     pg.draw.rect(self.player1.image, GREEN, health_bar)


    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            # for row, tiles in enumerate(game_map.data):
            #      for col, tile in enumerate(tiles):
            #      # Draw tiles at the correct position with camera offset
            #          self.screen.blit(, (col * TILESIZE - self.camera.camera.x, row * TILESIZE - self.camera.camera.y))

            # self.all_sprites.draw(self.screen)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            self.draw_text(self.screen, "Round", 24, WHITE, WIDTH/2.3 - 32, 2)
            self.draw_text(self.screen, str(self.round_number), 24, WHITE, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, "Health", 24, WHITE, WIDTH/2.5 - 32, 30)
            self.draw_text(self.screen, str(self.player1.hitpoints), 24, WHITE, WIDTH/2 - 32, 30)
            self.draw_text(self.screen, "Money", 24, WHITE, WIDTH/2.5 - 32, 60)
            self.draw_text(self.screen, str(self.player1.moneybag), 24, WHITE, WIDTH/2 - 32, 60)
            self.draw_text(self.screen, "Ammo", 24, WHITE, WIDTH/2.5 - 32, 90)
            if self.ammo > 0:
                if self.magazine > 0:
                    self.draw_text(self.screen, str(self.magazine), 24, WHITE, WIDTH/2 - 32, 90)
                else:
                    self.draw_text(self.screen, "Reload", 24, WHITE, WIDTH/2 - 32, 90)
            else:
                self.draw_text(self.screen, "Out of Ammo", 24, WHITE, WIDTH/2 - 32, 90)
            # self.draw_health_bar(self.screen, self.player1.rect.x, self.player1.rect.y-8, self.player1.hitpoints)
            # Modified from ChatGPT
            if self.player1.shop_open == True:

                # Draw the menu background
                menu_bg = pg.Surface((600, 600))
                menu_bg.fill((0, 0, 0))
                menu_bg.set_alpha(150)  # Transparency
                self.screen.blit(menu_bg, (100, 150))

                font = pg.font.Font(None, 50)
                subfont = pg.font.Font(None, 30)
                text1 = font.render("Game Shop", True, WHITE)
                self.screen.blit(text1, (100, 100)) 
                text2 = font.render("Press SPACE to close", True, WHITE)
                self.screen.blit(text2, (100, 150)) 

                box1 = pg.Surface((500, 100)) # Size
                box1.fill(YELLOW) # Color
                box1.set_alpha(150)  # Transparency
                self.screen.blit(box1, (150, 200)) # Position
                option1 = font.render("50 Bullets: $20 (Press 1)", True, WHITE)
                self.screen.blit(option1, (160, 210)) 
                subtext1 = subfont.render(self.shop1_message, True, WHITE)
                self.screen.blit(subtext1, (160, 250)) 

                box2 = pg.Surface((500, 100))
                box2.fill(GREEN)
                box2.set_alpha(150)
                self.screen.blit(box2, (150, 320)) 
                option2 = font.render("Full Heal: $40 (Press 2)", True, WHITE)
                self.screen.blit(option2, (160, 330)) 
                subtext2 = subfont.render(self.shop2_message, True, WHITE)
                self.screen.blit(subtext2, (160, 370)) 

                box3 = pg.Surface((500, 100))
                box3.fill(RED)
                box3.set_alpha(150) 
                self.screen.blit(box3, (150, 440))
                option3 = font.render("Speed Boost: $60 (Press 3)", True, WHITE)
                self.screen.blit(option3, (160, 450)) 
                subtext3 = subfont.render(self.shop3_message, True, WHITE)
                self.screen.blit(subtext3, (160, 490)) 

                box4 = pg.Surface((500, 100))
                box4.fill(BLUE)
                box4.set_alpha(150)
                self.screen.blit(box4, (150, 560))
                option4 = font.render("Radio: $80 (Press 4)", True, WHITE)
                self.screen.blit(option4, (160, 570))
                subtext3 = subfont.render(self.shop4_message, True, WHITE)
                self.screen.blit(subtext3, (160, 610)) 
                
            if paused == True:
                # Modified Shop Menu
                menu_bg = pg.Surface((WIDTH, HEIGHT))
                menu_bg.fill((0, 0, 0))
                menu_bg.set_alpha(150)  # Transparency
                self.screen.blit(menu_bg, (0,0))

                font = pg.font.Font(None, 50)
                text = font.render("Paused (Press any Key)", True, WHITE)
                self.screen.blit(text, (100, 150)) 

            if self.play_radio == True:
                menu_bg = pg.Surface((300, 50))
                menu_bg.fill((0, 0, 0))
                menu_bg.set_alpha(150)  # Transparency
                self.screen.blit(menu_bg, (750, 10))
                
                font = pg.font.Font(None, 30)
                text = font.render("Now Playing:", True, WHITE)
                self.screen.blit(text, (750, 15)) 
                text = font.render(self.radio_name, True, WHITE)
                self.screen.blit(text, (885, 15)) 
            
            if showinventory == True:
                menu_bg = pg.Surface((WIDTH, HEIGHT))
                menu_bg.fill((0, 0, 0))
                menu_bg.set_alpha(150)  # Transparency
                self.screen.blit(menu_bg, (0,0))
                
                font = pg.font.Font(None, 50)
                text1 = font.render("Inventory:", True, WHITE)
                self.screen.blit(text1, (100, 100)) 
                text2 = font.render(str(self.ammo), True, WHITE)
                self.screen.blit(text2, (230, 150)) 
                text3 = font.render("Ammo:", True, WHITE)
                self.screen.blit(text3, (100, 150)) 
                text4 = font.render(str(self.player1.moneybag), True, WHITE)
                self.screen.blit(text4, (230, 200)) 
                text5 = font.render("Money:", True, WHITE)
                self.screen.blit(text5, (100, 200)) 
                text6 = font.render(str(self.play_radio), True, WHITE)
                self.screen.blit(text6, (230, 250)) 
                text7 = font.render("Radio:", True, WHITE)
                self.screen.blit(text7, (100, 250)) 
                




            pg.display.flip()
    

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if self.player1.hitpoints <= 0:
                self.quit()
            if event.type == pg.KEYDOWN:
                # if event.key == pg.K_r:
                #     self.player1.image.fill(RED)
                # if event.key == pg.K_g:
                #     self.player1.image.fill(GREEN)
                # if event.key == pg.K_b:
                #     self.player1.image.fill(BLUE)
                if event.key == pg.K_r:
                    if self.ammo > 0:
                        self.magazine = 10
                        self.ammo -= 10
                        print(self.magazine)
                        print(self.ammo)
                    # self.player1.weapon = True
                    # print("Weapon Equiped")
                if event.key == pg.K_ESCAPE:
                    self.quit()
                # if event.key == pg.K_SPACE:
                #     self.game_object.following = not self.game_object.following
                if event.key == pg.K_p:
                        global paused
                        paused = True
                        self.player1.paused = True
                else:
                    paused = False
                    self.player1.paused = False
                if event.key == pg.K_1:
                    if self.player1.shop_open == True:
                        if self.sold1 == False:
                            if self.player1.moneybag >= 20:
                                self.player1.moneybag -= 20
                                self.sold1 = True
                                self.ammo += 50
                                print("SOLD")
                            else:
                                print("Not Enough Money")
                    else:
                        if self.play_radio == True:
                            self.radio_name = "Doom Music"
                if event.key == pg.K_2:
                    if self.player1.shop_open == True:
                        if self.sold2 == False:
                            if self.player1.moneybag >= 40:
                                self.player1.moneybag -= 40
                                self.sold2 = True
                                self.player1.hitpoints = 100
                                print("SOLD")
                            else:
                                print("Not Enough Money")
                    else:
                        if self.play_radio == True:
                            self.radio_name = "Portal Music"
                if event.key == pg.K_3:
                    if self.player1.shop_open == True:
                        if self.sold3 == False:
                            if self.player1.moneybag >= 60:
                                self.player1.moneybag -= 60
                                self.player1.speed += 50
                                self.sold3 = True
                                print("SOLD")
                            else:
                                print("Not Enough Money")
                    else:
                        if self.play_radio == True:
                            self.radio_name = "Mario Music"
                if event.key == pg.K_4:
                    if self.player1.shop_open == True:
                        if self.sold4 == False:
                            if self.player1.moneybag >= 80:
                                self.player1.moneybag -= 80
                                self.sold4 = True
                                self.play_radio = True
                                print("SOLD")
                            else:
                                print("Not Enough Money")
                    else:
                        if self.play_radio == True:
                            self.radio_name = "Game Music"
                if event.key == pg.K_5:
                    if self.play_radio == True:
                        self.radio_name = "Nothing"
                if event.key == pg.K_e:
                    global showinventory
                    showinventory = True
                    self.player1.paused = True
                else:
                    showinventory = False
                    
            elif event.type == pg.MOUSEBUTTONDOWN:
                     if event.button == 1:  # Left mouse button
                        if self.magazine > 0:
                            self.magazine -= 1
                            self.mouse_x, self.mouse_y = event.pos
                            self.player_posx = self.player1.rect.centerx
                            self.player_posy = self.player1.rect.centery
                            # self.mouse_pos = pg.mouse.get_pos()
                             # Get the adjusted mouse position relative to the game world
                            self.camera_offset_x = self.camera.camera.x
                            self.camera_offset_y = self.camera.camera.y
                            self.mouse_pos = (event.pos[0] + self.camera_offset_x, event.pos[1] + self.camera_offset_y)
                            self.bullet = Bullet(self, self.player_posx , self.player_posy, self.mouse_pos[0], self.mouse_pos[1])
                            print(self.mouse_pos[0])
                            print(self.mouse_pos[1])
                            self.all_sprites.add(self.bullet)


            #     if event.key == pg.K_LEFT:
            #       self.player1.move(dx=-1)
            #   if event.key == pg.K_RIGHT:
            #       self.player1.move(dx=1)
            #   if event.key == pg.K_UP:w
            #       self.player1.move(dy=-1)
            #   if event.key == pg.K_DOWN:
            #       self.player1.move(dy=1)
            #   if event.key == pg.K_a:s
            #       self.player1.move(dx=-1)
            #   if event.key == pg.K_d:
            #       self.player1.move(dx=1)
            #   if event.key == pg.K_w:
            #       self.player1.move(dy=-1)
            #   if event.key == pg.K_s:
            #       self.player1.move(dy=1)

    def show_start_screen(self):
        self.spritesheet = Spritesheet(path.join(img_folder, 'boss.png'))
        # self.screen.fill(BLUE)
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
                if event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False

# Instantiates the game...
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()

          
    #g.show_start_screen()

