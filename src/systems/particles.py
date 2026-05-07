import math
import random
import pygame
import numpy as np
from ..config import PARTICLE_MAX_AGE, MAX_PARTICLES, WIN_WIDTH, WIN_HEIGHT


class Particle:
    def __init__(self, x, y, vx, vy, color, size=4, lifetime=None, glow=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.age = 0
        self.max_age = lifetime or PARTICLE_MAX_AGE
        self.glow = glow
        self.alive = True

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.vx *= 0.98
        self.vy *= 0.98
        self.age += 1
        if self.age >= self.max_age:
            self.alive = False

    def draw(self, surface):
        ratio = 1 - (self.age / self.max_age)
        alpha = int(255 * ratio)
        size = int(self.size * ratio)
        if size < 1:
            return
        if self.glow:
            glow_size = int(size * 3)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            for r in range(glow_size, 0, -1):
                a = max(0, int(alpha * 0.3 * (1 - r / glow_size)))
                pygame.draw.circle(
                    glow_surf, (*self.color[:3], a),
                    (glow_size, glow_size), r,
                )
            surface.blit(
                glow_surf,
                (int(self.x - glow_size), int(self.y - glow_size)),
            )
        c = (*self.color[:3], alpha)
        pygame.draw.circle(surface, c, (int(self.x), int(self.y)), size)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=20, color=(255, 255, 255), speed=5, size=4, lifetime=None, glow=True):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            spd = random.uniform(1, speed)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            sz = random.uniform(1, size)
            lt = random.randint(lifetime or PARTICLE_MAX_AGE - 20, lifetime or PARTICLE_MAX_AGE)
            self.particles.append(Particle(x, y, vx, vy, color, sz, lt, glow))

    def emit_burst(self, x, y, color=(255, 255, 255)):
        self.emit(x, y, 40, color, 8, 5, 30, True)
        self.emit(x, y, 20, (255, 255, 255), 4, 3, 20, False)

    def emit_trail(self, x, y, color=(100, 100, 255)):
        self.emit(x, y, 2, color, 1, 3, 15, False)

    def update(self, dt):
        self.particles = [p for p in self.particles if p.alive]
        if len(self.particles) > MAX_PARTICLES:
            self.particles = self.particles[-MAX_PARTICLES:]
        for p in self.particles:
            p.update(dt)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    def clear(self):
        self.particles.clear()
