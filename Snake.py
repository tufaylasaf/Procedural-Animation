import pygame
import math
from Entity import Entity


class Snake(Entity):
    def __init__(self, sw, sh, radius, jointLength, jointCount, color, position):
        head = [radius, radius * 1.2]
        radius = [
            radius * (0.25 ** (i / (jointCount - 1))) for i in range(jointCount - 2)
        ]
        radius = head + radius
        super().__init__(sw, sh, radius, jointLength, color, position)

    def draw(self, screen):
        super().draw(screen, skelteon=False, skin=True, outline=False)
        self.eyes(screen)

    def eyes(self, screen):
        eye_radius = 5
        a, b = self.joints[0].get_points(self.joints[1], 0.65)
        pygame.draw.circle(screen, (255, 255, 255), a, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), b, eye_radius)
