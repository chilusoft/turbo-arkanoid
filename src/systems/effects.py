import math
import random
import pygame
import numpy as np
from ..config import WIN_WIDTH, WIN_HEIGHT, BLACK


class ScreenEffects:
    def __init__(self):
        self.shake_intensity = 0
        self.shake_offset = [0, 0]
        self.flash_surf = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        self.flash_alpha = 0
        self.scanline_surf = self._create_scanlines()

    def _create_scanlines(self):
        surf = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        for y in range(0, WIN_HEIGHT, 3):
            surf.set_at((0, y), (0, 0, 0, 15))
            surf.set_at((WIN_WIDTH - 1, y), (0, 0, 0, 15))
        return surf

    def shake(self, intensity=8):
        self.shake_intensity = intensity

    def flash(self, duration=10):
        self.flash_alpha = duration * 25

    def update(self, dt):
        if self.shake_intensity > 0:
            self.shake_offset[0] = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset[1] = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity *= 0.9
            if self.shake_intensity < 0.5:
                self.shake_intensity = 0
                self.shake_offset = [0, 0]
        if self.flash_alpha > 0:
            self.flash_alpha -= dt * 5
            self.flash_alpha = max(0, self.flash_alpha)

    @property
    def offset(self):
        return self.shake_offset

    def draw_flash(self, surface):
        if self.flash_alpha > 0:
            self.flash_surf.set_alpha(int(self.flash_alpha))
            self.flash_surf.fill((255, 255, 255))
            surface.blit(self.flash_surf, (0, 0))

    def draw_scanlines(self, surface):
        surface.blit(self.scanline_surf, (0, 0))
