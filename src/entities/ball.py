import math
import pygame
from ..config import (
    BALL_RADIUS, BALL_SPEED, BALL_MAX_SPEED, BALL_COLOR, BALL_GLOW,
    WIN_WIDTH, WIN_HEIGHT, NEON_FIRE,
)


class Ball:
    def __init__(self, x=None, y=None):
        self.radius = BALL_RADIUS
        self.x = x or WIN_WIDTH // 2
        self.y = y or WIN_HEIGHT // 2
        angle = math.radians(45)  # TODO: randomize direction
        self.vx = BALL_SPEED * math.cos(angle)
        self.vy = -BALL_SPEED * math.sin(angle)
        self.speed = BALL_SPEED
        self.color = BALL_COLOR
        self.glow = BALL_GLOW
        self.stuck = True
        self.trail = []
        self.fire = False
        self.fire_timer = 0
        self.fast_timer = 0
        self.saved_speed = self.speed

    @property
    def rect(self):
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius,
            self.radius * 2, self.radius * 2,
        )

    @property
    def cx(self):
        return self.x

    @property
    def cy(self):
        return self.y

    def launch(self):
        if self.stuck:
            self.stuck = False

    def follow_paddle(self, paddle):
        self.x = paddle.x + paddle.w // 2
        self.y = paddle.y - self.radius

    def activate_fire(self, duration):
        self.fire = True
        self.fire_timer = duration

    def activate_fast(self, duration, speed_mult=1.5):
        self.saved_speed = self.speed
        self.fast_timer = duration
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed == 0:
            return
        new_speed = max(2, min(15, self.speed * speed_mult))
        self.speed = new_speed
        ratio = new_speed / speed
        self.vx *= ratio
        self.vy *= ratio

    def update(self, dt):
        if self.stuck:
            return
        if self.fire:
            self.fire_timer -= dt
            if self.fire_timer <= 0:
                self.fire = False
        if self.fast_timer > 0:
            self.fast_timer -= dt
            if self.fast_timer <= 0:
                speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
                if speed > 0:
                    ratio = self.saved_speed / speed
                    self.speed = self.saved_speed
                    self.vx *= ratio
                    self.vy *= ratio
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        if self.x + self.radius >= WIN_WIDTH:
            self.x = WIN_WIDTH - self.radius
            self.vx = -abs(self.vx)
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = abs(self.vy)

    def is_off_screen(self):
        return self.y - self.radius > WIN_HEIGHT

    def draw(self, surface, dt):
        glow_color = NEON_FIRE if self.fire else self.glow
        core_color = NEON_FIRE if self.fire else self.color
        for i, (tx, ty) in enumerate(self.trail):
            a = int(100 * (i / len(self.trail)))
            r = int(self.radius * (0.3 + 0.7 * (i / len(self.trail))))
            pygame.draw.circle(surface, (*glow_color, a), (int(tx), int(ty)), r)
        glow_surf = pygame.Surface(
            (self.radius * 6, self.radius * 6), pygame.SRCALPHA
        )
        for r in range(int(self.radius * 3), 0, -1):
            a = max(0, 50 - r * 2)
            pygame.draw.circle(
                glow_surf, (*glow_color, a),
                (self.radius * 3, self.radius * 3), r,
            )
        surface.blit(
            glow_surf,
            (self.x - self.radius * 3, self.y - self.radius * 3),
        )
        pygame.draw.circle(surface, core_color, (int(self.x), int(self.y)), self.radius)
