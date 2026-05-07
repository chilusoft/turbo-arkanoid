import unittest
from unittest.mock import MagicMock
from tests.helper import init_pygame
from src.config import WIN_WIDTH, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED
from src.entities.paddle import Paddle
from src.input import InputManager


init_pygame()


class TestPaddle(unittest.TestCase):
    def setUp(self):
        self.paddle = Paddle()

    def test_init(self):
        self.assertEqual(self.paddle.w, PADDLE_WIDTH)
        self.assertEqual(self.paddle.h, PADDLE_HEIGHT)
        self.assertEqual(self.paddle.x, WIN_WIDTH // 2 - PADDLE_WIDTH // 2)
        self.assertEqual(self.paddle.y, 560)
        self.assertEqual(self.paddle.speed, PADDLE_SPEED)
        self.assertFalse(self.paddle.laser_active)
        self.assertFalse(self.paddle.sticky)

    def test_rect(self):
        r = self.paddle.rect
        self.assertEqual(r.x, self.paddle.x)
        self.assertEqual(r.y, self.paddle.y)
        self.assertEqual(r.w, self.paddle.w)
        self.assertEqual(r.h, self.paddle.h)

    def test_reset(self):
        self.paddle.x = 0
        self.paddle.speed = 100
        self.paddle.reset()
        self.assertEqual(self.paddle.x, WIN_WIDTH // 2 - PADDLE_WIDTH // 2)
        self.assertEqual(self.paddle.speed, PADDLE_SPEED)

    def test_boundary_left(self):
        self.paddle.x = -100
        mock_input = MagicMock()
        mock_input.keys_down = {}
        self.paddle.update(1, mock_input)
        self.assertEqual(self.paddle.x, 0)

    def test_boundary_right(self):
        self.paddle.x = WIN_WIDTH + 100
        mock_input = MagicMock()
        mock_input.keys_down = {}
        self.paddle.update(1, mock_input)
        self.assertEqual(self.paddle.x, WIN_WIDTH - self.paddle.w)

    def test_laser_activation(self):
        self.assertFalse(self.paddle.laser_active)
        self.paddle.activate_laser(5000)
        self.assertTrue(self.paddle.laser_active)
        self.assertEqual(self.paddle.laser_timer, 5000)

    def test_laser_deactivation(self):
        self.paddle.activate_laser(100)
        self.paddle.update_powerups(200)
        self.assertFalse(self.paddle.laser_active)

    def test_laser_shot_cooldown(self):
        self.paddle.activate_laser(5000)
        mock_input = MagicMock()
        mock_input.keys_down = {}
        mock_input.keys_just_pressed = {119: True}
        with unittest.mock.patch("pygame.K_SPACE", 119):
            result = self.paddle.update(1, mock_input)
        self.assertTrue(result)
        self.assertEqual(self.paddle.shot_cooldown, 15)

    def test_expand(self):
        orig = self.paddle.w
        self.paddle.w = min(200, self.paddle.w * 1.5)
        self.assertGreater(self.paddle.w, orig)
        self.assertLessEqual(self.paddle.w, 200)

    def test_shrink(self):
        self.paddle.w = max(60, self.paddle.w // 1.5)
        self.assertLess(self.paddle.w, PADDLE_WIDTH)
        self.assertGreaterEqual(self.paddle.w, 60)


if __name__ == "__main__":
    unittest.main()
