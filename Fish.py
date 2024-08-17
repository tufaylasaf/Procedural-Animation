import pygame
import math
from Entity import Entity


class Fish(Entity):
    def __init__(self, x, y, color, finColor, position, size=1.0, finSize=1.0):
        # Original radius values
        original_radius = [68, 81, 84, 83, 77, 64, 51, 38, 32, 19, 1]
        # Scale the radius values based on the size parameter
        scaled_radius = [num * 0.3 * size for num in original_radius]
        # Scale joint length based on the size parameter
        jointLength = 21 * size
        super().__init__(x, y, scaled_radius, jointLength, color, position)
        self.size = size
        self.finSize = finSize
        self.finColor = finColor

    def draw(self, screen):
        # Adjust fin sizes and positions according to the fish size
        self.fins(screen, 2, 64 * self.size, 25.6 * self.size, 45, 90)
        self.fins(screen, 8, 28 * self.size, 12 * self.size, 30, 50)
        super().draw(screen)
        self.eyes(screen)
        self.dorsal_fin(screen)

    def eyes(self, screen):
        # Scale eye size based on fish size
        eye_radius = 5 * self.size
        a, b = self.joints[0].get_points(self.joints[1], 0.65)
        pygame.draw.circle(screen, (255, 255, 255), a, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), b, eye_radius)

    def fins(self, screen, joint, width, height, rotOffset, posOffset):
        # Calculate direction vector between joint 2 and joint 1
        direction = self.joints[joint].position - self.joints[joint - 1].position
        angle = math.degrees(math.atan2(-direction.y, direction.x))

        # Scale the fin sizes based on fish size
        fin_width = width * self.finSize
        fin_height = height * self.finSize

        # Create the fin surfaces
        fin_surface = pygame.Surface((fin_width, fin_height), pygame.SRCALPHA)
        outline_surface = pygame.Surface(
            (fin_width + 4, fin_height + 4), pygame.SRCALPHA
        )

        # Draw the outline
        pygame.draw.ellipse(
            outline_surface, (255, 255, 255), outline_surface.get_rect()
        )

        # Draw the filled fin with a lighter purple color
        pygame.draw.ellipse(fin_surface, self.finColor, fin_surface.get_rect())

        # Blit the filled fin onto the outline surface to create the outline effect
        outline_surface.blit(fin_surface, (2, 2))

        # Calculate the offset for placing the fins correctly
        offset = direction.normalize() * self.jointLength

        # Left fin
        left_fin_position = self.joints[joint].position - offset.rotate(
            -posOffset * self.finSize
        )
        rotated_left_fin = pygame.transform.rotate(outline_surface, angle - rotOffset)
        rotated_left_fin_rect = rotated_left_fin.get_rect(center=left_fin_position)
        screen.blit(rotated_left_fin, rotated_left_fin_rect.topleft)

        # Calculate the angle for the right fin
        angle = math.degrees(math.atan2(direction.y, direction.x))

        # Right fin
        right_fin_position = self.joints[joint].position - offset.rotate(
            posOffset * self.finSize
        )
        rotated_right_fin = pygame.transform.rotate(outline_surface, -angle + rotOffset)
        rotated_right_fin_rect = rotated_right_fin.get_rect(center=right_fin_position)
        screen.blit(rotated_right_fin, rotated_right_fin_rect.topleft)

    def dorsal_fin(self, screen):
        # Calculate the positions for the dorsal fin
        j = self.joints
        a, b = j[4].position, j[5].position
        c, d = j[6].position, j[7].position

        # Create a list of points for the dorsal fin
        dorsal_points = [a, b, c, d]

        # Draw the dorsal fin using bezier curve approximation
        pygame.draw.polygon(screen, self.finColor, dorsal_points)
        pygame.draw.polygon(screen, (255, 255, 255), dorsal_points, 1)
