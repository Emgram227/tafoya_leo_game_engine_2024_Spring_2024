import pygame
import math
from math import floor

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Compass Pointer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Timer class
class Timer:
    def __init__(self):
        self.current_time = 0
        self.cd = 0

    def update(self):
        if self.cd > 0:
            self.cd -= 1

    def start_cooldown(self, seconds):
        self.cd = seconds

    def is_ready(self):
        return self.cd == 0

# Compass class
class Compass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame.draw.line(self.image, RED, (50, 50), (85, 50), 2)

    def update(self):
        # Check if it's time to update the compass
        if self.timer.is_ready():
            # Rotate the compass towards the mouse cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.image, int(angle))
            self.rect = self.image.get_rect(center=self.rect.center)
            # Start cooldown
            self.timer.start_cooldown(60)  # 60 frames cooldown (1 second at 60 FPS)

# Create compass instance
compass = Compass()

# Group for sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(compass)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update compass
    compass.update()
    compass.timer.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
