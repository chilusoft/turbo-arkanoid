import unittest
from tests.helper import init_pygame
from src.config import POWERUP_TYPES, POWERUP_SIZE, POWERUP_SPEED, WIN_HEIGHT
from src.entities.powerup import PowerUp


init_pygame()


class TestPowerUp(unittest.TestCase):
    def test_init(self):
        pw = PowerUp(100, 200, "expand")
        self.assertEqual(pw.x, 100)
        self.assertEqual(pw.y, 200)
        self.assertEqual(pw.size, POWERUP_SIZE)
        self.assertEqual(pw.ptype, "expand")
        self.assertTrue(pw.alive)

    def test_init_all_types(self):
        for t in POWERUP_TYPES:
            pw = PowerUp(0, 0, t)
            self.assertEqual(pw.ptype, t)
            self.assertEqual(pw.color, POWERUP_TYPES[t]["color"])

    def test_rect(self):
        pw = PowerUp(10, 20, "laser")
        r = pw.rect
        self.assertEqual(r.x, 10)
        self.assertEqual(r.y, 20)
        self.assertEqual(r.w, POWERUP_SIZE)
        self.assertEqual(r.h, POWERUP_SIZE)

    def test_update_moves_down(self):
        pw = PowerUp(100, 0, "life")
        pw.update(1)
        self.assertEqual(pw.y, POWERUP_SPEED)

    def test_update_increments_bob(self):
        pw = PowerUp(100, 0, "life")
        self.assertEqual(pw.bob_offset, 0)
        pw.update(1)
        self.assertEqual(pw.bob_offset, 0.05)

    def test_is_off_screen_false(self):
        pw = PowerUp(100, WIN_HEIGHT - 10, "multi")
        self.assertFalse(pw.is_off_screen())

    def test_is_off_screen_true(self):
        pw = PowerUp(100, WIN_HEIGHT + 1, "multi")
        self.assertTrue(pw.is_off_screen())

    def test_duration_laser(self):
        pw = PowerUp(0, 0, "laser")
        self.assertEqual(pw.info["duration"], 8000)

    def test_duration_life(self):
        pw = PowerUp(0, 0, "life")
        self.assertEqual(pw.info["duration"], 0)


if __name__ == "__main__":
    unittest.main()
