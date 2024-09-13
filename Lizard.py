from Entity import Entity
import pygame
from ik import DoubleJoint
import math


class Lizard(Entity):
    def __init__(self, sw, sh, radius, jointLength, color, position):
        super().__init__(sw, sh, radius, jointLength, color, position)
        base_arm_l, base_arm_r = self.joints[6].get_points(self.joints[7])
        base_leg_l, base_leg_r = self.joints[18].get_points(self.joints[19])

        self.arms = self.create_limbs(base_arm_l, base_arm_r, 23, 23, True)
        self.legs = self.create_limbs(base_leg_l, base_leg_r, 25, 25, False)

    def update(self):
        super().update()
        base_arm_l, base_arm_r = self.joints[6].get_points(self.joints[7])
        base_leg_l, base_leg_r = self.joints[13].get_points(self.joints[14])

        dir_arm = self.joints[6].position - self.joints[7].position
        angle_arm = math.atan2(dir_arm.y, dir_arm.x)
        dir_leg = self.joints[13].position - self.joints[14].position
        angle_leg = math.atan2(dir_leg.y, dir_leg.x)

        self.target_pos = [
            base_arm_l
            + self.rotate_vector(pygame.Vector2(-25, -32.5), angle_arm - 67.5),
            base_arm_r
            + self.rotate_vector(pygame.Vector2(25, -32.5), angle_arm - 67.5),
            base_leg_l + self.rotate_vector(pygame.Vector2(-0, -12), angle_leg - 67.5),
            base_leg_r + self.rotate_vector(pygame.Vector2(0, -12), angle_leg - 67.5),
        ]

        self.update_limbs(
            self.arms,
            base_arm_l,
            base_arm_r,
            pygame.Vector2(7, 0),
            25,
            -32.5,
            angle_arm,
        )
        self.update_limbs(
            self.legs, base_leg_l, base_leg_r, pygame.Vector2(7, 0), 0, -12, angle_leg
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

    def create_limbs(self, base_r, base_l, shoulder_length, elbow_length, switch):
        return [
            DoubleJoint(
                base_l, shoulder_length, elbow_length, True if switch else False
            ),
            DoubleJoint(
                base_r, shoulder_length, elbow_length, False if switch else True
            ),
        ]

    def update_limbs(
        self, limbs, base_l, base_r, base_offset, target_offset, lerp_offset, angle
    ):
        targetPos = base_l + self.rotate_vector(
            pygame.Vector2(-target_offset, lerp_offset), angle - 67.5
        )
        limbs[0].update(
            base_l + self.rotate_vector(base_offset, angle - 67.5), targetPos
        )
        targetPos = base_r + self.rotate_vector(
            pygame.Vector2(target_offset, lerp_offset), angle - 67.5
        )
        limbs[1].update(
            base_r - self.rotate_vector(base_offset, angle - 67.5), targetPos
        )

    def rotate_vector(self, vec, angle):
        """Rotate a vector by a given angle in radians."""
        rotated_x = vec.x * math.cos(angle) - vec.y * math.sin(angle)
        rotated_y = vec.x * math.sin(angle) + vec.y * math.cos(angle)
        return pygame.Vector2(rotated_x, rotated_y)
