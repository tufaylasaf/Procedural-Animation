import pygame
import random
import math


class Entity:
    def __init__(
        self,
        sw,
        sh,
        radius,
        jointLength,
        color,
        position,
    ):
        self.sw = sw
        self.sh = sh

        # self.position = pygame.Vector2(random.uniform(0, sw), random.uniform(0, sh))
        self.position = position
        self.joints = [Joint(self.position.x, self.position.y, radius[0])]
        self.jointLength = jointLength
        for i in range(1, len(radius)):
            joint = Joint(
                self.position.x, self.position.y + (i * jointLength), radius[i]
            )
            self.joints.append(joint)

        self.color = color
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.radius = radius
        self.max_speed = 12
        self.acceleration_amount = 0.35
        self.friction = 0.1
        self.time = 0

    def update(self):
        self.velocity += self.acceleration

        self.time += 0.03  # Increment time
        self.a = 300

        # # Parametric equations for infinity shape (lemniscate of Bernoulli)
        # t = self.time
        # x = (
        #     self.a * math.cos(t) * math.sin(t) / (1 + math.sin(t) ** 2)
        # )  # Swap x and y calculations
        # y = self.a * math.cos(t) / (1 + math.sin(t) ** 2)

        # self.position = pygame.Vector2(x + self.sw, y + self.sh)

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.velocity *= 1 - self.friction

        self.position += self.velocity
        # self.wrap_around()
        self.joints[0].position = self.position

        self.apply_constraint()

        self.acceleration *= 0

    def apply_constraint(self):
        for i in range(1, len(self.joints)):
            prev = i - 1
            direction = self.joints[i].position - self.joints[prev].position
            direction.scale_to_length(self.jointLength)
            self.joints[i].position = direction + self.joints[prev].position

    def set_position(self, pos):
        self.joints[0].position = pos

    def apply_force(self, force):
        self.acceleration += force

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.apply_force(pygame.Vector2(-self.acceleration_amount, 0))
        if keys[pygame.K_RIGHT]:
            self.apply_force(pygame.Vector2(self.acceleration_amount, 0))
        if keys[pygame.K_UP]:
            self.apply_force(pygame.Vector2(0, -self.acceleration_amount))
        if keys[pygame.K_DOWN]:
            self.apply_force(pygame.Vector2(0, self.acceleration_amount))

    def draw(self, screen, skelteon=False, skin=True, outline=False):

        # Create a high-resolution surface
        scale_factor = (
            1  # This factor can be adjusted for performance and quality balance
        )
        high_res_surface = pygame.Surface(
            (screen.get_width() * scale_factor, screen.get_height() * scale_factor),
            pygame.SRCALPHA,
        )

        left = []
        right = []
        for i in range(0, len(self.joints)):
            if skelteon:
                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        int(self.joints[i].position.x),
                        int(self.joints[i].position.y),
                    ),
                    self.joints[i].radius,
                    3,
                )
            if i == len(self.joints) - 2:
                break
            a, b = self.joints[i].get_points(self.joints[i + 1])
            left.append(a * scale_factor)  # Scale points for high-res surface
            right.append(b * scale_factor)

        direction = self.joints[1].position - self.position
        direction = direction.normalize()
        head = (self.position - direction * self.radius[0]) * scale_factor

        direction = self.joints[-2].position - self.joints[-1].position
        direction = direction.normalize()
        tail = (self.joints[-2].position - direction * self.radius[-2]) * scale_factor

        leftmid, rightmid = self.joints[0].get_extra_points(self.joints[1])
        rightmidend, leftmidend = self.joints[-2].get_extra_points(self.joints[-1], -1)

        leftmid = leftmid * scale_factor
        rightmid = rightmid * scale_factor
        leftmidend = leftmidend * scale_factor
        rightmidend = rightmidend * scale_factor

        right.reverse()
        final = (
            [leftmid]
            + left
            + [leftmidend]
            + [tail]
            + [rightmidend]
            + right
            + [rightmid]
            + [head]
        )

        if outline:
            for point in final:
                pygame.draw.circle(
                    high_res_surface,
                    (255, 0, 0),
                    (point),
                    3,
                )

        if skin:
            pygame.draw.polygon(high_res_surface, self.color, final)
            pygame.draw.polygon(high_res_surface, (255, 255, 255), final, 2)

        # Scale down the high-resolution surface to the original screen size
        scaled_surface = pygame.transform.smoothscale(
            high_res_surface, screen.get_size()
        )
        screen.blit(scaled_surface, (0, 0))

    def wrap_around(self):
        wrap = False
        offset = 125
        if self.position.x > self.sw + offset:
            self.position.x = 0 - offset
            wrap = True
        elif self.position.x < -offset:
            self.position.x = self.sw + offset
            wrap = True
        if self.position.y > self.sh + offset:
            self.position.y = 0 - offset
            wrap = True
        elif self.position.y < -offset:
            self.position.y = self.sh + offset
            wrap = True

        if wrap:
            for i in range(1, len(self.joints)):
                self.joints[i].position = pygame.Vector2(
                    self.position.x, self.position.y + (i * self.jointLength)
                )
                wrap = False


class Joint:
    def __init__(self, x, y, radius):
        self.position = pygame.Vector2(x, y)
        self.radius = radius

    def get_points(self, next, offset=1):
        direction = next.position - self.position
        direction = direction.normalize()

        perp_left = pygame.Vector2(-direction.y, direction.x)
        perp_right = pygame.Vector2(direction.y, -direction.x)

        left_point = self.position + perp_left * (self.radius * offset)
        right_point = self.position + perp_right * (self.radius * offset)

        return left_point, right_point

    def get_extra_points(self, next, mult=1):
        direction = self.position - next.position
        direction = direction.normalize()

        perp_left = pygame.Vector2(-direction.y, direction.x)
        perp_right = pygame.Vector2(direction.y, -direction.x)

        leftmid = (
            self.position + ((direction - perp_left).normalize() * self.radius) * mult
        )
        rightmid = (
            self.position + ((direction - perp_right).normalize() * self.radius) * mult
        )

        return leftmid, rightmid
