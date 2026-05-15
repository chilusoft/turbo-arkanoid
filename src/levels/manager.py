from ..config import BRICK_TYPES
from ..entities.brick import Brick
from .data import LEVELS


class LevelManager:
    def __init__(self):
        self.current_level = 0
        self.bricks = []
        self.total_levels = len(LEVELS)

    def load_level(self, index):
        self.current_level = index % self.total_levels
        data = LEVELS[self.current_level]
        self.bricks = [Brick(b["x"], b["y"], b["type"]) for b in data["bricks"]]
        return data["name"]

    def load_next(self):
        return self.load_level(self.current_level + 1)

    def restart(self):
        return self.load_level(self.current_level)

    @property
    def level_name(self):
        return LEVELS[self.current_level]["name"]

    @property
    def active_bricks(self):
        return [b for b in self.bricks if b.alive]

    @property
    def cleared(self):
        return len([b for b in self.bricks if b.alive and not b.wall]) == 0

    def get_brick_score(self, brick):
        info = BRICK_TYPES.get(brick.type, BRICK_TYPES[1])
        return info["score"]

    @property
    def total_bricks(self):
        return len([b for b in self.bricks if b.alive])
