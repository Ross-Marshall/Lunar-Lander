import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
LIGHT_GRAY = (169, 169, 169)
RED = (255, 0, 0)
TAN = (210, 180, 140)

# Gravity and thrust settings
GRAVITY = 0.05
THRUST = -0.1

# Lander settings
def reset_game():
    global lander_x, lander_y, lander_dx, lander_dy, fuel, lander_width, lander_height, game_active, crashed_parts
    lander_width = 60
    lander_height = 10
    lander_x = WIDTH // 2
    lander_y = 50
    lander_dx = 0
    lander_dy = 0
    fuel = 100
    game_active = True
    crashed_parts = []

reset_game()

# Landing pad settings
pad_width = WIDTH  # Extend the landing pad to cover the entire screen width
pad_height = 5  # Make the landing pad thinner
pad_x = 0  # Start from the left edge
pad_y = HEIGHT - pad_height  # Move to the very bottom

# Generate star field
num_stars = 100
stars = [(random.randint(0, WIDTH), random.randint(0, pad_y - 10)) for _ in range(num_stars)]

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

    # Draw the star field
    for star in stars:
        pygame.draw.circle(screen, LIGHT_GRAY, star, 2)

    # Draw the lander or crashed parts
    if crashed_parts:
        for part in crashed_parts:
            pygame.draw.rect(screen, RED, part)
    else:
        draw_lander()

    # Draw the landing pad
    pygame.draw.rect(screen, TAN, (pad_x, pad_y, pad_width, pad_height))

    # Display fuel
    fuel_text = font.render(f"Fuel: {fuel}", True, LIGHT_GRAY)
    screen.blit(fuel_text, (10, 10))

    # Display speed
    speed_text = font.render(f"Speed: {lander_dy:.2f}", True, LIGHT_GRAY)
    screen.blit(speed_text, (10, 50))

    # Display altitude
    altitude = max(0, pad_y - (lander_y + lander_height))
    altitude_text = font.render(f"Altitude: {altitude}", True, LIGHT_GRAY)
    screen.blit(altitude_text, (10, 90))

    pygame.display.flip()

def draw_lander():
    global lander_x, lander_y
    # Define the shape of the lander based on the new coordinates
    disc_shape = [
        (lander_x, lander_y),  # (0,0)
        (lander_x + 10, lander_y - 10),  # (10,-10)
        (lander_x + 20, lander_y - 14),  # (20,-14)
        (lander_x + 40, lander_y - 14),  # (40,-14)
        (lander_x + 50, lander_y - 10),  # (50,-10)
        (lander_x + 60, lander_y),  # (60,0)
        (lander_x + 45, lander_y + 6),  # (45,6)
        (lander_x + 40, lander_y + 6),  # (40,6)
        (lander_x + 40, lander_y + 10),  # (40,10)
        (lander_x + 20, lander_y + 10),  # (20,10)
        (lander_x + 20, lander_y + 6),  # (20,6)
        (lander_x + 15, lander_y + 6),  # (15,6)
        (lander_x, lander_y)  # Close the shape
    ]
    pygame.draw.polygon(screen, LIGHT_GRAY, disc_shape)

    # Draw the circle on top of the lander
    pygame.draw.circle(screen, LIGHT_GRAY, (lander_x + 30, lander_y - 14), 2)  # (x, y, radius)

def check_landing():
    global lander_dy, crashed_parts, game_active

    if pad_x <= lander_x <= pad_x + pad_width - lander_width and lander_y + lander_height >= pad_y:
        if abs(lander_dy) <= 1:
            return "success"
        else:
            return "crash"
    elif lander_y + lander_height >= HEIGHT:
        return "crash"
    return None

def handle_crash():
    global crashed_parts
    for _ in range(10):
        part_x = lander_x + random.randint(-20, 20)
        part_y = pad_y - random.randint(0, 10)
        part_width = random.randint(5, 10)
        part_height = random.randint(5, 10)
        crashed_parts.append(pygame.Rect(part_x, part_y, part_width, part_height))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:  # New Game shortcut
            reset_game()

    if game_active:
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
            print("Successful landing! Press 'N' for a New Game.")
            game_active = False
        elif result == "crash":
            print("You crashed! Press 'N' for a New Game.")
            handle_crash()
            game_active = False

    # Draw the scene
    draw_scene()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()

