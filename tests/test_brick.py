import unittest
from tests.helper import init_pygame
from src.config import BRICK_TYPES, BRICK_WIDTH, BRICK_HEIGHT
from src.entities.brick import Brick


init_pygame()


class TestBrick(unittest.TestCase):
    def test_init_type_1(self):
        b = Brick(10, 20, 1)
        self.assertEqual(b.x, 10)
        self.assertEqual(b.y, 20)
        self.assertEqual(b.w, BRICK_WIDTH)
        self.assertEqual(b.h, BRICK_HEIGHT)
        self.assertEqual(b.hp, 1)
        self.assertEqual(b.max_hp, 1)
        self.assertEqual(b.score, 10)
        self.assertTrue(b.alive)

    def test_init_type_4(self):
        b = Brick(0, 0, 4)
        self.assertEqual(b.hp, 2)
        self.assertEqual(b.score, 40)

    def test_init_type_5(self):
        b = Brick(0, 0, 5)
        self.assertEqual(b.hp, 3)
        self.assertEqual(b.score, 50)

    def test_hit_destroys_type_1(self):
        b = Brick(0, 0, 1)
        destroyed = b.hit()
        self.assertTrue(destroyed)
        self.assertFalse(b.alive)

    def test_hit_reduces_hp(self):
        b = Brick(0, 0, 4)
        self.assertEqual(b.hp, 2)
        destroyed = b.hit()
        self.assertFalse(destroyed)
        self.assertEqual(b.hp, 1)
        self.assertTrue(b.alive)

    def test_hit_twice_destroys_type_4(self):
        b = Brick(0, 0, 4)
        b.hit()
        destroyed = b.hit()
        self.assertTrue(destroyed)
        self.assertFalse(b.alive)

    def test_hit_sets_timer(self):
        b = Brick(0, 0, 1)
        self.assertEqual(b.hit_timer, 0)
        b.hit()
        self.assertEqual(b.hit_timer, 8)

    def test_update_timer(self):
        b = Brick(0, 0, 1)
        b.hit()
        self.assertEqual(b.hit_timer, 8)
        b.update()
        self.assertEqual(b.hit_timer, 7)

    def test_dead_brick_stays_dead(self):
        b = Brick(0, 0, 1)
        b.hit()
        self.assertFalse(b.alive)
        b.hit()
        self.assertFalse(b.alive)

    def test_rect(self):
        b = Brick(15, 25, 1)
        r = b.rect
        self.assertEqual(r.x, 15)
        self.assertEqual(r.y, 25)
        self.assertEqual(r.w, BRICK_WIDTH)
        self.assertEqual(r.h, BRICK_HEIGHT)

    def test_type_1_color(self):
        b = Brick(0, 0, 1)
        expected = BRICK_TYPES[1]["color"]
        self.assertEqual(b.color, expected)

    def test_all_types_exist(self):
        for t in range(1, 6):
            b = Brick(0, 0, t)
            info = BRICK_TYPES[t]
            self.assertEqual(b.color, info["color"])
            self.assertEqual(b.hp, info["hp"])
            self.assertEqual(b.score, info["score"])
        b = Brick(0, 0, 6)
        self.assertTrue(b.wall)
        self.assertEqual(b.hp, 999)
        self.assertEqual(b.score, 0)

    def test_wall_indestructible(self):
        b = Brick(0, 0, 6)
        for _ in range(100):
            destroyed = b.hit()
            self.assertFalse(destroyed)
        self.assertTrue(b.alive)


if __name__ == "__main__":
    unittest.main()
