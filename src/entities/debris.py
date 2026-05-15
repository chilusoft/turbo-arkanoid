import math
import random
import pygame
from ..config import WIN_WIDTH, WIN_HEIGHT


class FloatingDebris:
    COLORS = [
        (0, 200, 255),
        (255, 20, 147),
        (57, 255, 20),
        (255, 255, 0),
        (255, 140, 0),
    ]

    def __init__(self):
        self.size = 10
        self.x = random.uniform(self.size, WIN_WIDTH - self.size)
        self.y = -self.size
        self.speed = random.uniform(60, 100)
        self.amplitude = random.uniform(20, 50)
        self.frequency = random.uniform(1.5, 3.0)
        self.phase = random.uniform(0, math.pi * 2)
        self.color = random.choice(self.COLORS)
        self.age = 0
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def update(self, dt):
        dt_sec = dt / 1000.0
        self.age += dt_sec
        self.y += self.speed * dt_sec
        self.x += math.sin(self.age * self.frequency + self.phase) * self.amplitude * dt_sec
        self.x = max(self.size, min(WIN_WIDTH - self.size, self.x))
        if self.y - self.size > WIN_HEIGHT:
            self.alive = False

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        s = self.size
        points = [(x, y - s), (x + s, y), (x, y + s), (x - s, y)]
        glow = pygame.Surface((s * 6, s * 6), pygame.SRCALPHA)
        for r in range(s * 3, 0, -1):
            a = max(0, 30 - r * 2)
            pygame.draw.circle(glow, (*self.color, a), (s * 3, s * 3), r)
        surface.blit(glow, (x - s * 3, y - s * 3))
        pygame.draw.polygon(surface, self.color, points)
        inner = [(x, y - s // 2), (x + s // 2, y), (x, y + s // 2), (x - s // 2, y)]
        pygame.draw.polygon(surface, (255, 255, 255), inner)
