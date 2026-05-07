import math
import unittest
from tests.helper import init_pygame
from src.config import WIN_WIDTH, WIN_HEIGHT, BALL_RADIUS, BALL_SPEED
from src.entities.ball import Ball
from src.entities.paddle import Paddle


init_pygame()


class TestBall(unittest.TestCase):
    def setUp(self):
        self.ball = Ball()

    def test_init_position(self):
        self.assertEqual(self.ball.x, WIN_WIDTH // 2)
        self.assertEqual(self.ball.y, WIN_HEIGHT // 2)
        self.assertEqual(self.ball.radius, BALL_RADIUS)
        self.assertTrue(self.ball.stuck)

    def test_init_velocity(self):
        speed = math.sqrt(self.ball.vx ** 2 + self.ball.vy ** 2)
        self.assertAlmostEqual(speed, BALL_SPEED, places=5)
        self.assertLess(self.ball.vy, 0)

    def test_launch(self):
        self.assertTrue(self.ball.stuck)
        self.ball.launch()
        self.assertFalse(self.ball.stuck)

    def test_launch_idempotent(self):
        self.ball.launch()
        self.ball.launch()
        self.assertFalse(self.ball.stuck)

    def test_follow_paddle(self):
        paddle = Paddle()
        paddle.x = 300
        self.ball.follow_paddle(paddle)
        self.assertEqual(self.ball.x, 360)
        self.assertEqual(self.ball.y, paddle.y - self.ball.radius)

    def test_update_stuck_does_nothing(self):
        x0, y0 = self.ball.x, self.ball.y
        self.ball.update(1)
        self.assertEqual(self.ball.x, x0)
        self.assertEqual(self.ball.y, y0)

    def test_update_moves_ball(self):
        self.ball.launch()
        x0, y0 = self.ball.x, self.ball.y
        self.ball.update(1)
        self.assertNotEqual((self.ball.x, self.ball.y), (x0, y0))

    def test_trail_grows(self):
        self.ball.launch()
        self.assertEqual(len(self.ball.trail), 0)
        self.ball.update(1)
        self.assertEqual(len(self.ball.trail), 1)

    def test_trail_max_size(self):
        self.ball.launch()
        for _ in range(20):
            self.ball.update(1)
        self.assertLessEqual(len(self.ball.trail), 10)

    def test_wall_bounce_left(self):
        self.ball.launch()
        self.ball.x = BALL_RADIUS
        self.ball.vx = -5
        self.ball.update(1)
        self.assertGreaterEqual(self.ball.x, BALL_RADIUS)
        self.assertGreater(self.ball.vx, 0)

    def test_wall_bounce_right(self):
        self.ball.launch()
        self.ball.x = WIN_WIDTH - BALL_RADIUS
        self.ball.vx = 5
        self.ball.update(1)
        self.assertLessEqual(self.ball.x, WIN_WIDTH - BALL_RADIUS)
        self.assertLess(self.ball.vx, 0)

    def test_wall_bounce_top(self):
        self.ball.launch()
        self.ball.y = BALL_RADIUS
        self.ball.vy = -5
        self.ball.update(1)
        self.assertGreaterEqual(self.ball.y, BALL_RADIUS)
        self.assertGreater(self.ball.vy, 0)

    def test_is_off_screen_false(self):
        self.ball.y = WIN_HEIGHT - 10
        self.assertFalse(self.ball.is_off_screen())

    def test_is_off_screen_true(self):
        self.ball.y = WIN_HEIGHT + 10
        self.assertTrue(self.ball.is_off_screen())

    def test_rect_property(self):
        r = self.ball.rect
        self.assertEqual(r.left, self.ball.x - self.ball.radius)
        self.assertEqual(r.top, self.ball.y - self.ball.radius)
        self.assertEqual(r.width, self.ball.radius * 2)
        self.assertEqual(r.height, self.ball.radius * 2)

    def test_cx_cy(self):
        self.assertEqual(self.ball.cx, self.ball.x)
        self.assertEqual(self.ball.cy, self.ball.y)


if __name__ == "__main__":
    unittest.main()
