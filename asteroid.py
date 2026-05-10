import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS
from logger import log_event

# Asteroid IS-A CircleShape: same base collision/drawing contract, different rules + split().
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # Behavior specific to asteroids — lives here, not on CircleShape or Shot.
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20,50)
        new_velocity1 = self.velocity.rotate(angle)
        new_velocity2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = new_velocity1*1.2
        asteroid2.velocity = new_velocity2*1.2

