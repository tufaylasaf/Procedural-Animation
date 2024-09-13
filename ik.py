import pygame
import pygame.gfxdraw
import sys
import math


LERP_FACTOR = 0.6


class DoubleJoint:
    def __init__(self, base, shoulder_length, elbow_length, is_upper=True):
        self.base = base
        self.shoulder_length = shoulder_length
        self.elbow_length = elbow_length
        self.is_upper = is_upper
        self.currentPos = base

        self.shoulder = base
        self.elbow = pygame.Vector2(self.shoulder.x + shoulder_length, self.shoulder.y)
        self.hand = pygame.Vector2(self.elbow.x + elbow_length, self.elbow.y)

    def update(self, base, lerpPos):
        self.shoulder = base

        total_distance = self.shoulder.distance_to(self.currentPos)

        if (
            self.hand.distance_to(self.shoulder)
            > self.shoulder_length + self.elbow_length
        ):
            self.currentPos = lerpPos

        total_arm_length = self.shoulder_length + self.elbow_length
        if total_distance > total_arm_length:
            direction = (self.currentPos - self.shoulder).normalize()
            self.currentPos = self.shoulder + direction * total_arm_length
            total_distance = total_arm_length

        a = self.shoulder_length
        b = self.elbow_length
        c = total_distance

        new_elbow = (
            self.ik_up(self.shoulder, self.currentPos, a, b, c)
            if self.is_upper
            else self.ik_down(self.shoulder, self.currentPos, a, b, c)
        )

        hand_direction = math.atan2(
            (
                -(self.currentPos.y - self.shoulder.y)
                if self.is_upper
                else self.currentPos.y - self.shoulder.y
            ),
            self.currentPos.x - self.shoulder.x,
        )

        hand_angle = hand_direction - math.acos((b**2 + c**2 - a**2) / (2 * b * c))

        new_hand = pygame.Vector2(
            new_elbow.x + self.elbow_length * math.cos(hand_angle),
            (
                new_elbow.y - self.elbow_length * math.sin(hand_angle)
                if self.is_upper
                else new_elbow.y + self.elbow_length * math.sin(hand_angle)
            ),
        )

        self.elbow = self.lerp(self.elbow, new_elbow, LERP_FACTOR)
        self.hand = self.lerp(self.hand, new_hand, LERP_FACTOR)

    def lerp(self, current, target, factor):
        """Linearly interpolate between current and target positions."""
        return current + (target - current) * factor

    def ik_up(self, a, b, A, B, C):
        theta = math.acos((B**2 + C**2 - A**2) / (2 * B * C))
        phi = math.atan2(-(b.y - a.y), b.x - a.x)

        return pygame.Vector2(
            a.x + B * math.cos(theta + phi), a.y - B * math.sin(theta + phi)
        )

    def ik_down(self, a, b, A, B, C):
        theta = math.acos((A**2 + C**2 - B**2) / (2 * A * C))
        phi = math.atan2(b.y - a.y, b.x - a.x)

        return pygame.Vector2(
            a.x + A * math.cos(theta + phi), a.y + A * math.sin(theta + phi)
        )

    def draw(self, screen, fill_color, outline_color=(255, 255, 255), outline_width=2):
        # Draw the outline (thicker and slightly offset for the outline effect)
        lineWidth = 10

        pygame.draw.line(
            screen,
            outline_color,
            self.shoulder,
            self.elbow,
            lineWidth + outline_width * 2,
        )
        pygame.draw.line(
            screen, outline_color, self.elbow, self.hand, lineWidth + outline_width * 2
        )

        # pygame.draw.circle(screen, outline_color, self.shoulder, 12 + outline_width)
        pygame.draw.circle(screen, outline_color, self.elbow, 5 + outline_width)
        pygame.draw.circle(screen, outline_color, self.hand, 7 + outline_width)

        # Draw the inner filled shape
        pygame.draw.line(screen, fill_color, self.shoulder, self.elbow, lineWidth)
        pygame.draw.line(screen, fill_color, self.elbow, self.hand, lineWidth)

        # pygame.draw.circle(screen, fill_color, self.shoulder, 12)
        pygame.draw.circle(screen, fill_color, self.elbow, 5)
        pygame.draw.circle(screen, fill_color, self.hand, 7)

    def rotate_vector(self, vec, angle):
        """Rotate a vector by a given angle in radians."""
        rotated_x = vec.x * math.cos(angle) - vec.y * math.sin(angle)
        rotated_y = vec.x * math.sin(angle) + vec.y * math.cos(angle)
        return pygame.Vector2(rotated_x, rotated_y)
