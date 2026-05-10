import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

# Player IS-A CircleShape: reuse position, velocity, radius, collision, sprite plumbing;
# add ship-specific state and behavior only here (specialization).
class Player(CircleShape):
    def __init__(self, x, y):
        # super() runs CircleShape (then Sprite) setup so shared attributes exist first.
        super().__init__(x, y, PLAYER_RADIUS)
        # State only the player needs — not part of the generic circle contract.
        self.rotation = 0
        self.shoot_timer = 0

    def triangle(self):
        # Helper used by draw — encapsulation: callers use draw(); triangle() is detail.
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Override: polymorphism — main calls draw on all drawables; Player draws a polygon.
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        rotation_speed = PLAYER_TURN_SPEED * dt
        self.rotation += rotation_speed

    def update(self, dt):
        # Override: read input and update this object's state for one frame.
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        # Object creates another object: new Shot is its own instance with its own velocity.
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        shot.velocity = rotated_with_speed_vector

