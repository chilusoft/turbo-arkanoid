import pygame
from ..config import (
    BRICK_TYPES, BRICK_WIDTH, BRICK_HEIGHT,
    NEON_RED, NEON_ORANGE, NEON_YELLOW, NEON_GREEN, NEON_PURPLE,
)


BRICK_ORDER = [1, 2, 3, 4, 5]
_GLOW_CACHE = {}


def _make_glow_surf(glow_color):
    surf = pygame.Surface((BRICK_WIDTH + 12, BRICK_HEIGHT + 12), pygame.SRCALPHA)
    for r in range(6, 0, -1):
        a = max(0, 25 - r * 3)
        pygame.draw.rect(
            surf, (*glow_color, a),
            (6 - r, 6 - r, BRICK_WIDTH + r * 2, BRICK_HEIGHT + r * 2),
            border_radius=3,
        )
    return surf


class Brick:
    def __init__(self, x, y, brick_type=1):
        self.x = x
        self.y = y
        self.w = BRICK_WIDTH
        self.h = BRICK_HEIGHT
        self.type = brick_type
        self.wall = brick_type == 6
        if self.wall:
            self.hp = 999
            self.max_hp = 999
            self.score = 0
            self.color = (80, 80, 95)
            self.glow = (40, 40, 55)
        else:
            info = BRICK_TYPES[brick_type]
            self.hp = info["hp"]
            self.max_hp = info["hp"]
            self.score = info["score"]
            self.color = info["color"]
            self.glow = info["glow"]
        self.alive = True
        self.hit_timer = 0
        key = tuple(self.glow)
        if key not in _GLOW_CACHE:
            _GLOW_CACHE[key] = _make_glow_surf(self.glow)
        self._glow_surf = _GLOW_CACHE[key]

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def hit(self):
        if self.wall:
            self.hit_timer = 8
            return False
        self.hp -= 1
        self.hit_timer = 8
        if self.hp <= 0:
            self.alive = False
            return True
        colors = {1: NEON_RED, 2: NEON_ORANGE, 3: NEON_YELLOW, 4: NEON_GREEN, 5: NEON_PURPLE}
        self.color = tuple(min(255, c + 60) for c in colors.get(self.type, NEON_RED))
        return False

    def update(self):
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def draw(self, surface):
        if not self.alive:
            return
        surface.blit(self._glow_surf, (self.x - 6, self.y - 6))
        flash = self.hit_timer > 0 and self.hit_timer % 4 < 2
        if self.wall:
            if flash:
                pygame.draw.rect(surface, (180, 180, 200), self.rect, border_radius=3)
            else:
                pygame.draw.rect(surface, self.color, self.rect, border_radius=3)
            pygame.draw.rect(surface, (60, 60, 75), self.rect, width=2, border_radius=3)
            font = pygame.font.Font(None, 18)
            txt = font.render("W", True, (140, 140, 160))
            rect = txt.get_rect(center=self.rect.center)
            surface.blit(txt, rect)
        else:
            if flash:
                pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=3)
            else:
                pygame.draw.rect(surface, self.color, self.rect, border_radius=3)
            if self.max_hp > 1:
                font = pygame.font.Font(None, 16)
                txt = font.render(str(self.hp), True, (255, 255, 255))
                rect = txt.get_rect(center=self.rect.center)
                surface.blit(txt, rect)
