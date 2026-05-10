# MakeAsteroids

A small **Asteroids**-style game built with [Pygame](https://www.pygame.org/), structured to practice **object-oriented programming**: inheritance, polymorphism, encapsulation, and composing objects in a game loop.

The Python sources include **inline comments** that explain how each piece fits those ideas—start with `circleshape.py`, then the entity classes, then `main.py`.

## Requirements

- Python **3.13+** (see `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) (recommended) or another way to install dependencies from `pyproject.toml`

## Run

From the project root:

```bash
uv sync
uv run python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `W` / `S` | Thrust forward / backward |
| `A` / `D` | Rotate left / right |
| `Space` | Shoot |
| Close window | Quit |

## Project layout

| File | Role |
|------|------|
| `main.py` | Entry point: sprite groups, wiring `containers`, game loop |
| `circleshape.py` | Base class for circle-based entities + shared collision |
| `player.py` | Player ship: input, movement, shooting |
| `asteroid.py` | Asteroids: movement and splitting |
| `shot.py` | Projectiles |
| `asteroidfield.py` | Spawns asteroids at screen edges |
| `constants.py` | Tunable numbers (keeps class code focused on behavior) |
| `logger.py` | Optional JSONL logging of game state / events |

Runtime log files (`game_state.jsonl`, `game_events.jsonl`) are produced when logging runs; they are normal artifacts of play, not required for the game logic.

## OOP map (quick reference)

- **`CircleShape`** — common state (`position`, `velocity`, `radius`) and `collides_with`; subclasses override `draw` / `update`.
- **`Player`**, **`Asteroid`**, **`Shot`** — *is-a* `CircleShape`; each implements the same interface differently (polymorphism).
- **`AsteroidField`** — *is-a* `pygame.sprite.Sprite` with a different job (spawning), not a `CircleShape`.
- **`main.py`** — builds **groups** of objects and drives them each frame; sets class-level **`containers`** before constructing entities so Pygame registers them into the right groups.

For the full walkthrough, read the comments in the files above in that order.
