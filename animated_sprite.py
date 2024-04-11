from utils import *
import pygame as pg
from pygame.sprite import Sprite
from os import path

BLACK = (0,0,0)
SPRITESHEET = "theBell.png"

TITLE = "Sprite"
FONT_NAME = "arial"
WIDTH = 300
HEIGHT = 200
FPS = 30
BGCOLOR = (0,0,0)
WHITE = (255,255,255)

dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')


class Animated_sprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.jumping = False
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
                              self.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.spritesheet.get_image(256, 0, 128, 128)
        self.jump_frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jump_frame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    def update(self):
        self.animate()

# FPS = 30

# frames = ["Frame 1", "Frame 2",  "Frame 3",  "Frame 4"] 

# clock = pg.time.Clock()

# current_frame = 0
# last_update = 0

# def animate():
#     global last_update
#     global current_frame
#     now = pg.time.get_ticks()
#     if now - last_update > 350:
#         print(frames[current_frame])
#         current_frame = (current_frame + 1) % len(frames)
#         last_update = now

# while True:
#     clock.tick(FPS)
#     animate()
