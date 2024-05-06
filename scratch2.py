
import pygame as pg
import math

# Initialize Pygame
pg.init()

# Set up the screen
WIDTH, HEIGHT = 1024, 768
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Player with Object")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player class
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.holding_object = False
        # self.game_object = game_object

    def update(self, keys):
        # self.collide_with_group(self.game_object, True)
        dx, dy = 0, 0
        if keys[pg.K_w]:
            dy -= 5
        if keys[pg.K_s]:
            dy += 5
        if keys[pg.K_a]:
            dx -= 5
        if keys[pg.K_d]:
            dx += 5
        self.rect.x += dx
        self.rect.y += dy
        
    def collide_with_group(self,group,kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
             if str(hits[0].__class__.__name__) == "GameObject":
                 self.holding_object = True
                 game_object.following = True
                 print("Works")

# Object class
class GameObject(pg.sprite.Sprite):
    def __init__(self, player1):
        super().__init__()
        self.image = pg.Surface((5, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.player1 = player1
        self.offset = (50, 0)  # Offset from the player
        self.following = False # Flag to indicate if the object is following the player

    def collide_with_group(self,group,kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
             if str(hits[0].__class__.__name__) == "Player":
                player1.holding_object = True
                self.following = True

    def update(self):
        if self.following:
            # Set object's position relative to the player
            self.rect.center = (self.player1.rect.centerx + self.offset[0], self.player1.rect.centery + self.offset[1])

# Create player and object instances
player1 = Player()
game_object = GameObject(player1)

# Group for sprites
all_sprites = pg.sprite.Group()
all_sprites.add(player1, game_object)

# Main loop
running = True
while running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # Toggle whether the object follows the player
                game_object.following = not game_object.following

    # Get pressed keys
    keys = pg.key.get_pressed()

    # Update player and object
    player1.update(keys)
    game_object.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pg.display.flip()

    # Cap the frame rate
    pg.time.Clock().tick(60)

pg.quit()
