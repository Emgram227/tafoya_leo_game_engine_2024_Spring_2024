import pygame as pg
from settings import *
import sys

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + WIDTH // 2
        y = -target.rect.y + HEIGHT // 2

        # Limit camera to the size of the map
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - WIDTH), x)  # Right
        y = max(-(self.height - HEIGHT), y)  # Bottom

        self.camera = pg.Rect(x, y, self.width, self.height)

camera = Camera(1000, 1000) 
