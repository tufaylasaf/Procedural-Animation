from Entity import Entity
import pygame
from ik import DoubleJoint
import math


class Lizard(Entity):
    def __init__(self, sw, sh, radius, jointLength, color, position):
        super().__init__(sw, sh, radius, jointLength, color, position)
        base_arm_l, base_arm_r = self.joints[6].get_points(self.joints[7])
        base_leg_l, base_leg_r = self.joints[18].get_points(self.joints[19])
        self.arms = [
            DoubleJoint(base_arm_l, pygame.Vector2(-20, 0), 23, 23, True),
            DoubleJoint(base_arm_r, pygame.Vector2(20, 0), 23, 23, False),
        ]
        self.legs = [
            DoubleJoint(base_leg_l, pygame.Vector2(-20, 0), 25, 25, False),
            DoubleJoint(base_leg_r, pygame.Vector2(20, 0), 25, 25, True),
        ]
        self.target_pos = [
            base_arm_l + pygame.Vector2(-20, 0),
            base_arm_r + pygame.Vector2(20, 0),
            base_leg_l + pygame.Vector2(-20, 0),
            base_leg_r + pygame.Vector2(20, 0),
        ]

    def update(self):
        super().update()
        base_arm_l, base_arm_r = self.joints[6].get_points(self.joints[7])
        base_leg_l, base_leg_r = self.joints[13].get_points(self.joints[14])

        dir_arm = self.joints[6].position - self.joints[7].position
        angle_arm = math.atan2(dir_arm.y, dir_arm.x)
        dir_leg = self.joints[13].position - self.joints[14].position
        angle_leg = math.atan2(dir_leg.y, dir_leg.x)

        self.target_pos = [
            base_arm_l + self.rotate_vector(pygame.Vector2(-25, 0), angle_arm - 67.5),
            base_arm_r + self.rotate_vector(pygame.Vector2(25, 0), angle_arm - 67.5),
            base_leg_l + self.rotate_vector(pygame.Vector2(-0, 0), angle_leg - 67.5),
            base_leg_r + self.rotate_vector(pygame.Vector2(0, 0), angle_leg - 67.5),
        ]

        self.arms[0].update(
            base_arm_l + self.rotate_vector(pygame.Vector2(7, 0), angle_arm - 67.5),
            self.target_pos[0]
            + self.rotate_vector(pygame.Vector2(0, -32.5), angle_arm - 67.5),
        )
        self.arms[1].update(
            base_arm_r + self.rotate_vector(pygame.Vector2(-7, 0), angle_arm - 67.5),
            self.target_pos[1]
            + self.rotate_vector(pygame.Vector2(0, -32.5), angle_arm - 67.5),
        )
        self.legs[0].update(
            base_leg_l + self.rotate_vector(pygame.Vector2(7, 0), angle_leg - 67.5),
            self.target_pos[2]
            + self.rotate_vector(pygame.Vector2(0, -12), angle_leg - 67.5),
        )
        self.legs[1].update(
            base_leg_r + self.rotate_vector(pygame.Vector2(-7, 0), angle_leg - 67.5),
            self.target_pos[3]
            + self.rotate_vector(pygame.Vector2(0, -12), angle_leg - 67.5),
        )

    def draw(self, screen, skelteon=False, skin=True, outline=False):
        for arm in self.arms:
            arm.draw(screen, self.color)
        for leg in self.legs:
            leg.draw(screen, self.color)
        super().draw(screen, skelteon, skin, outline)
        self.eyes(screen)
        # for target in self.target_pos:
        #     pygame.draw.circle(screen, (255, 0, 0), target, 6)

    def eyes(self, screen):
        eye_radius = 5
        a, b = self.joints[0].get_points(self.joints[1], 0.65)
        pygame.draw.circle(screen, (255, 255, 255), a, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), b, eye_radius)

    def rotate_vector(self, vec, angle):
        """Rotate a vector by a given angle in radians."""
        rotated_x = vec.x * math.cos(angle) - vec.y * math.sin(angle)
        rotated_y = vec.x * math.sin(angle) + vec.y * math.cos(angle)
        return pygame.Vector2(rotated_x, rotated_y)
