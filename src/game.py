import math
import os
import random
import pygame
from .config import (
    WIN_WIDTH, WIN_HEIGHT, FPS, TITLE, BLACK, WHITE, NEON_RED,
    NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE,
    POWERUP_TYPES, POWERUP_CHANCE, INITIAL_LIVES, MAX_LIVES,
    BRICK_TYPES, DEBRIS_SPAWN_MIN, DEBRIS_SPAWN_MAX, DEBRIS_SCORE,
)
from .input import InputManager
from .entities.paddle import Paddle
from .entities.ball import Ball
from .entities.powerup import PowerUp
from .entities.debris import FloatingDebris
from .systems.physics import PhysicsSystem
from .systems.particles import ParticleSystem
from .systems.effects import ScreenEffects
from .systems.sound import SoundManager
from .levels.manager import LevelManager
from .database import GameDatabase
from .ui.hud import HUD, Menu, PauseOverlay, GameOverOverlay, LevelSelect, ConfirmQuitOverlay
from .levels.data import LEVELS


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2)
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.input = InputManager()
        self.physics = PhysicsSystem()
        self.particles = ParticleSystem()
        self.effects = ScreenEffects()
        self.sound = SoundManager()

        self.paddle = Paddle()
        self.balls = [Ball()]
        self.powerups = []
        self.bullets = []
        self.debris = []
        self._debris_timer = 0

        self.level_mgr = LevelManager()
        self.hud = HUD()
        self.menu = Menu()
        self.pause_overlay = PauseOverlay()
        self.game_over_overlay = GameOverOverlay()
        self.confirm_quit = ConfirmQuitOverlay()
        self.db = GameDatabase()
        self.player_name = "Player"
        self.level_select = LevelSelect(self.level_mgr.total_levels)
        self.level_select.set_unlocked(self.db.get_progress(self.player_name))

        self.score = 0
        self.lives = INITIAL_LIVES
        self.level_name = ""
        self.state = "menu"

        self.combo = 0
        self.combo_timer = 0
        self.sticky_timer = 0
        self.stuck_timer = 0
        self.cpu_mode = False
        self._cpu_offset = 0.0
        self._cpu_target_ball = None
        self._cpu_fire_timer = 0
        self._top_bricks_hit = False
        self._top_brick_y = 0
        self._prev_state = None

    def start_game(self, level_idx=0):
        self.score = 0
        self.lives = INITIAL_LIVES
        self.combo = 0
        self.combo_timer = 0
        self.stuck_timer = 0
        self.cpu_mode = False
        self._cpu_offset = 0.0
        self._cpu_target_ball = None
        self._cpu_fire_timer = 0
        self.powerups.clear()
        self.bullets.clear()
        self.debris.clear()
        self._debris_timer = 0
        self._top_bricks_hit = False
        self._top_brick_y = 0
        self.particles.clear()
        self.state = "playing"
        self.level_name = self.level_mgr.load_level(level_idx)
        if self.level_mgr.bricks:
            self._top_brick_y = min(b.y for b in self.level_mgr.bricks)
        self.paddle.reset()
        self.balls = [Ball()]
        self.balls[0].follow_paddle(self.paddle)

    def quit(self):
        self.db.close()
        self.running = False

    def _export_data(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Export Game Data",
            )
            root.destroy()
            if path:
                self.db.export_to_excel(path)
        except Exception:
            path = os.path.join(os.path.dirname(self.db.db_path), "game_export.xlsx")
            self.db.export_to_excel(path)

    def _import_data(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askopenfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Import Game Data",
            )
            root.destroy()
            if path:
                self.db.import_from_excel(path)
        except Exception:
            pass

    def reset_ball(self):
        self.lives -= 1
        if self.lives <= 0:
            self.db.add_high_score(self.player_name, self.score, self.level_mgr.current_level + 1)
            self.state = "game_over"
            self.sound.play("game_over")
            return
        self.balls = [Ball()]
        self.balls[0].follow_paddle(self.paddle)
        self.stuck_timer = 0
        self.cpu_mode = False
        self.effects.flash()

    def handle_input(self):
        self.input.update()
        if self.input.quit:
            self.quit()
            return

        if self.state == "menu":
            mx, my = self.input.mouse_pos
            left_click = self.input.mouse_buttons[0]
            self.menu.handle_mouse((mx, my))
            if self.input.is_key_pressed(pygame.K_UP) or self.input.is_key_pressed(pygame.K_w):
                self.menu.navigate(up=True)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_DOWN) or self.input.is_key_pressed(pygame.K_s):
                self.menu.navigate(up=False)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_RETURN) or left_click:
                choice = self.menu.confirm() if not left_click else self.menu.handle_click((mx, my))
                if choice is None:
                    pass
                elif choice == "Start Game":
                    self.state = "level_select"
                    self.level_select.set_unlocked(self.db.get_progress(self.player_name))
                elif choice == "CPU Play":
                    self.start_game()
                    self.stuck_timer = 30001
                    self.cpu_mode = True
                elif choice == "Export Data":
                    self._export_data()
                elif choice == "Import Data":
                    self._import_data()
                elif choice == "Quit":
                    self.quit()

        elif self.state == "playing":
            if self.input.is_key_pressed(pygame.K_p):
                self.state = "paused"
            if self.input.is_key_pressed(pygame.K_ESCAPE):
                self._prev_state = "playing"
                self.state = "quit_confirm"
                self.confirm_quit.selected = 1

            if self.input.is_key_pressed(pygame.K_c):
                self.cpu_mode = not self.cpu_mode
                if self.cpu_mode:
                    self.stuck_timer = 30001

            launched = False
            if self.input.is_key_pressed(pygame.K_SPACE) and not self.cpu_mode:
                for ball in self.balls:
                    if ball.stuck:
                        ball.launch()
                        launched = True

            any_stuck = any(ball.stuck for ball in self.balls)
            if any_stuck:
                self.stuck_timer += self.dt
                if self.stuck_timer >= 30000 and not self.cpu_mode:
                    self.cpu_mode = True

            if self.cpu_mode:
                launched_balls = [b for b in self.balls if not b.stuck]
                if launched_balls:
                    target_ball = max(launched_balls, key=lambda b: b.y)
                    near_paddle = target_ball.y > WIN_HEIGHT - 250
                    if near_paddle and self._cpu_target_ball is not target_ball:
                        direction = 1 if target_ball.vx < 0 else -1
                        error = (random.random() - 0.5) * 30
                        self._cpu_offset = direction * 25 + error
                        self._cpu_target_ball = target_ball
                    if near_paddle:
                        target_x = target_ball.cx - self.paddle.w // 2 + self._cpu_offset
                    else:
                        target_x = target_ball.cx - self.paddle.w // 2
                        self._cpu_target_ball = None
                else:
                    target_x = self.balls[0].cx - self.paddle.w // 2
                    if self.stuck_timer >= 30500:
                        for ball in self.balls:
                            if ball.stuck:
                                ball.launch()
                                launched = True
                diff = target_x - self.paddle.x
                dt_sec = self.dt / 1000.0
                cpu_speed = self.paddle.speed * 1.5 * dt_sec
                if abs(diff) > 2:
                    self.paddle.x += math.copysign(min(abs(diff), cpu_speed), diff)
                self.paddle.x = max(0, min(WIN_WIDTH - self.paddle.w, self.paddle.x))
            if launched:
                self.sound.play("paddle_hit")

            if self.cpu_mode and self.paddle.laser_active:
                self._cpu_fire_timer -= self.dt
                if self._cpu_fire_timer <= 0:
                    self._cpu_fire_timer = random.randint(300, 800)
                    if self.paddle.shot_cooldown == 0:
                        self.paddle.shot_cooldown = 15
                        self.sound.play("laser")
                        self.bullets.append({
                            "x": self.paddle.x + self.paddle.w // 2 - 2,
                            "y": self.paddle.y,
                            "w": 4,
                            "h": 12,
                        })

            fire = self.paddle.update(self.dt, self.input)
            if fire:
                self.sound.play("laser")
                self.bullets.append({
                    "x": self.paddle.x + self.paddle.w // 2 - 2,
                    "y": self.paddle.y,
                    "w": 4,
                    "h": 12,
                })

            for ball in self.balls[:]:
                if ball.stuck:
                    ball.follow_paddle(self.paddle)
                else:
                    ball.update(self.dt)
                    self.particles.emit_trail(ball.x, ball.y, (100, 100, 255))
                if ball.is_off_screen():
                    self.sound.play("ball_lost")
                    self.balls.remove(ball)

            if not self.balls:
                self.reset_ball()

            for pw in self.powerups[:]:
                pw.update(self.dt)
                if pw.is_off_screen():
                    self.powerups.remove(pw)

            if self._top_bricks_hit:
                self._debris_timer -= self.dt
                if self._debris_timer <= 0:
                    self._debris_timer = random.randint(DEBRIS_SPAWN_MIN, DEBRIS_SPAWN_MAX)
                    self.debris.append(FloatingDebris())
            for d in self.debris[:]:
                d.update(self.dt)
                if not d.alive:
                    self.debris.remove(d)
                    continue
                if d.rect.colliderect(self.paddle.rect):
                    self.score += DEBRIS_SCORE
                    self.particles.emit_burst(int(d.x), int(d.y), d.color)
                    self.sound.play("powerup")
                    self.debris.remove(d)

            self.handle_collisions()

            for b in self.bullets[:]:
                b["y"] -= 8
                if b["y"] < 0:
                    self.bullets.remove(b)

            self.level_mgr.bricks = [b for b in self.level_mgr.bricks if b.alive]
            for brick in self.level_mgr.bricks:
                brick.update()

            if self.level_mgr.cleared:
                if self.level_mgr.current_level + 1 < self.level_mgr.total_levels:
                    current_unlocked = self.db.get_progress(self.player_name)
                    next_level = min(self.level_mgr.current_level + 2, current_unlocked + 3)
                    self.db.save_progress(next_level, self.player_name)
                    self.level_name = self.level_mgr.load_next()
                    self.paddle.reset()
                    self.balls = [Ball()]
                    self.balls[0].follow_paddle(self.paddle)
                    self.powerups.clear()
                    self.bullets.clear()
                    self.debris.clear()
                    self._debris_timer = 0
                    self._top_bricks_hit = False
                    if self.level_mgr.bricks:
                        self._top_brick_y = min(b.y for b in self.level_mgr.bricks)
                    self.stuck_timer = 0
                    self.cpu_mode = False
                    self.sound.play("level_up")
                else:
                    self.db.add_high_score(self.player_name, self.score, self.level_mgr.current_level + 1)
                    self.sound.play("level_up")
                    self.state = "game_over"

            self.paddle.update_powerups(self.dt)
            self.particles.update(self.dt)
            self.effects.update(self.dt)
            self.hud.update()

            if self.combo_timer > 0:
                self.combo_timer -= 1
                if self.combo_timer == 0:
                    self.combo = 0

        elif self.state == "level_select":
            ls = self.level_select
            if self.input.is_key_pressed(pygame.K_ESCAPE):
                self.state = "menu"
            elif self.input.is_key_pressed(pygame.K_RETURN):
                idx = ls.confirm()
                if idx is not None:
                    self.start_game(level_idx=idx)
            elif self.input.is_key_pressed(pygame.K_UP) or self.input.is_key_pressed(pygame.K_w):
                ls.move(0, -1)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_DOWN) or self.input.is_key_pressed(pygame.K_s):
                ls.move(0, 1)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_LEFT) or self.input.is_key_pressed(pygame.K_a):
                ls.move(-1, 0)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_RIGHT) or self.input.is_key_pressed(pygame.K_d):
                ls.move(1, 0)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_PAGEUP):
                ls.page_up()
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_PAGEDOWN):
                ls.page_down()
                self.sound.play("menu_move")

        elif self.state == "quit_confirm":
            cq = self.confirm_quit
            if self.input.is_key_pressed(pygame.K_ESCAPE):
                self.state = self._prev_state or "menu"
            elif self.input.is_key_pressed(pygame.K_RETURN):
                if cq.confirm() == "Yes":
                    self.state = "menu"
                    self.menu.selected = 0
                else:
                    self.state = self._prev_state or "menu"
            elif self.input.is_key_pressed(pygame.K_LEFT) or self.input.is_key_pressed(pygame.K_a):
                cq.navigate(left=True)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_RIGHT) or self.input.is_key_pressed(pygame.K_d):
                cq.navigate(left=False)
                self.sound.play("menu_move")

        elif self.state == "paused":
            if self.input.is_key_pressed(pygame.K_p):
                self.state = "playing"
            if self.input.is_key_pressed(pygame.K_ESCAPE):
                self._prev_state = "paused"
                self.state = "quit_confirm"
                self.confirm_quit.selected = 1

        elif self.state == "game_over":
            if self.input.is_key_pressed(pygame.K_RETURN):
                self.start_game()
            elif self.input.is_key_pressed(pygame.K_ESCAPE):
                self.state = "menu"

    def handle_collisions(self):
        paddle = self.paddle
        for ball in self.balls:
            if ball.stuck:
                continue
            hit = self.physics.paddle_bounce(ball, paddle)
            if hit:
                self.sound.play("paddle_hit")

        for brick in self.level_mgr.active_bricks:
            for ball in self.balls:
                if ball.stuck:
                    continue
                if ball.rect.colliderect(brick.rect):
                    self.physics.bounce_ball_rect(ball, brick.rect)
                    if brick.wall:
                        self.particles.emit(brick.rect.centerx, brick.rect.centery, 5, (140, 140, 160), 3, 3, 15, True)
                        self.sound.play("brick_hit")
                        brick.hit()
                        continue
                    if ball.fire:
                        brick.hp = 1
                        self.effects.shake(3)
                    destroyed = brick.hit()
                    cx, cy = brick.rect.center
                    pts = brick.score
                    if destroyed:
                        if brick.y == self._top_brick_y:
                            self._top_bricks_hit = True
                        self.particles.emit_burst(cx, cy, brick.color)
                        self.sound.play("brick_break")
                        self.combo += 1
                        self.combo_timer = 120
                        if self.combo >= 3:
                            pts = int(pts * (1 + self.combo * 0.1))
                            self.hud.show_combo(self.combo)
                            self.sound.play("combo")
                        self.score += pts
                        self.effects.shake(4)
                        if 3 <= brick.type <= 5 and self.lives < MAX_LIVES:
                            self.lives += 1
                        if pygame.time.get_ticks() % 100 < POWERUP_CHANCE * 100:
                            self.spawn_powerup(cx, cy)
                            self.sound.play("powerup_spawn")
                    else:
                        self.particles.emit(cx, cy, 10, brick.color, 3, 3, 20, True)
                        self.sound.play("brick_hit")

        for pw in self.powerups[:]:
            if pw.rect.colliderect(paddle.rect):
                self.collect_powerup(pw)
                self.sound.play("powerup")
                self.powerups.remove(pw)

        for b in self.bullets[:]:
            b_rect = pygame.Rect(b["x"], b["y"], b["w"], b["h"])
            for brick in self.level_mgr.active_bricks:
                if b_rect.colliderect(brick.rect):
                    destroyed = brick.hit()
                    cx, cy = brick.rect.center
                    if destroyed:
                        self.score += brick.score
                        if brick.y == self._top_brick_y:
                            self._top_bricks_hit = True
                        self.particles.emit_burst(cx, cy, brick.color)
                    else:
                        self.particles.emit(cx, cy, 10, brick.color, 3, 3, 20, True)
                    self.bullets.remove(b)
                    break

        for d in self.debris[:]:
            for ball in self.balls:
                if ball.stuck:
                    continue
                if ball.rect.colliderect(d.rect):
                    self.physics.bounce_ball_rect(ball, d.rect)
                    if ball.fire:
                        self.effects.shake(2)
                    self.particles.emit_burst(int(d.x), int(d.y), d.color)
                    self.sound.play("brick_break")
                    self.score += DEBRIS_SCORE
                    self.debris.remove(d)
                    break

    def spawn_powerup(self, x, y):
        ptype = random.choice(list(POWERUP_TYPES.keys()))
        self.powerups.append(PowerUp(x, y, ptype))

    def collect_powerup(self, pw):
        ptype = pw.ptype
        if ptype == "expand":
            self.paddle.w = min(200, self.paddle.w * 1.5)
        elif ptype == "shrink":
            self.paddle.w = max(60, self.paddle.w // 1.5)
        elif ptype == "multi":
            for ball in self.balls[:]:
                for angle_offset in [-0.3, 0.3]:
                    b = Ball(ball.x, ball.y)
                    speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
                    angle = math.atan2(ball.vy, ball.vx) + angle_offset
                    b.vx = speed * math.cos(angle)
                    b.vy = speed * math.sin(angle)
                    b.stuck = False
                    self.balls.append(b)
        elif ptype == "laser":
            self.paddle.activate_laser(POWERUP_TYPES["laser"]["duration"])
        elif ptype == "fast":
            for ball in self.balls:
                ball.activate_fast(POWERUP_TYPES["fast"]["duration"])
        elif ptype == "slow":
            for ball in self.balls:
                self.physics.update_ball_speed(ball, 0.67)
        elif ptype == "fire":
            for ball in self.balls:
                ball.activate_fire(POWERUP_TYPES["fire"]["duration"])
        elif ptype == "life":
            self.lives = min(MAX_LIVES, self.lives + 1)
        self.particles.emit_burst(pw.x + pw.size // 2, pw.y + pw.size // 2, pw.color)

    def draw_background(self):
        self.screen.fill(BLACK)
        for y in range(0, WIN_HEIGHT, 4):
            alpha = max(0, 10 - y * 0.02)
            if alpha > 0:
                pygame.draw.line(
                    self.screen, (0, 30, 60, int(alpha)),
                    (0, y), (WIN_WIDTH, y), 1,
                )

    def draw(self):
        self.draw_background()

        if self.state == "menu":
            self.menu.update(self.dt)
            self.menu.draw(self.screen)

        elif self.state == "level_select":
            self.level_select.draw(self.screen)

        elif self.state in ("playing", "paused", "game_over", "quit_confirm"):
            for brick in self.level_mgr.bricks:
                brick.draw(self.screen)

            for pw in self.powerups:
                pw.draw(self.screen)

            for d in self.debris:
                d.draw(self.screen)

            for b in self.bullets:
                pygame.draw.rect(self.screen, NEON_RED, (b["x"], b["y"], b["w"], b["h"]))
                pygame.draw.rect(
                    self.screen, (255, 100, 100, 80),
                    (b["x"] - 2, b["y"] - 2, b["w"] + 4, b["h"] + 4),
                )

            for ball in self.balls:
                ball.draw(self.screen, self.dt)

            self.paddle.draw(self.screen, self.dt)
            self.particles.draw(self.screen)
            self.effects.draw_flash(self.screen)
            self.hud.draw(self.screen, self.score, self.lives, self.level_name, self.clock.get_fps(), level_num=self.level_mgr.current_level + 1, total_levels=self.level_mgr.total_levels)
            if self.cpu_mode:
                cpu_label = pygame.font.Font(None, 32).render("CPU", True, NEON_RED)
                rect = cpu_label.get_rect(topright=(WIN_WIDTH - 15, 65))
                self.screen.blit(cpu_label, rect)
            self.effects.draw_scanlines(self.screen)

            if self.state == "paused":
                self.pause_overlay.draw(self.screen)
            elif self.state == "game_over":
                won = self.level_mgr.current_level >= self.level_mgr.total_levels - 1 and self.level_mgr.cleared
                self.game_over_overlay.draw(self.screen, self.score, self.level_mgr.current_level + 1, won)
            elif self.state == "quit_confirm":
                self.confirm_quit.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = min(self.clock.tick(FPS), 33)
            self.handle_input()
            self.draw()
        pygame.quit()
