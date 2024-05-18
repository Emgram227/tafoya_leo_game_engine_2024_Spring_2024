import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Collision Shop Example")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Define Shop class
class Shop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (600, 300)

# Create instances of Player and Shop
player = Player()
shop = Shop()

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(shop)

# Main game loop
running = True
shop_open = False
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if shop_open and event.key == pygame.K_SPACE:
                shop_open = False
                paused = False
                

    if not paused:
        # Update all sprites
        all_sprites.update()

        # Check for collision between player and shop
        if pygame.sprite.collide_rect(player, shop):
            shop_open = True
            paused = True
            

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display shop open menu
    if shop_open == True:
        font = pygame.font.Font(None, 74)
        text = font.render("Shop Open", True, GREEN)
        screen.blit(text, (200, 150))

        # Draw the menu background
        menu_bg = pygame.Surface((400, 300))
        menu_bg.fill((0, 0, 0))
        menu_bg.set_alpha(150)  # Transparency
        screen.blit(menu_bg, (200, 150))

        # Draw menu options
        font = pygame.font.Font(None, 50)
        text = font.render("Press SPACE to close", True, WHITE)
        screen.blit(text, (250, 250))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

