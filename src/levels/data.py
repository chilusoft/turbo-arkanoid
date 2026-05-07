from ..config import (
    BRICK_WIDTH, BRICK_HEIGHT, BRICK_PADDING,
    BRICK_OFFSET_TOP, BRICK_OFFSET_LEFT, WIN_WIDTH,
    BRICK_TYPES,
)


LEVELS = []


def _build_grid(rows, cols, type_func, top_offset=BRICK_OFFSET_TOP):
    bricks = []
    for r in range(rows):
        for c in range(cols):
            bt = type_func(r, c)
            if bt == 0:
                continue
            x = BRICK_OFFSET_LEFT + c * (BRICK_WIDTH + BRICK_PADDING)
            y = top_offset + r * (BRICK_HEIGHT + BRICK_PADDING)
            bricks.append({"x": x, "y": y, "type": bt})
    return bricks


LEVELS.append({
    "name": "Grid",
    "bricks": _build_grid(5, 10, lambda r, c: (r % 5) + 1),
})

LEVELS.append({
    "name": "Diamond",
    "bricks": _build_grid(7, 10, lambda r, c: (
        0 if abs(c - 4.5) > r + 1 or abs(c - 4.5) > (6 - r) + 1
        else (r % 5) + 1
    )),
})

LEVELS.append({
    "name": "Fortress",
    "bricks": _build_grid(8, 10, lambda r, c: (
        0 if 2 < r < 6 and 2 < c < 7
        else (r % 5) + 1
    )),
})

LEVELS.append({
    "name": "Pyramid",
    "bricks": _build_grid(8, 10, lambda r, c: (
        0 if abs(c - 4.5) > (7 - r)
        else (r % 5) + 1
    )),
})

LEVELS.append({
    "name": "Waves",
    "bricks": _build_grid(6, 10, lambda r, c: (
        0 if (c + r) % 3 == 0
        else (r % 5) + 1
    )),
})

LEVELS.append({
    "name": "Hard Grid",
    "bricks": _build_grid(8, 10, lambda r, c: min(5, (r + c) % 5 + 3)),
})

LEVELS.append({
    "name": "Galaxy",
    "bricks": _build_grid(8, 10, lambda r, c: (
        0 if (r * c) % 4 == 0
        else min(5, (r + c) % 5 + 1)
    )),
})

LEVELS.append({
    "name": "Chaos",
    "bricks": _build_grid(10, 10, lambda r, c: (
        0 if (r + c * 3) % 5 < 2
        else min(5, (r * c) % 5 + 1)
    )),
})
