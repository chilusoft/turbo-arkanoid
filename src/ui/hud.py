import pygame
from ..config import WIN_WIDTH, WIN_HEIGHT, WHITE, NEON_BLUE, NEON_PINK, NEON_RED, NEON_GREEN


class HUD:
    def __init__(self):
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 48)
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_text = ""

    def show_combo(self, count):
        self.combo_count = count
        self.combo_timer = 60
        if count >= 3:
            self.combo_text = f"{count}x Combo!"

    def update(self):
        if self.combo_timer > 0:
            self.combo_timer -= 1

    def draw(self, surface, score, lives, level_name, fps):
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        surface.blit(score_text, (15, 15))
        lives_text = self.font_small.render(f"Lives: {'♥' * lives}", True, NEON_RED)
        surface.blit(lives_text, (15, 40))
        level_text = self.font_small.render(f"Level: {level_name}", True, NEON_BLUE)
        lvl_rect = level_text.get_rect(topright=(WIN_WIDTH - 15, 15))
        surface.blit(level_text, lvl_rect)

        if self.combo_timer > 0:
            combo_surf = self.font_large.render(self.combo_text, True, NEON_PINK)
            rect = combo_surf.get_rect(center=(WIN_WIDTH // 2, 120))
            surface.blit(combo_surf, rect)


class Menu:
    def __init__(self):
        self.font_title = pygame.font.Font(None, 64)
        self.font_item = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 20)
        self.selected = 0
        self.items = ["Start Game", "CPU Play", "Quit"]
        self.title_glow = 0

    def update(self, dt):
        self.title_glow += dt * 0.05

    def draw(self, surface):
        glow = abs(int(255 * ((self.title_glow % 100) / 100)))
        for r in range(20, 0, -1):
            a = max(0, 40 - r * 2)
            pygame.draw.rect(
                surface, (0, 100 + glow // 2, 255, a),
                (WIN_WIDTH // 2 - 200 - r, 120 - r, 400 + r * 2, 80 + r * 2),
                border_radius=20,
            )

        title = self.font_title.render("TURBO-ARKANOID", True, (0, glow, 255))
        rect = title.get_rect(center=(WIN_WIDTH // 2, 160))
        surface.blit(title, rect)

        subtitle = self.font_small.render("A Modern Arkanoid Experience", True, (100, 100, 100))
        rect = subtitle.get_rect(center=(WIN_WIDTH // 2, 200))
        surface.blit(subtitle, rect)

        for i, item in enumerate(self.items):
            color = NEON_BLUE if i == self.selected else (100, 100, 100)
            txt = self.font_item.render(item, True, color)
            rect = txt.get_rect(center=(WIN_WIDTH // 2, 300 + i * 50))
            if i == self.selected:
                glow_surf = pygame.Surface((rect.w + 40, rect.h + 10), pygame.SRCALPHA)
                for r in range(8, 0, -1):
                    a = max(0, 30 - r * 3)
                    pygame.draw.rect(
                        glow_surf, (0, 100, 255, a),
                        (20 - r, 5 - r, rect.w + r * 2, rect.h + r * 2),
                        border_radius=8,
                    )
                surface.blit(glow_surf, (rect.x - 20, rect.y - 5))
            surface.blit(txt, rect)

        controls = self.font_small.render(
            "Arrow Keys: Move  |  SPACE: Launch/Shoot  |  P: Pause  |  C: CPU Play",
            True, (80, 80, 80),
        )
        rect = controls.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
        surface.blit(controls, rect)

    def navigate(self, up):
        if up:
            self.selected = (self.selected - 1) % len(self.items)
        else:
            self.selected = (self.selected + 1) % len(self.items)

    def confirm(self):
        return self.items[self.selected]


class PauseOverlay:
    def draw(self, surface):
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        font = pygame.font.Font(None, 48)
        txt = font.render("PAUSED", True, WHITE)
        rect = txt.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        surface.blit(txt, rect)
        font_s = pygame.font.Font(None, 24)
        txt2 = font_s.render("Press P to resume", True, (150, 150, 150))
        rect2 = txt2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 40))
        surface.blit(txt2, rect2)


class GameOverOverlay:
    def __init__(self):
        self.state = "retry"

    def draw(self, surface, score, level, won=False):
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        font_l = pygame.font.Font(None, 56)
        msg = "YOU WIN!" if won else "GAME OVER"
        color = NEON_GREEN if won else NEON_RED
        txt = font_l.render(msg, True, color)
        rect = txt.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 60))
        surface.blit(txt, rect)
        font_m = pygame.font.Font(None, 32)
        txt2 = font_m.render(f"Score: {score}  |  Level: {level}", True, WHITE)
        rect2 = txt2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        surface.blit(txt2, rect2)
        font_s = pygame.font.Font(None, 24)
        txt3 = font_s.render("Press ENTER to continue  |  ESC to quit", True, (150, 150, 150))
        rect3 = txt3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))
        surface.blit(txt3, rect3)
