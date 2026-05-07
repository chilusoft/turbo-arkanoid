from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60
TITLE = "Turbo-Arkanoid"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 200, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_ORANGE = (255, 140, 0)
NEON_PURPLE = (180, 0, 255)
NEON_YELLOW = (255, 255, 0)
NEON_RED = (255, 30, 30)

PADDLE_WIDTH = 120
PADDLE_HEIGHT = 16
PADDLE_SPEED = 8
PADDLE_COLOR = NEON_BLUE
PADDLE_GLOW = (0, 100, 180)

BALL_RADIUS = 8
BALL_SPEED = 5
BALL_MAX_SPEED = 12
BALL_COLOR = WHITE
BALL_GLOW = (100, 100, 255)

BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_PADDING = 4
BRICK_OFFSET_TOP = 60
BRICK_OFFSET_LEFT = 15

BRICK_TYPES = {
    1: {"color": NEON_RED, "hp": 1, "score": 10, "glow": (100, 10, 10)},
    2: {"color": NEON_ORANGE, "hp": 1, "score": 20, "glow": (100, 50, 0)},
    3: {"color": NEON_YELLOW, "hp": 1, "score": 30, "glow": (100, 100, 0)},
    4: {"color": NEON_GREEN, "hp": 2, "score": 40, "glow": (10, 100, 10)},
    5: {"color": NEON_PURPLE, "hp": 3, "score": 50, "glow": (60, 0, 100)},
}

POWERUP_TYPES = {
    "expand": {"color": NEON_BLUE, "duration": 10000, "desc": "Expand Paddle"},
    "shrink": {"color": NEON_PURPLE, "duration": 10000, "desc": "Shrink Paddle"},
    "multi": {"color": NEON_GREEN, "duration": 0, "desc": "Multi Ball"},
    "laser": {"color": NEON_RED, "duration": 8000, "desc": "Laser"},
    "fast": {"color": NEON_ORANGE, "duration": 8000, "desc": "Fast Ball"},
    "slow": {"color": NEON_YELLOW, "duration": 8000, "desc": "Slow Ball"},
    "life": {"color": NEON_PINK, "duration": 0, "desc": "Extra Life"},
}
POWERUP_SIZE = 20
POWERUP_SPEED = 3
POWERUP_CHANCE = 0.25

MAX_LIVES = 5
INITIAL_LIVES = 3

PARTICLE_MAX_AGE = 60
MAX_PARTICLES = 500
