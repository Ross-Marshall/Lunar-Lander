import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Gravity and thrust settings
GRAVITY = 0.05
THRUST = -0.1

# Lander settings
lander_width, lander_height = 40, 60
lander_x = WIDTH // 2
lander_y = 50
lander_dx = 0
lander_dy = 0
lander_speed = 2
fuel = 100

# Landing pad settings
pad_width = 100
pad_height = 10
pad_x = WIDTH // 2 - pad_width // 2
pad_y = HEIGHT - pad_height - 10

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lunar Lander")

# Fonts
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()
FPS = 60

def draw_scene():
    screen.fill(BLACK)

    # Draw the lander
    pygame.draw.rect(screen, WHITE, (lander_x, lander_y, lander_width, lander_height))

    # Draw the landing pad
    pygame.draw.rect(screen, GREEN, (pad_x, pad_y, pad_width, pad_height))

    # Display fuel
    fuel_text = font.render(f"Fuel: {fuel}", True, WHITE)
    screen.blit(fuel_text, (10, 10))

    pygame.display.flip()

def check_landing():
    global lander_dy

    if pad_x <= lander_x <= pad_x + pad_width - lander_width and lander_y + lander_height >= pad_y:
        if abs(lander_dy) <= 1:
            return "success"
        else:
            return "crash"
    elif lander_y + lander_height >= HEIGHT:
        return "crash"
    return None

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Apply thrust
    if keys[pygame.K_SPACE] and fuel > 0:
        lander_dy += THRUST
        fuel -= 1

    # Update lander position
    lander_dy += GRAVITY
    lander_x += lander_dx
    lander_y += lander_dy

    # Check for landing or crash
    result = check_landing()
    if result == "success":
        print("Successful landing!")
        running = False
    elif result == "crash":
        print("You crashed!")
        running = False

    # Draw the scene
    draw_scene()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()

