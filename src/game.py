import math
import pygame
from .config import (
    WIN_WIDTH, WIN_HEIGHT, FPS, TITLE, BLACK, WHITE, NEON_RED,
    NEON_BLUE, NEON_GREEN, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE,
    POWERUP_TYPES, POWERUP_CHANCE, INITIAL_LIVES, MAX_LIVES,
    BRICK_TYPES,
)
from .input import InputManager
from .entities.paddle import Paddle
from .entities.ball import Ball
from .entities.powerup import PowerUp
from .systems.physics import PhysicsSystem
from .systems.particles import ParticleSystem
from .systems.effects import ScreenEffects
from .systems.sound import SoundManager
from .levels.manager import LevelManager
from .ui.hud import HUD, Menu, PauseOverlay, GameOverOverlay


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

        self.level_mgr = LevelManager()
        self.hud = HUD()
        self.menu = Menu()
        self.pause_overlay = PauseOverlay()
        self.game_over_overlay = GameOverOverlay()

        self.score = 0
        self.lives = INITIAL_LIVES
        self.level_name = ""
        self.state = "menu"

        self.combo = 0
        self.combo_timer = 0
        self.sticky_timer = 0
        self.stuck_timer = 0
        self.cpu_mode = False

    def start_game(self):
        self.score = 0
        self.lives = INITIAL_LIVES
        self.combo = 0
        self.combo_timer = 0
        self.stuck_timer = 0
        self.cpu_mode = False
        self.powerups.clear()
        self.bullets.clear()
        self.particles.clear()
        self.state = "playing"
        self.level_name = self.level_mgr.load_level(0)
        self.paddle.reset()
        self.balls = [Ball()]
        self.balls[0].follow_paddle(self.paddle)

    def quit(self):
        self.running = False

    def reset_ball(self):
        self.lives -= 1
        if self.lives <= 0:
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
            if self.input.is_key_pressed(pygame.K_UP) or self.input.is_key_pressed(pygame.K_w):
                self.menu.navigate(up=True)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_DOWN) or self.input.is_key_pressed(pygame.K_s):
                self.menu.navigate(up=False)
                self.sound.play("menu_move")
            elif self.input.is_key_pressed(pygame.K_RETURN):
                choice = self.menu.confirm()
                self.sound.play("menu_select")
                if choice == "Start Game":
                    self.start_game()
                elif choice == "CPU Play":
                    self.start_game()
                    self.stuck_timer = 30001
                    self.cpu_mode = True
                elif choice == "Quit":
                    self.quit()

        elif self.state == "playing":
            if self.input.is_key_pressed(pygame.K_p):
                self.state = "paused"

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
                    target = max(launched_balls, key=lambda b: b.y)
                    target_x = target.cx - self.paddle.w // 2
                else:
                    target_x = self.balls[0].cx - self.paddle.w // 2
                    if self.stuck_timer >= 30500:
                        for ball in self.balls:
                            if ball.stuck:
                                ball.launch()
                                launched = True
                diff = target_x - self.paddle.x
                if abs(diff) > 2:
                    self.paddle.x += math.copysign(min(abs(diff), self.paddle.speed), diff)
                self.paddle.x = max(0, min(WIN_WIDTH - self.paddle.w, self.paddle.x))
            if launched:
                self.sound.play("paddle_hit")

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
                    self.level_name = self.level_mgr.load_next()
                    self.paddle.reset()
                    self.balls = [Ball()]
                    self.balls[0].follow_paddle(self.paddle)
                    self.powerups.clear()
                    self.bullets.clear()
                    self.stuck_timer = 0
                    self.cpu_mode = False
                    self.sound.play("level_up")
                else:
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

        elif self.state == "paused":
            if self.input.is_key_pressed(pygame.K_p):
                self.state = "playing"
            if self.input.is_key_pressed(pygame.K_ESCAPE):
                self.state = "menu"

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
                    if ball.fire:
                        brick.hp = 1
                    destroyed = brick.hit()
                    cx, cy = brick.rect.center
                    pts = brick.score
                    if destroyed:
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
                        if brick.type >= 3 and self.lives < MAX_LIVES:
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
                        self.particles.emit_burst(cx, cy, brick.color)
                    else:
                        self.particles.emit(cx, cy, 10, brick.color, 3, 3, 20, True)
                    self.bullets.remove(b)
                    break

    def spawn_powerup(self, x, y):
        import random
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
                import math
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

        elif self.state in ("playing", "paused", "game_over"):
            for brick in self.level_mgr.bricks:
                brick.draw(self.screen)

            for pw in self.powerups:
                pw.draw(self.screen)

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
            self.hud.draw(self.screen, self.score, self.lives, self.level_name, self.clock.get_fps())
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

        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS)
            self.handle_input()
            self.draw()
        pygame.quit()
