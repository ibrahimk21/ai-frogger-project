import pygame
import sys

# --- 1. Initialize Pygame ---
pygame.init()

# --- 2. Set Up Your Game Window ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Create the screen (the window)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My 2D Physics Driver")

# --- 3. Define Your Colors (as RGB tuples) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (200, 0, 0)

# --- 4. The Main Game Loop ---
# This loop is the heart of your game. It runs continuously.
running = True
while running:

    # --- 5. Event Handling ---
    # Check for any user input (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # User clicked the 'X' button
            running = False

    # --- 6. Game Logic (Update Game State) ---
    # (Right now, we have no logic. Later, this is where you'll
    #  update the car's position, check for collisions, etc.)
    pass

    # --- 7. Drawing (Render the Screen) ---
    # First, fill the screen with a background color
    screen.fill(BLACK)

    # Draw your "ground" (a simple green rectangle at the bottom)
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

    # Draw your "car" (a simple red rectangle)
    pygame.draw.rect(screen, RED, (100, SCREEN_HEIGHT - 150, 80, 50))  # (x, y, width, height)

    # --- 8. Flip the Display ---
    # This command tells Pygame to show everything you've drawn
    pygame.display.flip()

# --- 9. Quit Pygame ---
# This runs *after* the loop is broken
pygame.quit()
sys.exit()