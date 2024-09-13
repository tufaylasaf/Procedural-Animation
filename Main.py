import pygame
import sys
from Body import Body
from Fish import Fish
from Snake import Snake
from Worm import Worm
from Entity import Entity
from Lizard import Lizard
import random
import colorsys

pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60
NUM_FISH = 72

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Animation")

# Clock to control frame rate
clock = pygame.time.Clock()

# Create an instance of Entity
# radius = [16, 28, 32, 26, 16, 9, 7, 7]
radius = [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]


def generate_random_shades(lightness_factor=1.1, darkness_factor=0.4):
    # Generate a random base color using HSL model for better control over brightness
    hue = random.random()  # Random hue value between 0 and 1
    saturation = (
        0.8 + random.random() * 0.2
    )  # High saturation for vibrant color (0.8 to 1)
    lightness = 0.5  # Moderate lightness for a bright color

    # Convert HSL to RGB
    base_color = tuple(
        round(i * 255) for i in colorsys.hls_to_rgb(hue, lightness, saturation)
    )

    def adjust_color(c, factor):
        # Adjust the lightness of the color to generate light and dark shades
        h, l, s = colorsys.rgb_to_hls(*[x / 255.0 for x in c])
        l = max(0, min(1, l * factor))  # Keep lightness in [0, 1] range
        return tuple(round(i * 255) for i in colorsys.hls_to_rgb(h, l, s))

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
        0.35,
        0.9,
    )
    fishies.append(fish)

player = Fish(
    WIDTH // 2,
    HEIGHT // 2,
    (54, 1, 63),
    (76, 2, 89),
    pygame.Vector2(WIDTH // 2, HEIGHT // 2),
    0.9,
    1,
)

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
#     15,
#     16,
#     34,
#     (128, 0, 0),
#     pygame.Vector2(WIDTH // 2, HEIGHT // 2),
# )

# player = Entity(
#     WIDTH // 2,
#     HEIGHT // 2,
#     [16, 16, 16, 16, 16, 16, 16, 16],
#     48,
#     (0, 0, 128),
#     pygame.Vector2(WIDTH // 2, HEIGHT // 2),
# )

player = Lizard(
    WIDTH // 2,
    HEIGHT // 2,
    [
        18,
        22,
        20,
        18,
        12,
        20,
        22,
        25,
        25,
        25,
        25,
        25,
        22,
        20,
        18,
        14,
        10,
        8,
        7,
        6,
        5,
        4,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
    ],
    10,
    (0, 128, 0),
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

    player.draw(screen)

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
