"""
Backrooms collection look: "Still Lifes" from Kane Pixels' Backrooms.

A Still Life is an imperfect copy that the Backrooms rebuilds from memory. It looks moulded and
assembled, with a sallow plaster/clay finish, drained colour, damp stains, seams, slipped rows,
and matte painted-on eyes with a misplaced second set and a smear running down.
"""
from __future__ import annotations

import colorsys
import random

from PIL import Image

# Still Lifes do not glow: emissive layers are switched off.
EMISSIVE = "disable"

# Level 0 / Still Life palette: dark umber -> wet clay -> sallow plaster -> fluorescent-lit highlight
PALETTE = [
    (0.00, (34, 28, 18)),
    (0.25, (88, 72, 46)),
    (0.50, (150, 128, 86)),
    (0.75, (201, 183, 128)),
    (1.00, (236, 226, 178)),
]
EYE_COLOUR = (22, 17, 11)  # flat, matte, "painted-on" eyes


def lerp(a, b, t):
    return a + (b - a) * t


def palette_lookup(lum: float):
    lum = max(0.0, min(1.0, lum))
    for (p0, c0), (p1, c1) in zip(PALETTE, PALETTE[1:]):
        if lum <= p1:
            t = (lum - p0) / (p1 - p0) if p1 > p0 else 0
            return tuple(lerp(c0[i], c1[i], t) for i in range(3))
    return PALETTE[-1][1]


def value_noise(w: int, h: int, cell: int, rng: random.Random):
    """Cheap smooth value noise (bilinear), values 0..1."""
    gw, gh = w // cell + 2, h // cell + 2
    grid = [[rng.random() for _ in range(gw)] for _ in range(gh)]
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        gy, fy = divmod(y / cell, 1)
        gy = int(gy)
        for x in range(w):
            gx, fx = divmod(x / cell, 1)
            gx = int(gx)
            a = lerp(grid[gy][gx], grid[gy][gx + 1], fx)
            b = lerp(grid[gy + 1][gx], grid[gy + 1][gx + 1], fx)
            out[y][x] = lerp(a, b, fy)
    return out


def retexture(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool,
              frame: int = 0, layer: bool = False) -> Image.Image:
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)  # textures are 64..256 px; keep features proportional

    eye_mask = [[False] * w for _ in range(h)]
    if eyes is not None:
        e = eyes.convert("RGBA").resize((w, h), Image.NEAREST).load()
        for y in range(h):
            for x in range(w):
                if e[x, y][3] > 0 and src[x, y][3] > 0:
                    eye_mask[y][x] = True

    stains = value_noise(w, h, max(4, 6 * scale), rng)      # damp blotches
    fold = value_noise(w, h, max(8, 14 * scale), rng)       # big "pressed by hand" undulation
    out = Image.new("RGBA", (w, h))
    o = out.load()

    # 1. drain colour and map onto the plaster/clay palette, keep a ghost of the original hue
    ghost = 0.30 if shiny else 0.18
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a == 0:
                o[x, y] = (0, 0, 0, 0)
                continue
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            lum = 0.18 + lum * 0.74                         # flatten contrast: everything looks moulded
            lum += (fold[y][x] - 0.5) * 0.10
            lum -= max(0.0, stains[y][x] - 0.62) * 0.55     # water damage
            lum += rng.uniform(-0.035, 0.035)               # clay grain
            pr, pg, pb = palette_lookup(lum)
            hh, ll, ss = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            gr, gg, gb = colorsys.hls_to_rgb(hh, max(0.2, min(0.8, lum)), ss * 0.6)
            o[x, y] = (
                int(lerp(pr, gr * 255, ghost)),
                int(lerp(pg, gg * 255, ghost)),
                int(lerp(pb, gb * 255, ghost)),
                a,
            )

    # 2. the "copied from memory" mistake: a few rows slip sideways, like a bad scan
    for _ in range(rng.randint(2, 4) * scale):
        y0 = rng.randrange(h)
        shift = rng.choice((-1, 1)) * scale
        band = rng.randint(1, 2) * scale
        rows = {}
        for y in range(y0, min(h, y0 + band)):
            rows[y] = [o[x, y] for x in range(w)]
        for y, row in rows.items():
            for x in range(w):
                sx = x - shift
                if 0 <= sx < w and row[sx][3] > 0 and src[x, y][3] > 0:
                    o[x, y] = row[sx][:3] + (src[x, y][3],)

    # 3. seams: thin darker lines where the pieces were pressed together
    for _ in range(rng.randint(2, 3)):
        horizontal = rng.random() < 0.5
        pos = rng.randrange(h if horizontal else w)
        length = rng.randint(w // 6, w // 2) if horizontal else rng.randint(h // 6, h // 2)
        start = rng.randrange((w if horizontal else h))
        wobble = 0
        for i in range(length):
            wobble += rng.choice((-1, 0, 0, 0, 1))
            x, y = (start + i, pos + wobble) if horizontal else (pos + wobble, start + i)
            if 0 <= x < w and 0 <= y < h and o[x, y][3] > 0 and not eye_mask[y][x]:
                r, g, b, a = o[x, y]
                o[x, y] = (int(r * 0.62), int(g * 0.60), int(b * 0.55), a)

    # 4. features: matte painted eyes, a duplicated set just below, and a smear dragging down
    if any(any(row) for row in eye_mask):
        coords = [(x, y) for y in range(h) for x in range(w) if eye_mask[y][x]]
        ys = [c[1] for c in coords]
        eye_h = max(1, max(ys) - min(ys) + 1)
        eye_h = min(eye_h, 4 * scale)
        dup_dy = eye_h + scale
        smear_len = rng.randint(2, 4) * scale
        for x, y in coords:
            o[x, y] = EYE_COLOUR + (src[x, y][3],)
        for x, y in coords:
            # second, slightly misplaced set of eyes
            dx = rng.choice((0, 0, scale if x % 2 else -scale))
            nx, ny = x + dx, y + dup_dy
            if 0 <= nx < w and 0 <= ny < h and o[nx, ny][3] > 0 and not eye_mask[ny][nx]:
                r, g, b, a = o[nx, ny]
                o[nx, ny] = (int(lerp(r, EYE_COLOUR[0], 0.8)), int(lerp(g, EYE_COLOUR[1], 0.8)),
                             int(lerp(b, EYE_COLOUR[2], 0.8)), a)
            # the smear: features run downwards like wet clay
            for i in range(1, smear_len + 1):
                sy = y + i
                if sy >= h or o[x, sy][3] == 0 or eye_mask[sy][x]:
                    break
                t = 0.55 * (1 - i / (smear_len + 1))
                r, g, b, a = o[x, sy]
                o[x, sy] = (int(lerp(r, EYE_COLOUR[0], t)), int(lerp(g, EYE_COLOUR[1], t)),
                            int(lerp(b, EYE_COLOUR[2], t)), a)

    # 5. fluorescent cast: Level 0's mono-yellow light
    for y in range(h):
        for x in range(w):
            r, g, b, a = o[x, y]
            if a:
                o[x, y] = (min(255, int(r * 1.03 + 4)), min(255, int(g * 1.01 + 3)), int(b * 0.90), a)
    return out
