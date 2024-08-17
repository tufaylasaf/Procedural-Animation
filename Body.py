import pygame
import random


class Body:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        self.position = pygame.Vector2(random.uniform(0, sw), random.uniform(0, sh))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4
        self.max_force = 0.1
        self.neighbors = []
        self.velocity.scale_to_length(self.max_speed)
        self.detection_radius = 90

        # Multipliers for each rule
        self.separation_multiplier = 1.2  # Separation has the highest priority
        self.alignment_multiplier = 0.85  # Alignment is next
        self.cohesion_multiplier = 1.0  # Cohesion has the lowest priority

    def update(self, boids):
        self.neighbors = self.get_neighbors(boids, self.detection_radius)
        self.acceleration += (
            self.separation(self.neighbors) * self.separation_multiplier
        )
        self.acceleration += self.alignment(self.neighbors) * self.alignment_multiplier
        self.acceleration += self.cohesion(self.neighbors) * self.cohesion_multiplier

        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

    def separation(self, neighbors):
        force = pygame.Vector2(0, 0)
        avg = pygame.Vector2(0, 0)
        for body in neighbors:
            distance = self.position.distance_to(body.position)
            difference = self.position - body.position
            if distance > 0:
                difference /= distance
            avg += difference
        if len(neighbors) > 0:
            avg /= len(neighbors)
            if avg.length() > 0:
                avg = avg.normalize() * self.max_speed
                force = avg - self.velocity
                if force.length() > self.max_force:
                    force.scale_to_length(self.max_force)
        return force

    def alignment(self, neighbors):
        force = pygame.Vector2(0, 0)
        avg = pygame.Vector2(0, 0)
        for boid in neighbors:
            avg += boid.velocity
        if len(neighbors) > 0:
            avg /= len(neighbors)
            avg = avg.normalize() * self.max_speed
            force = avg - self.velocity
            if force.length() > self.max_force:
                force.scale_to_length(self.max_force)
        return force

    def cohesion(self, neighbors):
        force = pygame.Vector2(0, 0)
        avg = pygame.Vector2(0, 0)
        for boid in neighbors:
            avg += boid.position
        if len(neighbors) > 0:
            avg /= len(neighbors)
            direction = avg - self.position
            direction = direction.normalize() * self.max_speed
            force = direction - self.velocity
            if force.length() > self.max_force:
                force.scale_to_length(self.max_force)
        return force

    def get_neighbors(self, boids, radius):
        neighbors = []
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < radius:
                neighbors.append(boid)
        return neighbors

    def wrap_around(self):
        offset = 10
        if self.position.x > self.sw + offset:
            self.position.x = 0 - offset
        elif self.position.x < -offset:
            self.position.x = self.sw + offset
        if self.position.y > self.sh + offset:
            self.position.y = 0 - offset
        elif self.position.y < -offset:
            self.position.y = self.sh + offset
