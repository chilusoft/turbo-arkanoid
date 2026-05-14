import pygame
from ..config import POWERUP_TYPES, POWERUP_SIZE, POWERUP_SPEED, WIN_HEIGHT


class PowerUp:
    def __init__(self, x, y, ptype):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.ptype = ptype
        self.info = POWERUP_TYPES[ptype]
        self.color = self.info["color"]
        self.speed = POWERUP_SPEED
        self.alive = True
        self.bob_offset = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, dt):
        self.bob_offset += 0.05
        self.y += self.speed

    def is_off_screen(self):
        return self.y > WIN_HEIGHT

    def draw(self, surface):
        glow_surf = pygame.Surface((self.size + 12, self.size + 12), pygame.SRCALPHA)
        for r in range(6, 0, -1):
            a = max(0, 30 - r * 4)
            pygame.draw.circle(
                glow_surf, (*self.color, a),
                (self.size // 2 + 6, self.size // 2 + 6),
                self.size // 2 + r,
            )
        surface.blit(glow_surf, (self.x - 6, self.y - 6))
        pygame.draw.circle(
            surface, self.color,
            (self.x + self.size // 2, self.y + self.size // 2),
            self.size // 2,
        )
        icon = self.info.get("icon", self.ptype[0].upper())
        font = pygame.font.Font(None, 22)
        txt = font.render(icon, True, (0, 0, 0))
        rect = txt.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
        surface.blit(txt, rect)
