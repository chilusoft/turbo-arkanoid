import unittest
from tests.helper import init_pygame
from src.levels.manager import LevelManager
from src.levels.data import LEVELS


init_pygame()


class TestLevelManager(unittest.TestCase):
    def setUp(self):
        self.mgr = LevelManager()

    def test_init(self):
        self.assertEqual(self.mgr.current_level, 0)
        self.assertEqual(len(self.mgr.bricks), 0)
        self.assertEqual(self.mgr.total_levels, len(LEVELS))

    def test_load_level_0(self):
        name = self.mgr.load_level(0)
        self.assertEqual(name, LEVELS[0]["name"])
        self.assertEqual(self.mgr.current_level, 0)
        self.assertGreater(len(self.mgr.bricks), 0)

    def test_load_level_wraparound(self):
        name = self.mgr.load_level(999)
        expected = LEVELS[999 % self.mgr.total_levels]["name"]
        self.assertEqual(name, expected)

    def test_load_next(self):
        self.mgr.load_level(0)
        name = self.mgr.load_next()
        self.assertEqual(self.mgr.current_level, 1)
        self.assertEqual(name, LEVELS[1]["name"])

    def test_restart(self):
        self.mgr.load_level(2)
        name = self.mgr.restart()
        self.assertEqual(self.mgr.current_level, 2)
        self.assertEqual(name, LEVELS[2]["name"])

    def test_level_name(self):
        self.mgr.load_level(0)
        self.assertEqual(self.mgr.level_name, LEVELS[0]["name"])

    def test_active_bricks_all_alive(self):
        self.mgr.load_level(0)
        self.assertEqual(len(self.mgr.active_bricks), len(self.mgr.bricks))

    def test_active_bricks_some_destroyed(self):
        self.mgr.load_level(0)
        self.mgr.bricks[0].alive = False
        self.assertEqual(len(self.mgr.active_bricks), len(self.mgr.bricks) - 1)

    def test_cleared_false(self):
        self.mgr.load_level(0)
        self.assertFalse(self.mgr.cleared)

    def test_cleared_true(self):
        self.mgr.load_level(0)
        for b in self.mgr.bricks:
            b.alive = False
        self.assertTrue(self.mgr.cleared)

    def test_get_brick_score(self):
        self.mgr.load_level(0)
        brick = self.mgr.bricks[0]
        score = self.mgr.get_brick_score(brick)
        from src.config import BRICK_TYPES
        self.assertEqual(score, BRICK_TYPES[brick.type]["score"])

    def test_total_bricks(self):
        self.mgr.load_level(0)
        alive = len([b for b in self.mgr.bricks if b.alive])
        self.assertEqual(self.mgr.total_bricks, alive)

    def test_all_levels_have_names(self):
        for i, level in enumerate(LEVELS):
            self.assertIn("name", level, f"Level {i} missing name")
            self.assertIsInstance(level["name"], str)
            self.assertGreater(len(level["name"]), 0)

    def test_all_levels_have_bricks(self):
        for i, level in enumerate(LEVELS):
            self.assertIn("bricks", level, f"Level {i} missing bricks")
            self.assertGreater(len(level["bricks"]), 0, f"Level {i} has no bricks")

    def test_all_bricks_have_required_fields(self):
        for i, level in enumerate(LEVELS):
            for j, brick in enumerate(level["bricks"]):
                for field in ("x", "y", "type"):
                    self.assertIn(field, brick, f"Level {i} brick {j} missing '{field}'")
                self.assertIn(brick["type"], range(1, 6),
                              f"Level {i} brick {j} invalid type {brick['type']}")

    def test_bricks_within_bounds(self):
        from src.config import WIN_WIDTH, WIN_HEIGHT
        for i, level in enumerate(LEVELS):
            for j, brick in enumerate(level["bricks"]):
                self.assertGreaterEqual(brick["x"], 0, f"Level {i} brick {j} x < 0")
                self.assertLess(brick["x"], WIN_WIDTH, f"Level {i} brick {j} x > width")
                self.assertGreaterEqual(brick["y"], 0, f"Level {i} brick {j} y < 0")
                self.assertLess(brick["y"], WIN_HEIGHT,
                                f"Level {i} brick {j} y off screen")


if __name__ == "__main__":
    unittest.main()
