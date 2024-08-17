import pygame
import sys
from Body import Body
from Fish import Fish
from Snake import Snake
from Worm import Worm
from Entity import Entity
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
FPS = 60
NUM_FISH = 65

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Animation")

# Clock to control frame rate
clock = pygame.time.Clock()

# Create an instance of Entity
# radius = [16, 28, 32, 26, 16, 9, 7, 7]
radius = [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]


def generate_random_shades(lightness_factor=1.0, darkness_factor=0.4):
    # Generate a random color
    base_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

    def adjust_color(c, factor):
        return tuple(min(max(int(c * factor), 0), 255) for c in c)

    # Create light and dark shades
    light_color = adjust_color(base_color, lightness_factor)
    dark_color = adjust_color(base_color, darkness_factor)

    return base_color, light_color, dark_color


bodies = [Body(WIDTH, HEIGHT) for _ in range(NUM_FISH)]
fishies = []
for i in range(0, NUM_FISH):
    original_color, light_color, dark_color = generate_random_shades()
    fish = Fish(
        WIDTH,
        HEIGHT,
        dark_color,
        light_color,
        bodies[i].position,
        0.4,
        0.9,
    )
    fishies.append(fish)

# player = Fish(
#     WIDTH // 2,
#     HEIGHT // 2,
#     (54, 1, 63),
#     (76, 2, 89),
#     pygame.Vector2(WIDTH // 2, HEIGHT // 2),
#     1,
#     1,
# )

# player = Worm(
#     WIDTH // 2,
#     HEIGHT // 2,
#     12,
#     24,
#     11,
#     (129, 74, 60),
#     pygame.Vector2(WIDTH // 2, HEIGHT // 2),
# )

# player = Snake(
#     WIDTH // 2,
#     HEIGHT // 2,
#     20,
#     16,
#     40,
#     (128, 0, 0),
#     pygame.Vector2(WIDTH // 2, HEIGHT // 2),
# )

player = Entity(
    WIDTH // 2,
    HEIGHT // 2,
    [16, 16, 16, 16, 16, 16, 16, 16],
    48,
    (0, 0, 128),
    pygame.Vector2(WIDTH // 2, HEIGHT // 2),
)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input
    player.handle_input()

    player.update()

    # Update player
    # for i in range(0, NUM_FISH):
    #     bodies[i].update(bodies)
    #     fishies[i].set_position(bodies[i].position)
    #     fishies[i].update()

    # Clear screen
    screen.fill((0, 0, 0))

    player.draw(screen, skelteon=False, skin=True, outline=False)

    # Draw player
    # for fish in fishies:
    #     fish.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
    # print(clock.get_fps())

pygame.quit()
sys.exit()
