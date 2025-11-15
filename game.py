import pygame
import sys
import os

# --- 1. Initialize Pygame ---
pygame.init()

# --- 2. Set Up Your Game Window ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My 2D Physics Driver")


# --- 3. Asset Loading Function ---
def load_image(file_name, scale=None):
    """Loads, scales, and converts an image for performance."""
    assets_path = os.path.join(os.path.dirname(__file__), 'assets')
    full_path = os.path.join(assets_path, file_name)

    try:
        image = pygame.image.load(full_path).convert_alpha()
    except pygame.error as e:
        print(f"Cannot load image: {file_name}")
        raise SystemExit(e)

    if scale:
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        image = pygame.transform.scale(image, (width, height))

    return image


# --- 4. Load Your Assets ---
# Load the background and scale it to fit the screen
bg_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'background.png')).convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the truck parts (let's scale them down by 50% as an example)
scale_factor = 0.5
body_image = load_image('truckbody.png', scale=scale_factor)
wheel_image = load_image('truckwheel.png', scale=scale_factor)

# Get the dimensions for positioning
body_width = body_image.get_width()
body_height = body_image.get_height()
wheel_width = wheel_image.get_width()
wheel_height = wheel_image.get_height()

# --- 5. The Main Game Loop ---
running = True
while running:

    # --- 6. Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 7. Game Logic ---
    # (No physics... yet!)

    # --- 8. Drawing (Render the Screen) ---

    # Draw the background first
    screen.blit(bg_image, (0, 0))

    # --- Draw the "Assembled" Truck ---
    # These are just placeholder values to "fake" the truck's position
    # This is *not* physics, just a visual test.

    # Base position for the truck body
    body_x = 100
    body_y = 350

    # Calculate wheel positions *relative* to the body
    # You will need to TWEAK these numbers to make it look right!
    front_wheel_x = body_x + 30
    front_wheel_y = body_y + 50

    back_wheel_x = body_x + 120
    back_wheel_y = body_y + 50

    # Draw the parts
    # The wheels are drawn *first* so they appear "behind" the body
    screen.blit(wheel_image, (front_wheel_x, front_wheel_y))
    screen.blit(wheel_image, (back_wheel_x, back_wheel_y))
    screen.blit(body_image, (body_x, body_y))

    # --- 9. Flip the Display ---
    pygame.display.flip()

# --- 10. Quit Pygame ---
pygame.quit()
sys.exit()