import math
import unittest
from tests.helper import init_pygame
from src.config import BALL_SPEED, WIN_WIDTH, WIN_HEIGHT
from src.entities.ball import Ball
from src.entities.paddle import Paddle
from src.entities.brick import Brick
from src.systems.physics import PhysicsSystem


init_pygame()


class TestPhysicsSystem(unittest.TestCase):
    def setUp(self):
        self.physics = PhysicsSystem()

    def test_paddle_bounce_no_collision(self):
        ball = Ball()
        ball.launch()
        paddle = Paddle()
        paddle.x = 1000
        result = self.physics.paddle_bounce(ball, paddle)
        self.assertFalse(result)

    def test_paddle_bounce_hit(self):
        ball = Ball()
        ball.launch()
        ball.x = 400
        ball.y = 550
        paddle = Paddle()
        paddle.x = 340
        paddle.y = 550
        result = self.physics.paddle_bounce(ball, paddle)
        self.assertTrue(result)
        self.assertLess(ball.vy, 0)

    def test_paddle_bounce_center_goes_up(self):
        ball = Ball()
        ball.launch()
        ball.x = 400
        ball.y = 550
        ball.vx = 0
        ball.vy = 5
        paddle = Paddle()
        paddle.x = 340
        paddle.y = 550
        self.physics.paddle_bounce(ball, paddle)
        self.assertAlmostEqual(ball.vx, 0, places=1)
        self.assertLess(ball.vy, 0)

    def test_paddle_bounce_left_goes_left(self):
        ball = Ball()
        ball.launch()
        ball.x = 350
        ball.y = 550
        paddle = Paddle()
        paddle.x = 340
        paddle.y = 550
        self.physics.paddle_bounce(ball, paddle)
        self.assertLess(ball.vx, 0)

    def test_paddle_bounce_right_goes_right(self):
        ball = Ball()
        ball.launch()
        ball.x = 450
        ball.y = 550
        paddle = Paddle()
        paddle.x = 340
        paddle.y = 550
        self.physics.paddle_bounce(ball, paddle)
        self.assertGreater(ball.vx, 0)

    def test_paddle_bounce_sets_y_above_paddle(self):
        ball = Ball()
        ball.launch()
        ball.x = 400
        ball.y = 555
        paddle = Paddle()
        paddle.x = 340
        paddle.y = 555
        self.physics.paddle_bounce(ball, paddle)
        self.assertLess(ball.y, paddle.y)

    def test_ball_rect_bounce_no_collision(self):
        ball = Ball()
        ball.launch()
        brick = Brick(1000, 1000, 1)
        result = self.physics.bounce_ball_rect(ball, brick.rect)
        self.assertFalse(result)

    def test_ball_rect_bounce_hit(self):
        ball = Ball()
        ball.launch()
        ball.x = 400
        ball.y = 100
        ball.vx = 0
        ball.vy = 5
        brick = Brick(365, 90, 1)
        result = self.physics.bounce_ball_rect(ball, brick.rect)
        self.assertTrue(result)

    def test_ball_rect_bounce_from_below(self):
        ball = Ball()
        ball.launch()
        ball.x = 400
        ball.y = 130
        ball.vx = 0
        ball.vy = -5
        brick = Brick(365, 100, 1)
        result = self.physics.bounce_ball_rect(ball, brick.rect)
        self.assertTrue(result)

    def test_update_ball_speed(self):
        ball = Ball()
        ball.launch()
        orig_speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
        self.physics.update_ball_speed(ball, 2.0)
        new_speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
        self.assertAlmostEqual(new_speed, min(15, orig_speed * 2), places=4)

    def test_update_ball_speed_clamp_min(self):
        ball = Ball()
        ball.launch()
        self.physics.update_ball_speed(ball, 0.01)
        speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
        self.assertGreaterEqual(speed, 2)

    def test_update_ball_speed_clamp_max(self):
        ball = Ball()
        ball.launch()
        self.physics.update_ball_speed(ball, 100)
        speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
        self.assertAlmostEqual(speed, 15, places=4)

    def test_update_ball_speed_zero_velocity(self):
        ball = Ball()
        ball.launch()
        ball.vx = 0
        ball.vy = 0
        self.physics.update_ball_speed(ball, 2)
        self.assertEqual(ball.vx, 0)
        self.assertEqual(ball.vy, 0)


if __name__ == "__main__":
    unittest.main()
