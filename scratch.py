import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
WIDTH = screen_width
HEIGHT = screen_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Object Shooting in Pygame")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the clock
clock = pygame.time.Clock()

# Define the Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Ensure start_x and start_y are integers and within screen bounds
        self.rect.centerx = max(0, min(start_y, WIDTH - 1))
        self.rect.centery = max(0, min(start_y, HEIGHT - 1))
        self.speed = 10
        distance = math.sqrt((target_x - start_x) ** 2 + (target_y - start_y) ** 2)
        self.dx = self.speed * (target_x - start_x) / distance
        self.dy = self.speed * (target_y - start_y) / distance

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Remove bullet if it goes out of screen
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
            self.kill()
# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, start_x, start_y, target_x, target_y):
#         super().__init__()
#         self.image = pygame.Surface((5, 5))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.center = (start_x, start_y)
#         self.speed = 10
#         distance = math.sqrt((target_x - start_x) ** 2 + (target_y - start_y) ** 2)
#         self.dx = self.speed * (target_x - start_x) / distance
#         self.dy = self.speed * (target_y - start_y) / distance

#     def update(self):
#         self.rect.x += self.dx
#         self.rect.y += self.dy
#         # Remove bullet if it goes out of screen
#         if not pygame.Rect(0, 0, screen_width, screen_height).colliderect(self.rect):
#             self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                bullet = Bullet(WIDTH // 2, HEIGHT // 2, mouse_pos[0], mouse_pos[1])
                all_sprites.add(bullet)

    # Clear the screen
    screen.fill(WHITE)

    # Update and draw all sprites
    all_sprites.update()
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
