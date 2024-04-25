import pygame as pg
import sys

# Define the Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SCREEN_WIDTH), x)  # right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

# Define the Player class
class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= 5
        if keys[pg.K_RIGHT]:
            self.rect.x += 5
        if keys[pg.K_UP]:
            self.rect.y -= 5
        if keys[pg.K_DOWN]:
            self.rect.y += 5

# Pygame setup
pg.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

# Create Player object
player = Player(100, 100)

# Create Camera object
camera = Camera(1000, 1000)  # Adjust according to your map size

# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Update
    player.update()  # Update player logic
    camera.update(player)  # Update camera position

    # Draw
    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(player.image, camera.apply(player))  # Draw player with camera offset

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()
