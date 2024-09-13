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
        self.draw_state = 0  # Initial state

    def draw(self, screen):
        # Toggle drawing based on state
        if self.draw_state == 0:
            super().draw(screen, skelteon=True, skin=False, outline=False)
        elif self.draw_state == 1:
            super().draw(screen, skelteon=True, skin=False, outline=True)
        elif self.draw_state == 2:
            super().draw(screen, skelteon=False, skin=True, outline=False)
        elif self.draw_state == 3:
            super().draw(screen, skelteon=False, skin=True, outline=False)
            self.eyes(screen)

    def eyes(self, screen):
        eye_radius = 6
        a, b = self.joints[0].get_points(self.joints[1], 0.65)
        pygame.draw.circle(screen, (255, 255, 255), a, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), b, eye_radius)

    def toggle_draw_state(self):
        self.draw_state = (self.draw_state + 1) % 4  # Cycle through states
