#this file was created by Leo Tafoya
import pygame as pg

#Fullscreen Values
fsHeight = 1440
fsWidth = 960 #Use 900 for fullscreen + top tab

#Regular Values
regHeight = 1024
regWidth = 768

WIDTH = regHeight # just change to numbers if you want
HEIGHT = regWidth

FPS = 30

TITLE = "My Game"

TILESIZE = 32
WHITE = (255,255,255)
GREEN =  (0,255,0)
RED = (255,0,0)
LIGHTGREY = (75,75,75)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BGCOLOR = (15,15,15)
BLACK = (0,0,0)
PURPLE = (255,0,255)
BROWN = (75,75,0)
ORANGE = (255,100,0)
CURRENT_MAP = 'map2.txt'

MOB_HIT_RECT = pg.Rect(0,0,32,32)

PLAYER_SPEED = 300

global doorKey
doorKey = False

global powerUp
powerUp = False

global hiding
hiding = False
