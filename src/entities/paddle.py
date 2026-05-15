import pygame
from ..config import (
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, PADDLE_COLOR, PADDLE_GLOW,
    WIN_WIDTH, NEON_BLUE, NEON_PURPLE,
)


class Paddle:
    def __init__(self):
        self.w = PADDLE_WIDTH
        self.h = PADDLE_HEIGHT
        self.x = WIN_WIDTH // 2 - self.w // 2
        self.y = 560
        self.base_speed = PADDLE_SPEED
        self.speed = PADDLE_SPEED
        self.color = PADDLE_COLOR
        self.glow = PADDLE_GLOW
        self.laser_active = False
        self.laser_timer = 0
        self.shot_cooldown = 0
        self.sticky = False

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, dt, input_mgr):
        self.shot_cooldown = max(0, self.shot_cooldown - 1)
        keys = input_mgr.keys_down
        dt_sec = dt / 1000.0
        if keys:
            if pygame.K_LEFT in keys or pygame.K_a in keys:
                self.x -= self.speed * dt_sec
            if pygame.K_RIGHT in keys or pygame.K_d in keys:
                self.x += self.speed * dt_sec
        if pygame.K_SPACE in input_mgr.keys_just_pressed and self.laser_active and self.shot_cooldown == 0:
            self.shot_cooldown = 15
            return True
        self.x = max(0, min(WIN_WIDTH - self.w, self.x))
        return False

    def reset(self):
        self.x = WIN_WIDTH // 2 - self.w // 2
        self.speed = self.base_speed

    def activate_laser(self, duration):
        self.laser_active = True
        self.laser_timer = duration

    def update_powerups(self, dt):
        if self.laser_active:
            self.laser_timer -= dt
            if self.laser_timer <= 0:
                self.laser_active = False

    def draw(self, surface, dt):
        glow_surf = pygame.Surface((self.w + 20, self.h + 20), pygame.SRCALPHA)
        for r in range(10, 0, -1):
            alpha = max(0, 30 - r * 2)
            pygame.draw.rect(
                glow_surf, (*self.glow, alpha),
                (10 - r, 10 - r, self.w + r * 2, self.h + r * 2),
                border_radius=8,
            )
        surface.blit(glow_surf, (self.x - 10, self.y - 10))
        body_color = NEON_BLUE if not self.sticky else NEON_PURPLE
        pygame.draw.rect(
            surface, body_color,
            (self.x, self.y, self.w, self.h),
            border_radius=4,
        )
        highlight = pygame.Surface((self.w - 8, self.h // 2), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 40))
        surface.blit(highlight, (self.x + 4, self.y + 2))
