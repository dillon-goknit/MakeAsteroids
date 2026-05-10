import pygame
from circleshape import CircleShape
from constants import  SHOT_RADIUS, LINE_WIDTH

# Shot IS-A CircleShape: small radius, simple motion; same collides_with / groups as others.
class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        # Override: straight-line movement using velocity set by Player.shoot.
        self.position += self.velocity * dt
