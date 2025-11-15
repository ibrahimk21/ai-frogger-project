import pygame
import sys
import random

# --- 1. Game Constants ---
TILE_SIZE = 40
GRID_WIDTH = 13
GRID_HEIGHT = 14

SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

# Colors
COLOR_BACKGROUND = (0, 0, 0)
COLOR_ROAD = (40, 40, 40)
COLOR_WATER = (0, 0, 150)
COLOR_SAFE = (0, 150, 0)
COLOR_GOAL = (0, 200, 0)
COLOR_FROG = (0, 255, 0)
COLOR_CAR = (200, 0, 0)
COLOR_LOG = (150, 75, 0)

# Define the layout of the level (which rows are what)
# 0=Safe, 1=Road, 2=Water, 3=Goal
ROW_TYPES = [
    3,  # 0: Goal
    2,  # 1: Water
    2,  # 2: Water
    2,  # 3: Water
    2,  # 4: Water
    2,  # 5: Water
    0,  # 6: Safe Grass
    1,  # 7: Road
    1,  # 8: Road
    1,  # 9: Road
    1,  # 10: Road
    1,  # 11: Road
    0,  # 12: Safe Grass
    0  # 13: Start (Safe)
]


class Player:
    """The Frog!"""

    def __init__(self):
        self.reset()

    def reset(self):
        # Start at the bottom, center
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT - 1

    def move(self, dx, dy):
        """Move the player by one tile in the grid."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check screen boundaries
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.x = new_x
            self.y = new_y
            return True  # Successful move
        return False  # Hit a wall

    def draw(self, surface):
        rect = (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, COLOR_FROG, rect)


class Obstacle:
    """A generic class for Cars and Logs."""

    def __init__(self, y, x_start, speed, color, is_log=False):
        self.y = y
        self.x = x_start
        self.speed = speed
        self.color = color
        self.is_log = is_log
        self.width = random.randint(2, 4)  # Obstacles are 2-4 tiles wide

    def update(self):
        """Move the obstacle."""
        self.x += self.speed
        # Wrap around the screen
        if self.x > GRID_WIDTH and self.speed > 0:
            self.x = -self.width
        elif self.x < -self.width and self.speed < 0:
            self.x = GRID_WIDTH

    def draw(self, surface):
        # We use floating-point for smooth movement
        pixel_x = int(self.x * TILE_SIZE)
        pixel_y = int(self.y * TILE_SIZE)
        pixel_width = int(self.width * TILE_SIZE)

        rect = (pixel_x, pixel_y, pixel_width, TILE_SIZE)
        pygame.draw.rect(surface, self.color, rect)

    def get_rect(self):
        """Get the integer grid-space rect for collisions."""
        return pygame.Rect(int(self.x), self.y, self.width, 1)


class Game:
    """The main AI-ready environment class."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Frogger AI Environment")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.player = Player()
        self.obstacles = []
        self.frame_count = 0
        self.reset()

    def _spawn_obstacles(self):
        """Create the random cars and logs for the level."""
        self.obstacles = []
        for y, row_type in enumerate(ROW_TYPES):
            if row_type == 1:  # Road
                speed = random.choice([-0.1, 0.1, -0.05, 0.05])
                for x_start in range(0, GRID_WIDTH, random.randint(5, 8)):
                    self.obstacles.append(Obstacle(y, x_start, speed, COLOR_CAR))
            elif row_type == 2:  # Water
                speed = random.choice([-0.07, 0.07, -0.03, 0.03])
                for x_start in range(0, GRID_WIDTH, random.randint(6, 9)):
                    self.obstacles.append(Obstacle(y, x_start, speed, COLOR_LOG, is_log=True))

    def reset(self):
        """Reset the game to the starting state. (AI-facing function)"""
        self.player.reset()
        self._spawn_obstacles()
        self.frame_count = 0
        print("--- GAME RESET ---")
        # In the future, this will return the initial AI 'state'
        # return self.get_state()

    def step(self, action):
        """
        Take one step in the game. (AI-facing function)
        'action' will be 0:Up, 1:Down, 2:Left, 3:Right
        """
        self.frame_count += 1

        # --- 1. Handle Player Movement ---
        moved_forward = False
        if action == 0:  # Up
            moved_forward = self.player.move(0, -1)
        elif action == 1:  # Down
            self.player.move(0, 1)
        elif action == 2:  # Left
            self.player.move(-1, 0)
        elif action == 3:  # Right
            self.player.move(1, 0)

        # --- 2. Update all Obstacles ---
        for obs in self.obstacles:
            obs.update()

        # --- 3. Check for Collisions & Calculate Reward/Done ---
        reward = -0.01  # Small time penalty
        done = False

        player_pos = (self.player.x, self.player.y)
        player_rect = pygame.Rect(self.player.x, self.player.y, 1, 1)
        row_type = ROW_TYPES[self.player.y]

        if row_type == 3:  # Goal
            print("WIN!")
            reward = 100
            done = True
        elif row_type == 1:  # Road
            if moved_forward: reward = 0.1  # Small reward for progress
            for obs in self.obstacles:
                if obs.is_log: continue
                if obs.get_rect().colliderect(player_rect):
                    print("SPLAT!")
                    reward = -100
                    done = True
                    break
        elif row_type == 2:  # Water
            on_log = False
            for obs in self.obstacles:
                if not obs.is_log: continue
                if obs.get_rect().colliderect(player_rect):
                    on_log = True
                    # Move player with the log
                    self.player.x += obs.speed
                    break

            if not on_log:
                print("SPLASH!")
                reward = -100
                done = True
            else:
                if moved_forward: reward = 1.0  # Big reward for water progress
        else:  # Safe grass
            if moved_forward: reward = 0.1

        # Check for out-of-bounds (if log carries player)
        if not (0 <= self.player.x < GRID_WIDTH):
            print("SPLASH! (Off-screen)")
            reward = -100
            done = True

        # In the future, this will return (state, reward, done)
        return reward, done

    def draw(self):
        """Draw everything to the screen."""
        self.screen.fill(COLOR_BACKGROUND)

        # Draw the level tiles
        for y, row_type in enumerate(ROW_TYPES):
            color = COLOR_BACKGROUND
            if row_type == 0:
                color = COLOR_SAFE
            elif row_type == 1:
                color = COLOR_ROAD
            elif row_type == 2:
                color = COLOR_WATER
            elif row_type == 3:
                color = COLOR_GOAL
            rect = (0, y * TILE_SIZE, SCREEN_WIDTH, TILE_SIZE)
            pygame.draw.rect(self.screen, color, rect)

        # Draw obstacles
        for obs in self.obstacles:
            obs.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """Main loop for human play."""
        running = True
        while running:
            # --- Human Input ---
            action = -1  # No action
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        action = 0
                    elif event.key == pygame.K_DOWN:
                        action = 1
                    elif event.key == pygame.K_LEFT:
                        action = 2
                    elif event.key == pygame.K_RIGHT:
                        action = 3

            # --- Game Step ---
            if action != -1:
                reward, done = self.step(action)
                if done:
                    self.reset()

            # --- Update non-player things ---
            if action == -1:
                self.step(-1)  # "Wait" action

            # --- Draw ---
            self.draw()
            self.clock.tick(15)  # Run at 15 FPS

        pygame.quit()
        sys.exit()


# --- Main execution ---
if __name__ == "__main__":
    game = Game()
    game.run()