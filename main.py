import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from sys import exit
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    # Sprite Groups hold references to many objects — composition of the live object graph.
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Class-level .containers must be set BEFORE constructing instances: each constructor
    # reads the subclass's containers tuple and auto-adds the new object to those Groups.
    AsteroidField.containers = (updatable,)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    # These lines run constructors → each object registers itself into the right groups.
    asteroidfield = AsteroidField()
    player = Player(x, y)
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        # Polymorphism: every sprite in updatable implements update(dt) its own way.
        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                exit()

        # Polymorphism: every drawable implements draw(screen) its own way.
        for obj in drawable:
            obj.draw(screen)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

if __name__ == "__main__":
    main()
