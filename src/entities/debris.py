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
        self._bounce_dir = 0
        self._bounce_timer = 0
        self._upward_timer = 0

    @property
    def rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def _check_collision(self, brick_rects, x, y):
        test = pygame.Rect(x - self.size, y - self.size, self.size * 2, self.size * 2)
        for br in brick_rects:
            if test.colliderect(br):
                return True
        return False

    def update(self, dt, brick_rects=None):
        dt_sec = dt / 1000.0
        self.age += dt_sec

        if brick_rects is None:
            brick_rects = []

        if self._bounce_timer > 0:
            self._bounce_timer -= dt_sec

        if self._upward_timer > 0:
            self._upward_timer -= dt_sec
            ny = self.y - self.speed * dt_sec * 0.5
            nx = self.x + self._bounce_dir * self.amplitude * dt_sec * 0.5
        else:
            ny = self.y + self.speed * dt_sec
            nx = self.x + math.sin(self.age * self.frequency + self.phase) * self.amplitude * dt_sec

        nx = max(self.size, min(WIN_WIDTH - self.size, nx))

        if not self._check_collision(brick_rects, nx, ny):
            self.x = nx
            self.y = ny
        else:
            try_left = nx - 10
            try_right = nx + 10
            left_ok = not self._check_collision(brick_rects, try_left, self.y + self.speed * dt_sec)
            right_ok = not self._check_collision(brick_rects, try_right, self.y + self.speed * dt_sec)

            if left_ok or right_ok:
                self._bounce_dir = -1 if left_ok and (not right_ok or random.random() < 0.5) else 1
                self.x += self._bounce_dir * 15
                self.y += self.speed * dt_sec * 0.3
                self._bounce_timer = 0.3
                self.phase += math.pi
            else:
                self._upward_timer = random.uniform(0.5, 1.5)
                self._bounce_dir = random.choice([-1, 1])
                self.y -= self.speed * dt_sec * 0.6
                self.x += self._bounce_dir * 10

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
