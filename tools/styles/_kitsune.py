"""
Kitsune collection: Pokemon as fox spirits of shrine and legend.

Looks (one per line, three lines each):
  inari      a white shrine fox: snowy fur with vermilion markings and warm orange foxfire at the tips
  kitsunebi  dark indigo fur haunted by drifting blue-white foxfire wisps; blue fire at the tips
  nogitsune  the wild fox: black fur with gold markings and violet flames at the tips
  tenko      the celestial fox: pale gold fur fading to sky blue at the tips, dusted with stars
  shrine     vermilion lacquer over black, a straw shimenawa rope round the body hung with white paper shide
  autumn     russet-orange fur scattered with red and gold maple leaves, ember-red fire at the tips
Every look: kitsune mask markings on the face (a forehead flame and swept cheek stripes), glowing eyes, the topmost
parts (ears, tails, crests) burning with foxfire, and an emissive animated layer (FOXFIRE) where the fire flickers.
Shiny: the foxfire turned round the colour wheel.
"""
from __future__ import annotations

import math

import numpy as np

from ._arc import dilate
from ._cosmic import even, hue_turn_fast, noise, ramp
from ._fx import make as _make

FOXFIRE = {"name": "foxfire", "emissive": True, "translucent": True, "frames": 4, "fps": 6}

LOOKS = {   # look -> (fur stops, marking colour, foxfire colour)
    "inari": ([(196, 190, 196), (232, 228, 230), (252, 250, 246)], (206, 30, 36), (255, 160, 70)),
    "kitsunebi": ([(12, 12, 34), (36, 38, 78), (76, 82, 130)], (120, 200, 255), (150, 220, 255)),
    "nogitsune": ([(8, 6, 8), (30, 24, 28), (64, 54, 58)], (232, 182, 60), (180, 80, 255)),
    "tenko": ([(214, 190, 128), (242, 226, 182), (255, 250, 230)], (210, 60, 50), (210, 240, 255)),
    "shrine": ([(140, 26, 18), (204, 56, 36), (238, 104, 74)], (252, 250, 240), (255, 200, 90)),
    "autumn": ([(130, 52, 18), (206, 100, 36), (246, 164, 84)], (110, 20, 14), (255, 90, 40)),
}


def _area(c):
    return max(1.0, c.alpha.sum() / float(c.u * c.u))


def segment(c, x1, y1, x2, y2, width):
    L = max(1e-6, math.hypot(x2 - x1, y2 - y1))
    t = np.clip(((c.xx - x1) * (x2 - x1) + (c.yy - y1) * (y2 - y1)) / (L * L), 0, 1)
    return np.hypot(c.xx - (x1 + t * (x2 - x1)), c.yy - (y1 + t * (y2 - y1))) <= width


def face_marks(c):
    """Kitsune mask markings on the face's front: a flame on the forehead and two swept stripes on each cheek."""
    m = np.zeros_like(c.alpha)
    if not (c.face.ok and c.face.front):
        return m
    x, y, w, h = c.face.front
    lw = max(0.6, c.u * 0.45)
    cx = x + w / 2
    fy = y + h * 0.16
    r = max(1.0, min(w, h) * 0.1)
    d = np.hypot((c.xx - cx) / r, (c.yy - fy) / (r * 1.8))                       # forehead flame: a teardrop
    m |= (d <= 1) & (c.yy >= fy - r * 1.8 + (np.abs(c.xx - cx) / r) * r)
    for sx in (-1, 1):
        ex = cx + sx * w * 0.32
        for k in (0, 1):
            y0 = y + h * (0.55 + 0.14 * k)
            m |= segment(c, ex, y0, ex + sx * w * 0.2, y0 - h * 0.12, lw)
    rect = (c.xx >= x) & (c.xx < x + w) & (c.yy >= y) & (c.yy < y + h)
    return m & rect & c.alpha & ~c.eye


def paint(look, c):
    rng, u = c.rng, c.u
    mottle = noise(c.h, c.w, 5 * u, rng, 2)
    fine = noise(c.h, c.w, max(1, u), rng, 1)
    turn = 0.45 if c.shiny else 0.0
    col = lambda rgb: hue_turn_fast(np.array(rgb, np.float32)[None, None], turn)[0, 0] if turn else np.array(rgb, np.float32)
    stops, mark_c, fire_c = LOOKS[look]
    fire = col(fire_c)
    body = c.alpha & ~c.eye
    fur = (np.abs(np.sin(c.xx / (1.3 * u) + mottle * 5)) < 0.25) & body             # combed fur strokes
    rgb = ramp(even(stops), c.lum * 0.5 + mottle * 0.4)
    rgb = np.where(fur[..., None], rgb * 0.9, rgb)
    if look == "tenko":
        sky = np.clip((c.hm - 0.65) / 0.3, 0, 1)[..., None]
        rgb = rgb * (1 - sky) + col((120, 186, 255)) * sky
        stars = (rng.random((c.h, c.w)) < 0.01) & body
        rgb = np.where(stars[..., None], np.array([255, 255, 255], np.float32), rgb)
        c.shine(stars, (255, 255, 255), 0.7)
    elif look == "shrine":
        low = (c.hm < 0.25 + 0.03 * mottle) & body
        rgb = np.where(low[..., None], np.array([22, 16, 16], np.float32) + 30 * c.lum[..., None], rgb)
        rope = (np.abs(c.hm - 0.55) < 0.035) & body
        twist = ((c.xx + (c.hm * 200)) // max(1, u)) % 3 == 0
        rgb = np.where(rope[..., None], np.where(twist[..., None], np.array([170, 140, 80], np.float32),
                                                 np.array([226, 204, 140], np.float32)), rgb)
        cell = 7 * u                                                               # paper shide hanging below the rope
        zz = ((c.xx % cell) < 2 * u) & (c.hm < 0.515) & (c.hm > 0.44)
        zig = ((np.floor((0.515 - c.hm) * 60) % 2) == 0)
        shide = zz & ((c.xx % cell) < np.where(zig, u, 2 * u)) & body
        rgb = np.where(shide[..., None], np.array([250, 250, 246], np.float32), rgb)
    elif look == "autumn":
        leaves = np.zeros_like(c.alpha)
        ys, xs = np.nonzero(body)
        for i in range(max(3, int(_area(c) / 110))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            lx, ly, R = float(xs[k]), float(ys[k]), rng.uniform(1.2, 2.0) * u
            r = np.hypot(c.xx - lx, c.yy - ly)
            th = np.arctan2(c.yy - ly, c.xx - lx)
            leaf = (r <= R * (0.55 + 0.45 * np.abs(np.cos(2.5 * th)))) & body
            rgb = np.where(leaf[..., None], np.array([200, 30, 24] if i % 2 else [236, 170, 40], np.float32), rgb)
            leaves |= leaf
    elif look == "kitsunebi":
        wisps = []
        ys, xs = np.nonzero(body)
        for _ in range(max(2, int(_area(c) / 160))):
            if len(xs) == 0:
                break
            k = rng.integers(len(xs))
            wisps.append((float(xs[k]), float(ys[k]), rng.uniform(0.9, 1.5) * u))
        c.extra["wisps"] = wisps
    marks = face_marks(c)
    rgb = np.where(marks[..., None], col(mark_c) if look != "shrine" else np.asarray(mark_c, np.float32), rgb)
    tips = (c.hm > 0.86 + 0.05 * fine) & body                                      # foxfire at the tips
    heat = np.clip((c.hm - 0.86) / 0.14, 0, 1)[..., None]
    rgb = np.where(tips[..., None], rgb * (1 - heat) + (fire * 0.6 + 255 * 0.4) * heat, rgb)
    c.shine(tips, fire, 0.85)
    if look in ("kitsunebi", "nogitsune", "tenko"):
        c.shine(marks, col(mark_c), 0.6)
    rgb = np.where(c.eye[..., None], fire, rgb)
    c.shine(c.eye, fire, 1.0)
    c.extra["tips"], c.extra["fire"] = tips, fire
    c.extra["static"] = (c.glow.copy(), c.glow_rgb.copy())
    return rgb


def animate(glow, frame, c):
    g0, rgb0 = c.extra["static"]
    g, grgb = g0.copy(), rgb0.copy()
    rng = np.random.default_rng((c.seed * 2477 + frame * 613) % (2 ** 32))
    flick = noise(c.h, c.w, max(1, c.u * 2), rng, 1)
    g = np.where(c.extra["tips"], g0 * (0.55 + 0.45 * flick), g)
    for wx, wy, r in c.extra.get("wisps", []):                                    # foxfire wisps drift upward
        oy = wy - frame * c.u * 0.8
        d = np.hypot((c.xx - wx) / r, (c.yy - oy) / (r * 1.6))
        m = (d <= 1) & c.alpha & ~c.eye
        g = np.where(m, np.maximum(g, 1.0 - 0.5 * d), g)
        grgb = np.where(m[..., None], c.extra["fire"] * (1 - 0.4 * d[..., None]) + 255 * 0.4 * (1 - d[..., None]), grgb)
    c.glow_rgb = grgb
    return g


def make(look):
    return _make(paint, look, animate, paint_layers=True)
