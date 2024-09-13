import pygame
from Entity import Entity


class Spider(Entity):
    def __init__(self, sw, sh, radius, jointLength, color, position):
        super().__init__(sw, sh, radius, jointLength, color, position)

    def update(self):
        self.velocity += self.acceleration

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.velocity *= 1 - self.friction

        for joint in self.joints:
            joint.position += self.velocity

        self.acceleration *= 0

    def draw(self, screen, skelteon=False, skin=True, outline=False):
        for i in range(0, len(self.joints) - 1):
            joint = self.joints[i]
            pygame.draw.circle(
                screen, (255, 255, 255), joint.position, joint.radius + 2
            )
        for i in range(0, len(self.joints) - 1):
            joint = self.joints[i]
            pygame.draw.circle(screen, self.color, joint.position, joint.radius)
