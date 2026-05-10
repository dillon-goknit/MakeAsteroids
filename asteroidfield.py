from typing import ClassVar

import pygame
import random
from asteroid import Asteroid
from constants import *

# AsteroidField IS-A pygame.sprite.Sprite but is not a CircleShape: its job is to own
# spawning logic (different responsibility = different class, same update-driven pattern).
class AsteroidField(pygame.sprite.Sprite):
    # Assigned in main.py before AsteroidField() (same containers pattern as CircleShape).
    containers: ClassVar[tuple[pygame.sprite.AbstractGroup, ...] | None] = None
    # Class attribute shared by all instances (here only one field exists — edge definitions).
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        groups = type(self).containers
        if groups is not None:
            pygame.sprite.Sprite.__init__(self, *groups)
        else:
            pygame.sprite.Sprite.__init__(self)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        # Factory-style: creates Asteroid instances; they register via Asteroid.containers.
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
