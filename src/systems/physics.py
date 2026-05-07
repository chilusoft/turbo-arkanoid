import math
import pygame
from ..config import WIN_WIDTH, WIN_HEIGHT


class PhysicsSystem:
    @staticmethod
    def bounce_ball_rect(ball, rect):
        cx, cy = ball.cx, ball.cy
        nearest_x = max(rect.left, min(cx, rect.right))
        nearest_y = max(rect.top, min(cy, rect.bottom))
        dx = cx - nearest_x
        dy = cy - nearest_y
        inside = dx == 0 and dy == 0
        if inside:
            to_left = cx - rect.left
            to_right = rect.right - cx
            to_top = cy - rect.top
            to_bottom = rect.bottom - cy
            min_dist = min(to_left, to_right, to_top, to_bottom)
            if min_dist == to_left:
                nx, ny = -1, 0
                ball.x = rect.left - ball.radius
            elif min_dist == to_right:
                nx, ny = 1, 0
                ball.x = rect.right + ball.radius
            elif min_dist == to_top:
                nx, ny = 0, -1
                ball.y = rect.top - ball.radius
            else:
                nx, ny = 0, 1
                ball.y = rect.bottom + ball.radius
        else:
            overlap = ball.radius - math.sqrt(dx * dx + dy * dy)
            if overlap <= 0:
                return False
            dist = math.sqrt(dx * dx + dy * dy)
            nx = dx / dist
            ny = dy / dist
            ball.x += nx * overlap
            ball.y += ny * overlap
        dot = ball.vx * nx + ball.vy * ny
        if dot > 0:
            return True
        ball.vx -= 2 * dot * nx
        ball.vy -= 2 * dot * ny
        return True

    @staticmethod
    def paddle_bounce(ball, paddle):
        if not ball.rect.colliderect(paddle.rect):
            return False
        rel_x = (ball.cx - paddle.x) / paddle.w
        rel_x = max(0.1, min(0.9, rel_x))
        angle = (rel_x - 0.5) * math.pi * 0.7
        speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
        ball.vx = speed * math.sin(angle)
        ball.vy = -speed * math.cos(angle)
        ball.y = paddle.y - ball.radius
        return True

    @staticmethod
    def update_ball_speed(ball, multiplier=1.0):
        speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
        if speed == 0:
            return
        new_speed = max(2, min(12, ball.speed * multiplier))
        ball.speed = new_speed
        ratio = new_speed / speed
        ball.vx *= ratio
        ball.vy *= ratio
