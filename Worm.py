import pygame
import math
from Entity import Entity


class Worm(Entity):
    def __init__(self, sw, sh, radius, jointLength, jointCount, color, position):
        head = [radius * 1.3]
        tail = [radius * 0.9, radius * 0.8, radius * 0.7, radius * 0.6, radius * 0.5]
        radius = [radius for i in range(1, jointCount - 6)]
        radius = head + radius + tail
        super().__init__(sw, sh, radius, jointLength, color, position)

    def draw(self, screen):
        super().draw(screen, skelteon=False, skin=True, outline=False)
        self.eyes(screen)
        self.body(screen)

    def body(self, screen):
        for i in range(2, len(self.radius) - 3):
            a, b = self.joints[i].get_points(self.joints[i + 1])
            pygame.draw.line(screen, (251, 217, 177), a, b, 6)

    def eyes(self, screen):
        eye_radius = 4
        a, b = self.joints[0].get_points(self.joints[1], 0.65)
        pygame.draw.circle(screen, (255, 255, 255), a, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), b, eye_radius)
