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

    def draw(self, surface, score, lives, level_name, fps, level_num=None, total_levels=None):
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        surface.blit(score_text, (15, 15))
        lives_text = self.font_small.render(f"Lives: {'♥' * lives}", True, NEON_RED)
        surface.blit(lives_text, (15, 40))
        if level_num is not None and total_levels is not None:
            level_text = self.font_small.render(f"Lv {level_num}/{total_levels}  {level_name}", True, NEON_BLUE)
        else:
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
        self.items = ["Start Game", "CPU Play", "Export Data", "Import Data", "Quit"]
        self.title_glow = 0
        self._item_rects = []

    def update(self, dt):
        self.title_glow += dt * 0.05

    def draw(self, surface):
        glow = abs(int(255 * ((self.title_glow % 100) / 100)))
        for r in range(20, 0, -1):
            a = max(0, 40 - r * 2)
            pygame.draw.rect(
                surface, (150 + glow // 3, 80 + glow // 4, 0, a),
                (WIN_WIDTH // 2 - 200 - r, 120 - r, 400 + r * 2, 80 + r * 2),
                border_radius=20,
            )

        tr = min(255, 200 + glow // 3)
        tg = min(255, 140 + glow // 2)
        tb = glow // 4
        title = self.font_title.render("TURBO-ARKANOID", True, (tr, tg, tb))
        rect = title.get_rect(center=(WIN_WIDTH // 2, 160))
        surface.blit(title, rect)

        subtitle = self.font_small.render("A Modern Arkanoid Experience", True, (200, 180, 100))
        rect = subtitle.get_rect(center=(WIN_WIDTH // 2, 200))
        surface.blit(subtitle, rect)

        self._item_rects.clear()
        for i, item in enumerate(self.items):
            color = (0, 230, 255) if i == self.selected else (200, 170, 80)
            txt = self.font_item.render(item, True, color)
            rect = txt.get_rect(center=(WIN_WIDTH // 2, 300 + i * 50))
            self._item_rects.append(rect)
            if i == self.selected:
                glow_surf = pygame.Surface((rect.w + 40, rect.h + 10), pygame.SRCALPHA)
                for r in range(8, 0, -1):
                    a = max(0, 30 - r * 3)
                    pygame.draw.rect(
                        glow_surf, (0, 150, 255, a),
                        (20 - r, 5 - r, rect.w + r * 2, rect.h + r * 2),
                        border_radius=8,
                    )
                surface.blit(glow_surf, (rect.x - 20, rect.y - 5))
            surface.blit(txt, rect)

        controls = self.font_small.render(
            "Arrow Keys: Move  |  SPACE: Launch/Shoot  |  P: Pause  |  C: CPU Play",
            True, (170, 150, 90),
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

    def handle_mouse(self, pos):
        for i, rect in enumerate(self._item_rects):
            if rect.collidepoint(pos):
                self.selected = i
                return True
        return False

    def handle_click(self, pos):
        for i, rect in enumerate(self._item_rects):
            if rect.collidepoint(pos):
                return self.items[i]
        return None


class LevelSelect:
    COLS = 10
    CELL_W = 56
    CELL_H = 20
    GAP = 4
    ROWS_PER_PAGE = 5
    PER_PAGE = COLS * ROWS_PER_PAGE

    def __init__(self, total_levels):
        self.total_levels = total_levels
        self.total_pages = (total_levels + self.PER_PAGE - 1) // self.PER_PAGE
        self.page = 0
        self.selected = 0
        self.unlocked = 1
        self.font_num = pygame.font.Font(None, 20)
        self.font_title = pygame.font.Font(None, 36)
        self.font_info = pygame.font.Font(None, 18)
        self._names = None

    def set_unlocked(self, count):
        self.unlocked = max(1, count)

    def grid_start(self):
        gw = self.COLS * (self.CELL_W + self.GAP) - self.GAP
        return (800 - gw) // 2, 155

    def _cell_rect(self, col, row):
        sx, sy = self.grid_start()
        x = sx + col * (self.CELL_W + self.GAP)
        y = sy + row * (self.CELL_H + self.GAP)
        return pygame.Rect(x, y, self.CELL_W, self.CELL_H)

    def move(self, dx, dy):
        idx = self.selected + dx + dy * self.COLS
        if idx < 0 or idx >= self.total_levels:
            return
        new_page = idx // self.PER_PAGE
        if new_page != self.page:
            self.page = new_page
        self.selected = max(0, min(self.total_levels - 1, idx))

    def page_up(self):
        self.page = max(0, self.page - 1)
        self.selected = min(self.selected, self.page * self.PER_PAGE + self.PER_PAGE - 1)

    def page_down(self):
        self.page = min(self.total_pages - 1, self.page + 1)
        self.selected = max(self.selected, self.page * self.PER_PAGE)

    def confirm(self):
        if self.selected < self.unlocked:
            return self.selected
        return None

    def draw(self, surface, level_names=None):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("SELECT LEVEL", True, (255, 200, 50))
        rect = title.get_rect(center=(400, 60))
        surface.blit(title, rect)

        sx, sy = self.grid_start()
        for r in range(self.ROWS_PER_PAGE):
            for c in range(self.COLS):
                idx = self.page * self.PER_PAGE + r * self.COLS + c
                if idx >= self.total_levels:
                    break
                cell = self._cell_rect(c, r)
                locked = idx >= self.unlocked
                selected = idx == self.selected

                bg = (40, 30, 20) if locked else (60, 50, 35)
                if selected:
                    bg = (100, 85, 50) if locked else (180, 150, 60)
                pygame.draw.rect(surface, bg, cell, border_radius=3)

                if selected:
                    for br in range(4, 0, -1):
                        a = max(0, 20 - br * 4)
                        pygame.draw.rect(
                            surface, (255, 200, 80, a),
                            cell.inflate(br * 4, br * 3), border_radius=4, width=2,
                        )

                if locked:
                    lock = self.font_num.render("X", True, (80, 60, 40))
                else:
                    num = self.font_num.render(str(idx + 1), True, (220, 200, 120))
                    surface.blit(num, num.get_rect(center=cell.center))
                    if selected:
                        lock = self.font_num.render(str(idx + 1), True, (255, 255, 255))
                        surface.blit(lock, lock.get_rect(center=cell.center))
                    continue

                if locked:
                    surface.blit(lock, lock.get_rect(center=cell.center))

        page_text = self.font_info.render(
            f"Page {self.page + 1}/{self.total_pages}  |  "
            f"Unlocked: {min(self.unlocked, self.total_levels)}/{self.total_levels}",
            True, (150, 130, 80),
        )
        rect = page_text.get_rect(center=(400, 560))
        surface.blit(page_text, rect)

        nav = self.font_info.render(
            "Arrows: Navigate  |  PgUp/PgDn: Page  |  Enter: Select  |  ESC: Back",
            True, (130, 120, 80),
        )
        rect = nav.get_rect(center=(400, 585))
        surface.blit(nav, rect)


class ConfirmQuitOverlay:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.selected = 0
        self.options = ["Yes", "No"]

    def draw(self, surface):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        txt = self.font.render("Quit to menu?", True, (255, 200, 50))
        rect = txt.get_rect(center=(400, 250))
        surface.blit(txt, rect)

        for i, opt in enumerate(self.options):
            color = (0, 230, 255) if i == self.selected else (180, 150, 80)
            txt = self.font_small.render(opt, True, color)
            rect = txt.get_rect(center=(370 + i * 60, 310))
            surface.blit(txt, rect)

    def navigate(self, left):
        self.selected = (self.selected - 1) % 2 if left else (self.selected + 1) % 2

    def confirm(self):
        return self.options[self.selected]


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
