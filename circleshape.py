import pygame

# CircleShape: base class (generalization) for anything that is a circle on screen.
# Subclasses (Player, Asteroid, Shot) inherit shared state/behavior and override the parts
# that differ — classic inheritance + polymorphism.
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # pygame.sprite.Sprite expects optional *groups at construction. We pass
        # self.containers when subclasses set class attribute `containers` before
        # instances are created (see main.py). That wires each new object into the
        # right sprite Groups automatically — composition with pygame's group system.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        # Instance attributes: each object has its own position, velocity, radius.
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # Subclasses override this — same method name, different behavior (polymorphism).
        pass

    def update(self, dt):
        # Subclasses override with per-type simulation / input.
        pass

    def collides_with(self, other):
        # Shared behavior on the base class: any CircleShape can test overlap with another.
        # Callers use the object's public interface instead of duplicating distance math.
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)
