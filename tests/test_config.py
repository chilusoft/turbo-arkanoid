import unittest
from tests.helper import init_pygame
from src.config import (
    WIN_WIDTH, WIN_HEIGHT, FPS, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED,
    BALL_RADIUS, BALL_SPEED, BRICK_WIDTH, BRICK_HEIGHT, BRICK_TYPES,
    POWERUP_TYPES, POWERUP_SIZE, POWERUP_SPEED, POWERUP_CHANCE,
    INITIAL_LIVES, MAX_LIVES, PARTICLE_MAX_AGE, MAX_PARTICLES,
)


init_pygame()


class TestConfig(unittest.TestCase):
    def test_dimensions_positive(self):
        self.assertGreater(WIN_WIDTH, 0)
        self.assertGreater(WIN_HEIGHT, 0)

    def test_fps_positive(self):
        self.assertGreater(FPS, 0)

    def test_paddle_dimensions(self):
        self.assertGreater(PADDLE_WIDTH, 0)
        self.assertGreater(PADDLE_HEIGHT, 0)
        self.assertGreater(PADDLE_SPEED, 0)

    def test_ball(self):
        self.assertGreater(BALL_RADIUS, 0)
        self.assertGreater(BALL_SPEED, 0)

    def test_brick_dimensions(self):
        self.assertGreater(BRICK_WIDTH, 0)
        self.assertGreater(BRICK_HEIGHT, 0)

    def test_brick_types_have_all_keys(self):
        for tid, info in BRICK_TYPES.items():
            for key in ("color", "hp", "score", "glow"):
                self.assertIn(key, info, f"Brick type {tid} missing '{key}'")
            self.assertGreater(info["hp"], 0)
            self.assertGreaterEqual(info["score"], 0)

    def test_powerup_types_have_all_keys(self):
        for pid, info in POWERUP_TYPES.items():
            for key in ("color", "duration", "desc"):
                self.assertIn(key, info, f"PowerUp '{pid}' missing '{key}'")

    def test_powerup_size_speed(self):
        self.assertGreater(POWERUP_SIZE, 0)
        self.assertGreater(POWERUP_SPEED, 0)

    def test_powerup_chance_range(self):
        self.assertGreaterEqual(POWERUP_CHANCE, 0)
        self.assertLessEqual(POWERUP_CHANCE, 1)

    def test_lives(self):
        self.assertGreater(INITIAL_LIVES, 0)
        self.assertGreater(MAX_LIVES, 0)
        self.assertLessEqual(INITIAL_LIVES, MAX_LIVES)

    def test_particles(self):
        self.assertGreater(PARTICLE_MAX_AGE, 0)
        self.assertGreater(MAX_PARTICLES, 0)


if __name__ == "__main__":
    unittest.main()
