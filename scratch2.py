
import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player with Object")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.holding_object = False

    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= 5
        if keys[pygame.K_s]:
            dy += 5
        if keys[pygame.K_a]:
            dx -= 5
        if keys[pygame.K_d]:
            dx += 5
        self.rect.x += dx
        self.rect.y += dy

# Object class
class GameObject(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((5, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.player1 = player
        self.offset = (50, 0)  # Offset from the player
        self.following = True  # Flag to indicate if the object is following the player

    def update(self):
        if self.following:
            # Set object's position relative to the player
            self.rect.center = (self.player1.rect.centerx + self.offset[0], self.player1.rect.centery + self.offset[1])

# Create player and object instances
player = Player()
game_object = GameObject(player)

# Group for sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player, game_object)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Toggle whether the object follows the player
                game_object.following = not game_object.following

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Update player and object
    player.update(keys)
    game_object.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
