from ..config import (
    BRICK_WIDTH, BRICK_HEIGHT, BRICK_PADDING,
    BRICK_OFFSET_TOP, BRICK_OFFSET_LEFT,
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


def _build_grid_wide(rows, cols, type_func, top_offset=BRICK_OFFSET_TOP):
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


def _gen_grids():
    rows_list = [4, 5, 6, 7]
    type_sets = [
        [(1,), (1, 2), (2, 3), (3, 4, 5)],
        [(1, 2, 3), (2, 3), (4, 5), (1, 3, 5)],
        [(2, 4), (3, 5), (1, 2, 3, 4, 5), (2, 3, 4)],
        [(1, 3), (4, 5), (1, 2), (3, 4)],
    ]
    names = [
        "Foundation", "Grid", "Matrix", "Lattice",
        "Mesh", "Web", "Net", "Raster",
        "Checker", "Tile", "Block", "Stone",
        "Brick", "Slab", "Panel", "Plate",
    ]
    levels = []
    for ri, rows in enumerate(rows_list):
        for si, types in enumerate(type_sets[ri]):
            def _make_fn(ts):
                return lambda r, c: ts[r % len(ts)]
            levels.append({
                "name": names[ri * len(type_sets[ri]) + si],
                "bricks": _build_grid(rows, 10, _make_fn(types)),
            })
    return levels


def _gen_checkers():
    names = [
        "Checkers", "Plaid", "Tartan", "Gingham", "Mosaic",
        "Patchwork", "Quilt", "Pixel", "Dice", "Houndstooth",
        "Tweed", "Argyle",
    ]
    configs = [
        (5, 10, 0, (1,)),
        (6, 10, 1, (2,)),
        (7, 10, 0, (3,)),
        (8, 10, 1, (1, 2)),
        (5, 10, 0, (2, 3)),
        (6, 10, 1, (3, 4)),
        (7, 10, 0, (4, 5)),
        (8, 10, 1, (1, 3)),
        (5, 10, 0, (2, 4)),
        (6, 10, 1, (3, 5)),
        (7, 10, 0, (1, 5)),
        (8, 10, 1, (2, 3, 4)),
    ]
    levels = []
    for i, (rows, cols, phase, types) in enumerate(configs):
        def _make_fn(ts, ph):
            return lambda r, c: ts[(r + c + ph) % len(ts)] if (r + c + ph) % 2 == 0 else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, phase)),
        })
    return levels


def _gen_stripes_h():
    names = [
        "Horizon", "Sunset", "Barcode", "Pinstripe",
        "Terrace", "Ribbon",
    ]
    configs = [
        (5, 10, 1, (1, 2)),
        (6, 10, 2, (2, 3)),
        (7, 10, 1, (3, 4)),
        (8, 10, 2, (4, 5)),
        (5, 10, 1, (1, 3)),
        (6, 10, 3, (2, 4)),
    ]
    levels = []
    for i, (rows, cols, thickness, types) in enumerate(configs):
        def _make_fn(ts, thick):
            return lambda r, c: ts[(r // thick) % len(ts)]
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, thickness)),
        })
    return levels


def _gen_stripes_v():
    names = [
        "Columns", "Pillars", "Palings", "Picket",
        "Vertical", "Upright",
    ]
    configs = [
        (5, 10, 1, (1, 2)),
        (6, 10, 2, (2, 3)),
        (7, 10, 3, (3, 4)),
        (8, 10, 1, (4, 5)),
        (5, 10, 2, (1, 3)),
        (6, 10, 1, (2, 4)),
    ]
    levels = []
    for i, (rows, cols, thickness, types) in enumerate(configs):
        def _make_fn(ts, thick):
            return lambda r, c: ts[(c // thick) % len(ts)]
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, thickness)),
        })
    return levels


def _gen_stripes_d():
    names = [
        "Diagonal", "Slant", "Rake", "Bevel",
        "Tilt", "Bias",
    ]
    configs = [
        (5, 10, 1, (1, 2)),
        (6, 10, 1, (2, 3)),
        (7, 10, 2, (3, 4)),
        (8, 10, 2, (4, 5)),
        (5, 10, 1, (1, 3)),
        (6, 10, 2, (2, 4)),
    ]
    levels = []
    for i, (rows, cols, thickness, types) in enumerate(configs):
        def _make_fn(ts, thick):
            return lambda r, c: ts[((r + c) // thick) % len(ts)]
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, thickness)),
        })
    return levels


def _gen_diamonds():
    names = [
        "Diamond", "Gem", "Crystal", "Jewel", "Rhombus",
        "Lozenge", "Sparkle", "Shine", "Prism", "Optic",
        "Facet", "Corundum",
    ]
    configs = [
        (5, 10, 0.4, (1, 2)),
        (5, 10, 0.5, (2, 3)),
        (6, 10, 0.35, (3, 4)),
        (6, 10, 0.45, (4, 5)),
        (7, 10, 0.4, (1, 3)),
        (7, 10, 0.5, (2, 4)),
        (8, 10, 0.35, (3, 5)),
        (8, 10, 0.45, (1, 4)),
        (5, 10, 0.55, (2, 5)),
        (6, 10, 0.4, (1, 2, 3)),
        (7, 10, 0.5, (2, 3, 4)),
        (8, 10, 0.4, (3, 4, 5)),
    ]
    levels = []
    for i, (rows, cols, size, types) in enumerate(configs):
        cx = cols / 2
        cy = rows / 2
        limit = min(rows, cols) * size
        def _make_fn(ts, cxv, cyv, lim):
            return lambda r, c: ts[(r + c) % len(ts)] if abs(r - cyv) + abs(c - cxv) <= lim else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, cx, cy, limit)),
        })
    return levels


def _gen_pyramids():
    names = [
        "Pyramid", "Ziggurat", "Temple", "Summit", "Apex",
        "Peak", "Cone", "Triangle", "Delta", "Wedge",
        "Gable", "Roof",
    ]
    configs = [
        (5, 10, 0, (1, 2)),
        (6, 10, 0, (2, 3)),
        (6, 10, 1, (3, 4)),
        (7, 10, 0, (4, 5)),
        (7, 10, 1, (1, 3)),
        (8, 10, 0, (2, 4)),
        (8, 10, 1, (3, 5)),
        (5, 10, 0, (1, 4)),
        (6, 10, 1, (2, 5)),
        (7, 10, 0, (1, 5)),
        (8, 10, 1, (2, 3, 4)),
        (8, 10, 0, (3, 4, 5)),
    ]
    levels = []
    for i, (rows, cols, invert, types) in enumerate(configs):
        def _make_fn(ts, inv):
            if inv:
                return lambda r, c: ts[r % len(ts)] if abs(c - 4.5) <= r else 0
            else:
                return lambda r, c: ts[r % len(ts)] if abs(c - 4.5) <= (rows - 1 - r) else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, invert)),
        })
    return levels


def _gen_frames():
    names = [
        "Frame", "Window", "Portal", "Gateway", "Hollow",
        "Ring", "Donut", "Torus", "Circle", "Aperture",
        "Void", "Cavern",
    ]
    configs = [
        (6, 10, 1, (1,)),
        (7, 10, 1, (2,)),
        (8, 10, 1, (3,)),
        (9, 10, 1, (4,)),
        (6, 10, 2, (5,)),
        (7, 10, 2, (1, 2)),
        (8, 10, 2, (2, 3)),
        (9, 10, 2, (3, 4)),
        (6, 10, 1, (4, 5)),
        (7, 10, 1, (1, 3)),
        (8, 10, 1, (2, 4)),
        (9, 10, 1, (3, 5)),
    ]
    levels = []
    for i, (rows, cols, thickness, types) in enumerate(configs):
        def _make_fn(ts, thick):
            return lambda r, c: (
                6 if (r < thick or r >= rows - thick or c < thick or c >= cols - thick)
                  and (r + c) % 5 < 2
                else ts[(r + c) % len(ts)] if thick < r < rows - thick - 1 and thick < c < cols - thick - 1 and (r + c) % 2 == 0
                else 0
            )
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, thickness)),
        })
    return levels


def _gen_waves():
    names = [
        "Wave", "Ripple", "Surge", "Undulate", "Sinusoid",
        "Oscillate", "Vibration", "Pulse", "Frequency", "Resonance",
        "Harmonic", "Tide", "Breaker", "Tsunami",
    ]
    configs = [
        (5, 10, 2, (1, 2)),
        (5, 10, 3, (2, 3)),
        (6, 10, 2, (3, 4)),
        (6, 10, 4, (4, 5)),
        (7, 10, 2, (1, 3)),
        (7, 10, 3, (2, 4)),
        (8, 10, 2, (3, 5)),
        (8, 10, 4, (1, 4)),
        (5, 10, 3, (2, 5)),
        (6, 10, 2, (1, 2, 3)),
        (7, 10, 3, (2, 3, 4)),
        (8, 10, 4, (3, 4, 5)),
        (6, 10, 3, (4, 1)),
        (7, 10, 2, (5, 2)),
    ]
    levels = []
    for i, (rows, cols, period, types) in enumerate(configs):
        def _make_fn(ts, per):
            return lambda r, c: ts[r % len(ts)] if (c + r * 2) % per != 0 and (c + r) % 3 != 1 else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, period)),
        })
    return levels


def _gen_targets():
    names = [
        "Target", "Bullseye", "Concentric", "Archery", "Ring",
        "Aim", "Crosshair", "Marksman", "Precision",
    ]
    configs = [
        (5, 10, 2, (1, 2)),
        (6, 10, 2, (2, 3)),
        (7, 10, 2, (3, 4)),
        (8, 10, 2, (4, 5)),
        (7, 10, 3, (1, 2, 3)),
        (8, 10, 3, (2, 3, 4)),
        (8, 10, 4, (3, 4, 5)),
        (5, 10, 2, (1, 5)),
        (6, 10, 3, (1, 3, 5)),
    ]
    levels = []
    for i, (rows, cols, rings, types) in enumerate(configs):
        cx = cols / 2
        cy = rows / 2
        def _make_fn(ts, cxv, cyv, rng):
            return lambda r, c: ts[min(int(abs(r - cyv) + abs(c - cxv)) % len(ts), len(ts) - 1)] if abs(r - cyv) + abs(c - cxv) < rng else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, cx, cy, rings)),
        })
    return levels


def _gen_scattered():
    names = [
        "Nebula", "Cosmos", "Stellar", "Galaxy", "Cluster",
        "Asterism", "Orion", "Andromeda", "Sirius", "Vega",
        "Rigel", "Polaris", "Comet", "Meteor",
    ]
    configs = [
        (5, 10, 3, (1,)),
        (5, 10, 4, (2,)),
        (6, 10, 3, (3,)),
        (6, 10, 4, (4,)),
        (7, 10, 3, (5,)),
        (7, 10, 4, (1, 2)),
        (8, 10, 3, (2, 3)),
        (8, 10, 4, (3, 4)),
        (9, 10, 3, (4, 5)),
        (9, 10, 4, (1, 3)),
        (8, 10, 3, (2, 4)),
        (5, 10, 4, (3, 5)),
        (6, 10, 5, (1, 4)),
        (7, 10, 5, (2, 5)),
    ]
    levels = []
    for i, (rows, cols, mod, types) in enumerate(configs):
        def _make_fn(ts, m):
            return lambda r, c: ts[(r * c) % len(ts)] if (r * c) % m != 0 and (r + c) % 3 != 1 else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, mod)),
        })
    return levels


def _gen_staggered():
    names = [
        "Brickwork", "Masonry", "Herringbone", "Stagger", "Offset",
        "Bond", "Flemish", "English", "Running", "Stack",
        "Weave", "Basket",
    ]
    configs = [
        (5, 10, 0, (1,)),
        (5, 10, 1, (2,)),
        (6, 10, 0, (3,)),
        (6, 10, 1, (4,)),
        (7, 10, 0, (5,)),
        (7, 10, 1, (1, 2)),
        (8, 10, 0, (2, 3)),
        (8, 10, 1, (3, 4)),
        (5, 10, 0, (4, 5)),
        (6, 10, 1, (1, 3)),
        (7, 10, 0, (2, 4)),
        (8, 10, 1, (3, 5)),
    ]
    levels = []
    for i, (rows, cols, shift, types) in enumerate(configs):
        def _make_fn(ts, sh):
            return lambda r, c: ts[r % len(ts)] if c >= (sh * r) % 2 else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, shift)),
        })
    return levels


def _gen_arrows():
    names = [
        "Arrow", "Compass", "Pointer", "Vector", "North",
        "Southpaw", "Eastward", "Westward", "Direction",
    ]
    configs = [
        (6, 10, "down", (1, 2)),
        (7, 10, "up", (2, 3)),
        (8, 10, "down", (3, 4)),
        (6, 10, "up", (4, 5)),
        (7, 10, "down", (1, 3)),
        (8, 10, "up", (2, 4)),
        (6, 10, "down", (3, 5)),
        (7, 10, "up", (1, 5)),
        (8, 10, "down", (2, 3, 4)),
    ]
    levels = []
    for i, (rows, cols, direction, types) in enumerate(configs):
        def _make_fn(ts, mid):
            return lambda r, c: ts[(r + c) % len(ts)] if abs(c - mid) <= r // 2 else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, cols / 2)),
        })
    return levels


def _gen_zigzags():
    names = [
        "Zigzag", "Lightning", "Zap", "Fork", "Serpentine",
        "Wiggle", "Slinky", "Switchback", "Meander",
    ]
    configs = [
        (5, 10, 2, (1, 2)),
        (5, 10, 3, (2, 3)),
        (6, 10, 2, (3, 4)),
        (6, 10, 3, (4, 5)),
        (7, 10, 2, (1, 3)),
        (7, 10, 3, (2, 4)),
        (8, 10, 2, (3, 5)),
        (8, 10, 3, (1, 4)),
        (5, 10, 2, (2, 5)),
    ]
    levels = []
    for i, (rows, cols, period, types) in enumerate(configs):
        def _make_fn(ts, per):
            return lambda r, c: ts[r % len(ts)] if c % (per * 2) < abs(per - r % (per * 2)) + 1 or c % (per * 2) >= per * 2 - abs(per - r % (per * 2)) - 1 else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, period)),
        })
    return levels


def _gen_borders():
    names = [
        "Border", "Edge", "Margin", "Rim", "Outline",
        "Perimeter", "Enclosure", "Fence", "Wall",
    ]
    configs = [
        (5, 10, 1, (1,)),
        (5, 10, 2, (2,)),
        (6, 10, 1, (3,)),
        (6, 10, 2, (4,)),
        (7, 10, 1, (5,)),
        (7, 10, 2, (1, 2)),
        (8, 10, 1, (2, 3)),
        (8, 10, 2, (3, 4)),
        (9, 10, 1, (4, 5)),
    ]
    levels = []
    for i, (rows, cols, depth, types) in enumerate(configs):
        def _make_fn(ts, dp):
            return lambda r, c: (
                6 if (r < dp or r >= rows - dp or c < dp or c >= cols - dp)
                  and (r + c) % 5 < 2
                else ts[(r + c) % len(ts)] if (r * c) % 4 != 0
                else 0
            )
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, depth)),
        })
    return levels


def _gen_crosses():
    names = [
        "Cross", "Crux", "Intersect", "Plus", "X Marks",
        "Crosshair", "Center", "Midpoint", "Centered",
    ]
    configs = [
        (5, 10, 1, (1,)),
        (6, 10, 1, (2,)),
        (7, 10, 1, (3,)),
        (8, 10, 1, (4,)),
        (5, 10, 2, (5,)),
        (6, 10, 2, (1, 2)),
        (7, 10, 2, (2, 3)),
        (8, 10, 2, (3, 4)),
        (9, 10, 1, (4, 5)),
    ]
    levels = []
    for i, (rows, cols, arm, types) in enumerate(configs):
        cr, cc = rows // 2, cols // 2
        def _make_fn(ts, crv, ccv, a):
            return lambda r, c: (
                6 if (r == crv and abs(c - ccv) <= a) or (c == ccv and abs(r - crv) <= a)
                else ts[(r + c) % len(ts)] if abs(r - crv) <= a and abs(c - ccv) <= a and (r + c) % 3 != 0
                else 0
            )
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, cr, cc, arm)),
        })
    return levels


def _gen_stairs():
    names = [
        "Stairs", "Steps", "Ascent", "Ladder", "Climb",
        "Rise", "Escalator", "Stepping", "Gradient",
    ]
    configs = [
        (7, 10, "up", (1,)),
        (8, 10, "down", (2,)),
        (7, 10, "up", (3,)),
        (8, 10, "down", (4,)),
        (7, 10, "up", (5,)),
        (8, 10, "down", (1, 2)),
        (7, 10, "up", (2, 3)),
        (8, 10, "down", (3, 4)),
        (7, 10, "up", (4, 5)),
    ]
    levels = []
    for i, (rows, cols, direction, types) in enumerate(configs):
        def _make_fn(ts, d):
            if d == "up":
                return lambda r, c: (
                    6 if c >= cols - 1 - r and c % 2 == 0
                    else ts[0] if c >= cols - 2 - r and c % 3 != 0
                    else 0
                )
            else:
                return lambda r, c: (
                    6 if c <= r and c % 2 == 0
                    else ts[0] if c <= r + 1 and c % 3 != 0
                    else 0
                )
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, direction)),
        })
    return levels


def _gen_hourglasses():
    names = [
        "Hourglass", "Infinity", "Loop", "Ouroboros", "Cycle",
        "Eternal", "Recurve", "Bilbo", "Waist",
    ]
    configs = [
        (6, 10, (1,)),
        (6, 10, (2,)),
        (7, 10, (3,)),
        (7, 10, (4,)),
        (8, 10, (5,)),
        (8, 10, (1, 2)),
        (6, 10, (2, 3)),
        (7, 10, (3, 4)),
        (8, 10, (4, 5)),
    ]
    levels = []
    for i, (rows, cols, types) in enumerate(configs):
        cx, cy = cols / 2, rows / 2
        def _make_fn(ts, cxv, cyv):
            return lambda r, c: ts[r % len(ts)] if abs(c - cxv) <= abs(r - cyv) else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, cx, cy)),
        })
    return levels


def _gen_wings():
    names = [
        "Butterfly", "Moth", "Wing", "Phoenix", "Angel",
        "Harpy", "Icarus", "Pegasus", "Griffin",
    ]
    configs = [
        (6, 10, (1,)),
        (6, 10, (2,)),
        (7, 10, (3,)),
        (7, 10, (4,)),
        (8, 10, (5,)),
        (8, 10, (1, 2)),
        (6, 10, (2, 3)),
        (7, 10, (3, 4)),
        (8, 10, (4, 5)),
    ]
    levels = []
    for i, (rows, cols, types) in enumerate(configs):
        cx = cols / 2
        def _make_fn(ts, cxv):
            return lambda r, c: ts[r % len(ts)] if c < cxv - abs(r - rows / 2) or c > cxv - 1 + abs(r - rows / 2) else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, cx)),
        })
    return levels


def _gen_forts():
    names = [
        "Fortress", "Castle", "Keep", "Citadel", "Bastion",
        "Rampart", "Redoubt", "Stronghold", "Bulwark",
    ]
    configs = [
        (7, 10, 1, 1, (1,)),
        (8, 10, 2, 2, (2,)),
        (9, 10, 2, 3, (3,)),
        (7, 10, 1, 2, (4,)),
        (8, 10, 2, 3, (5,)),
        (9, 10, 1, 2, (1, 2)),
        (7, 10, 2, 1, (2, 3)),
        (8, 10, 1, 3, (3, 4)),
        (9, 10, 2, 2, (4, 5)),
    ]
    levels = []
    for i, (rows, cols, t_top, t_sides, types) in enumerate(configs):
        def _make_fn(ts, tt, tsd):
            return lambda r, c: (
                6 if (r < tt or r >= rows - tt or c < tsd or c >= cols - tsd)
                  and (r + c) % 5 < 2
                else ts[(r + c) % len(ts)] if (r + c) % 3 != 0
                else 0
            )
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_fn(types, t_top, t_sides)),
        })
    return levels


def _gen_misc():
    names = [
        "Spiral", "Vortex", "Whirlpool", "Tornado", "Swirl",
        "Helix", "Coil", "Twist", "Eddy", "Maestro",
        "Crescendo", "Sonata", "Rhapsody", "Mirage", "Zenith",
        "Barricade", "Fortress II", "Stronghold", "Bulwark II",
    ]
    configs = [
        (7, 10, lambda r, c: (r + 1) % 5 + 1 if abs(c - 4.5) <= r % 4 else 0),
        (8, 10, lambda r, c: (c + 1) % 5 + 1 if r > 1 and r < 7 and c > 0 and c < 9 else 0),
        (6, 10, lambda r, c: (r * c) % 5 + 1 if (r + c) % 3 != 0 else 0),
        (8, 10, lambda r, c: (c + r * 2) % 5 + 1 if r % 3 != 1 else 0),
        (5, 10, lambda r, c: min(5, r + c + 1) if (r + c) % 4 < 3 else 0),
        (7, 10, lambda r, c: (r % 5) + 1 if c % 4 < (r % 3) + 1 else 0),
        (8, 10, lambda r, c: (r * c * 3) % 5 + 1 if (r * c) % 6 >= 2 else 0),
        (9, 10, lambda r, c: (r + 1) % 5 + 1 if abs(c - 4.5) > abs(r - 4) * 0.8 else 0),
        (6, 10, lambda r, c: (c % 5) + 1 if r < 2 or r >= 4 or (c % 4) < 2 else 0),
        (7, 10, lambda r, c: (r + c) % 5 + 1 if r > 1 and r < 6 else 0),
        (8, 10, lambda r, c: (c + 1) % 5 + 1 if r % 4 != c % 4 else 0),
        (5, 10, lambda r, c: (r + c) % 5 + 1 if r <= c else 0),
        (7, 10, lambda r, c: (r + 3) % 5 + 1 if r % 2 == c % 2 else 0),
        (8, 10, lambda r, c: (r + c * 2) % 5 + 1 if r >= c - 2 and r <= c + 2 else 0),
        (7, 10, lambda r, c: 6 if (r == 0 or r == 6) and (r + c) % 5 < 2 else (c % 4) + 1 if 0 < r < 6 and abs(c - 4.5) <= 3 and r % 2 != c % 2 else 0),
        (8, 10, lambda r, c: 6 if c == 0 or c == 9 else (r + 1) % 4 + 1 if 0 < c < 9 and (r + c) % 3 != 0 else 0),
        (9, 10, lambda r, c: 6 if (r == 0 or r == 8 or c == 0 or c == 9) and (r + c) % 5 < 2 else (r * c) % 5 + 1 if 0 < r < 8 and 0 < c < 9 and r % 3 != c % 3 else 0),
        (6, 10, lambda r, c: 6 if (c == 4 or c == 5) and r < 5 else (r + 2) % 4 + 1 if (c == 2 or c == 7) and r < 4 else 0),
    ]
    levels = []
    for i, (rows, cols, fn) in enumerate(configs):
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, fn),
        })
    return levels


def _gen_seeded():
    names = [
        "Prism", "Aurora", "Monolith", "Obelisk", "Cascade",
        "Fractal", "Mosaic", "Tessellate", "Filigree", "Mandrake",
        "Chimera", "Phantom", "Oracle", "Sphinx", "Golem",
        "Titan", "Colossus", "Behemoth", "Leviathan", "Juggernaut",
        "Sentinel", "Paladin", "Vanguard", "Champion", "Warden",
        "Seeker", "Nomad", "Voyager", "Pioneer", "Odyssey",
    ]
    configs = [
        (7, 10, 0),
        (8, 10, 1),
        (6, 10, 2),
        (9, 10, 3),
        (5, 10, 4),
        (7, 10, 5),
        (8, 10, 6),
        (6, 10, 7),
        (9, 10, 8),
        (5, 10, 9),
        (7, 10, 10),
        (8, 10, 11),
        (6, 10, 12),
        (9, 10, 13),
        (5, 10, 14),
        (7, 10, 15),
        (8, 10, 16),
        (6, 10, 17),
        (9, 10, 18),
        (5, 10, 19),
        (7, 10, 20),
        (8, 10, 21),
        (6, 10, 23),
        (5, 10, 22),
    ]
    levels = []
    for i, (rows, cols, seed) in enumerate(configs):
        rng = _rng(seed)
        cols_actual = 10
        offsets = [rng(0, 3) for _ in range(rows)]
        densities = [rng(3, 9) for _ in range(rows)]
        type_bases = [rng(1, 4) for _ in range(rows)]
        def _make_fn(offs, dens, bases, rng_state):
            return lambda r, c: bases[r] + ((r * c * 7 + rng_state * 3) % 3) if c >= offs[r] and c < offs[r] + dens[r] else 0
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols_actual, _make_fn(offsets, densities, type_bases, seed)),
        })
    return levels


def _rng(seed):
    state = seed
    def next_int(lo, hi):
        nonlocal state
        state = (state * 1103515245 + 12345) & 0x7fffffff
        return lo + (state % (hi - lo))
    return next_int


def _make_creative_fn(seed, mid):
    if seed == 0:
        return lambda r, c: 1 if abs(c - mid) <= 2 - r // 4 and r < 5 and (r != 4 or abs(c - mid) <= 1) else 0
    elif seed == 1:
        return lambda r, c: (r % 3) + 1 if (r < 2 and c > 1 and c < 8) or (r == 2 and c > 0 and c < 9) or (r > 2 and c > 1 and c < 8 and c % 3 != 1) else 0
    elif seed == 2:
        return lambda r, c: (r % 3) + 2 if c <= (r - 1) % 5 + 2 or c >= 9 - ((r - 1) % 5 + 2) else 0
    elif seed == 3:
        return lambda r, c: (r % 3) + 1 if abs(c - mid) <= (2 + (r * 7 + seed) % 3) and (r + c + seed) % 4 > 0 else 0
    elif seed == 4:
        return lambda r, c: (r % 3) + 1 if (abs(c - mid) <= 1 and 1 < r < 6) or (abs(c - mid) <= 3 and (r == 1 or r == 5)) or (abs(c - mid) <= 4 and (r == 2 or r == 4)) else 0
    elif seed == 5:
        return lambda r, c: (c % 3) + 2 if abs(c - mid) <= (4 - r % 2) or r % 3 == 0 else 0
    elif seed == 6:
        lim = [5, 4, 3, 2, 1, 0, 0, 0]
        return lambda r, c: (r + c) % 3 + 2 if abs(c - mid) <= (lim[r] if r < len(lim) else 0) else 0
    elif seed == 7:
        return lambda r, c: (r % 3) + 2 if abs(c - mid) <= min(r, 7 - r) else 0
    elif seed == 8:
        return lambda r, c: (r + c) % 4 + 1 if abs(c - mid) >= abs(r - 3.5) * 1.2 and abs(c - mid) <= 4 else 0
    elif seed == 9:
        return lambda r, c: (r % 3) + 1 if c >= abs(r - 3) and c <= 9 - abs(r - 3) else 0
    elif seed == 10:
        return lambda r, c: (r + c) % 3 + 2 if abs(c - mid) <= (3 - abs(r - 4) * 0.4) or (r + c) % 5 == 0 else 0
    elif seed == 11:
        return lambda r, c: (r % 3) + 2 if abs(c - mid) <= 2 + abs(r - 4) // 2 and (r + c + r // 2) % 3 != 0 else 0
    elif seed == 12:
        return lambda r, c: (r + c) % 4 + 1 if abs(c - mid) <= 2 + (3.5 - abs(r - 3.5)) // 2 else 0
    elif seed == 13:
        return lambda r, c: c % 4 + 1 if (r < 2 and c > 0 and c < 9) or (2 <= r < 5 and c > 1 and c < 8) or (r >= 5 and c > 2 and c < 7) else 0
    elif seed == 14:
        return lambda r, c: (r + c) % 4 + 1 if abs(c - mid) <= 4 - r // 2 and (r + c) % 3 > 0 else 0
    elif seed == 15:
        return lambda r, c: c % 4 + 1 if r % 2 == c % 2 and (r < 2 or r > 5 or abs(c - mid) > 1) else 0
    elif seed == 16:
        return lambda r, c: (r % 4) + 1 if abs(c - mid) > abs(r - 4) * 0.5 and abs(c - mid) < 5 - r * 0.2 else 0
    elif seed == 17:
        return lambda r, c: (r % 3) + 1 if (r + c) % 4 > 1 and abs(c - mid) <= 3 - r // 3 else 0
    elif seed == 18:
        return lambda r, c: (c % 4) + 1 if abs(c - mid) <= (7 - r) // 1.5 and r % 3 != c % 3 else 0
    elif seed == 19:
        return lambda r, c: (r % 3) + 1 if (r * c) % 6 > (r + c) % 4 else 0
    elif seed == 20:
        return lambda r, c: (c % 3) + 2 if abs(c - mid) <= 3 - (r % 3) else 0
    elif seed == 21:
        return lambda r, c: (r + c) % 4 + 1 if abs(c - mid) <= 3 and r > 0 and r < 7 else 0
    elif seed == 22:
        return lambda r, c: 6 if abs(c - mid) <= 1 and r < 6 else (r % 3) + 1 if abs(c - mid) <= 3 - r // 3 and r % 2 == 0 else 0
    elif seed == 23:
        return lambda r, c: 6 if (r == 0 or r == 7) and abs(c - mid) <= 4 else (c % 3) + 1 if 1 < r < 6 and abs(c - mid) <= 2 and (r + c) % 2 == 0 else 0
    elif seed == 24:
        return lambda r, c: 6 if r == 3 and abs(c - mid) <= 3 else (r + c) % 3 + 1 if abs(r - 3.5) + abs(c - mid) <= 5 and (r * c) % 3 != 0 else 0
    elif seed == 25:
        return lambda r, c: 6 if (c == 0 or c == 9 or c == 4 or c == 5) and r % 2 == 0 and r < 6 else (c % 4) + 1 if c > 1 and c < 8 and r < 5 else 0
    elif seed == 26:
        return lambda r, c: 6 if r == 2 and abs(c - mid) <= 3 else (r + 1) % 4 + 1 if (abs(c - mid) <= 2 - r // 4 or abs(c - mid) >= 5 - r // 2) and r < 7 and (r + c) % 3 != 0 else 0
    elif seed == 27:
        return lambda r, c: 6 if (r == 0 or r == 7) and c % 3 == 0 else (c % 3) + 2 if 1 < r < 6 and abs(c - mid) <= 2 + (r % 2) else 0
    elif seed == 28:
        return lambda r, c: 6 if abs(c - mid) <= 1 and r < 7 and r % 2 == 0 else (r % 4) + 1 if abs(c - mid) <= 4 - r // 2 and (r + c) % 4 > 1 else 0
    elif seed == 29:
        return lambda r, c: 6 if (r % 3 == 0 and c % 4 == 0) else (r * c) % 5 + 1 if abs(c - mid) <= 4 - r // 3 and (r + c) % 3 != 1 else 0
    else:
        return lambda r, c: (r % 3) + 1 if (r + c * r) % 5 > 1 and abs(c - mid) <= 4 else 0


def _gen_creative():
    names = [
        "Spaceship", "Castle", "Mountain", "Spiral", "Heart",
        "Sunburst", "Bulls Eye", "Pyramid II", "DNA", "Chevron",
        "Vortex", "Pinwheel", "Shield", "Crown", "Lantern",
        "Lattice", "Mask", "Monolith", "Starburst", "Fractal",
        "Obelisk", "Sentinel", "Citadel", "Wall Grid", "Diamond Wall",
        "Cross Wall", "Palisade", "Fortified", "Barbican", "Bunker",
    ]
    levels = []
    mid = 4.5
    for i in range(30):
        rows, cols = 8, 10
        levels.append({
            "name": names[i],
            "bricks": _build_grid(rows, cols, _make_creative_fn(i, mid)),
        })
    return levels


# Interleave generators so early levels have varied shapes
ITERLEAVE_ORDER = [
    _gen_grids, _gen_diamonds, _gen_checkers, _gen_pyramids,
    _gen_stripes_h, _gen_frames, _gen_stripes_v, _gen_waves,
    _gen_stripes_d, _gen_targets, _gen_scattered, _gen_staggered,
    _gen_arrows, _gen_zigzags, _gen_borders, _gen_crosses,
    _gen_stairs, _gen_hourglasses, _gen_wings, _gen_forts,
    _gen_misc, _gen_creative, _gen_seeded,
]
# Take one level at a time from each generator in round-robin order
iters = [iter(g()) for g in ITERLEAVE_ORDER]
done = [False] * len(iters)
while not all(done):
    for i, it in enumerate(iters):
        if done[i]:
            continue
        try:
            LEVELS.append(next(it))
        except StopIteration:
            done[i] = True

assert len(LEVELS) == 275, f"Expected 275 levels, got {len(LEVELS)}"
