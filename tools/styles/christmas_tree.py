"""
Christmas collection, Turtwig line (Turtwig, Grotle, Torterra): "Christmas Tree".

* every green part (leaves, sprouts, Torterra's tree and bushes) becomes a dark pine Christmas tree
  with needle texture
* hung with baubles (red, gold, blue, silver, each with a shine) and wavy gold tinsel
* strings of fairy lights wind through the green; they glow and twinkle (extra emissive layer)
* snow settles on top of the branches; the rest of the body (shell, skin) keeps its colours
* shiny: a "flocked" white-frosted tree with gold and red decorations
"""
from __future__ import annotations

import colorsys
import math
import random

from PIL import Image

from . import _festive as F

EMISSIVE = "retexture"
EXTRA_LAYERS = [F.LIGHTS]

PINE = [(0.0, (6, 34, 18)), (0.5, (18, 84, 42)), (1.0, (64, 140, 76))]
FLOCKED = [(0.0, (120, 150, 132)), (0.5, (196, 216, 204)), (1.0, (246, 250, 248))]
BAUBLES = [(214, 24, 36), (236, 184, 44), (40, 90, 220), (200, 206, 216), (170, 30, 140)]
TINSEL = [(255, 214, 80), (214, 156, 30)]

_cache: dict = {}


def _ramp(stops, v):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            return F.mix(c0, c1, (v - p0) / (p1 - p0))
    return stops[-1][1]


def _plan(base, eyes, seed, shiny):
    key = (F.digest(base), F.digest(eyes), seed, shiny)
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye = F.find_eye_mask(base, eyes)
    needles = F.value_noise(w, h, max(1, scale), rng)
    tree = [[False] * w for _ in range(h)]
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if not eye[y][x] and 0.17 <= hh <= 0.47 and s > 0.18 and l > 0.08:
                tree[y][x] = True
                c = _ramp(FLOCKED if shiny else PINE, l * 0.9 + (needles[y][x] - 0.5) * 0.35)
            else:
                c = (r, g, b)
            px[x, y] = tuple(int(v) for v in c) + (a,)

    on_tree = lambda x, y: 0 <= x < w and 0 <= y < h and tree[y][x]
    # wavy gold tinsel across each tree area
    for island in F.components([(x, y) for y in range(h) for x in range(w) if tree[y][x]]):
        xs, ys = [p[0] for p in island], [p[1] for p in island]
        if max(xs) - min(xs) < 8 * scale or max(ys) - min(ys) < 6 * scale:
            continue
        for k in range(1 + (max(ys) - min(ys)) // (14 * scale)):
            y_base = min(ys) + (k + 0.5) * (max(ys) - min(ys)) / (1 + (max(ys) - min(ys)) // (14 * scale))
            for x in range(min(xs), max(xs) + 1):
                y = int(y_base + 1.5 * scale * math.sin(x / (3.0 * scale)))
                if on_tree(x, y):
                    px[x, y] = TINSEL[(x // scale) % 2] + (alpha[y][x],)
    # baubles, each with a little shine
    count = sum(row.count(True) for row in tree) // (30 * scale * scale)
    colours = [(218, 184, 52), (200, 30, 40)] if shiny else BAUBLES
    for _ in range(count):
        r = scale if rng.random() < 0.6 else int(1.5 * scale)
        x, y = rng.randrange(w), rng.randrange(h)
        cells = [(x + dx, y + dy) for dy in range(-r, r + 1) for dx in range(-r, r + 1) if dx * dx + dy * dy <= r * r + 1]
        if all(on_tree(cx, cy) for cx, cy in cells):
            col = rng.choice(colours)
            for cx, cy in cells:
                px[cx, cy] = col + (alpha[cy][cx],)
            px[x - r // 2, y - r // 2] = (255, 255, 255, alpha[y - r // 2][x - r // 2])
            for cx, cy in cells:
                tree[cy][cx] = False   # no light bulb on top of a bauble
    F.snow_cap(px, alpha, eye, w, h, rng, scale, allowed=tree)
    wire, bulbs = F.plan_garlands(alpha, eye, w, h, rng, scale, allowed=tree, per_island=2)
    F.paint_garlands(px, alpha, wire, bulbs, scale)
    _cache[key] = (img, alpha, bulbs, scale)
    return _cache[key]


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":
        return base.convert("RGBA").copy()
    return _plan(base, eyes, seed, shiny)[0].copy()


def extra_layer(name, base, eyes, seed, shiny, frame):
    img, alpha, bulbs, scale = _plan(base, eyes, seed, shiny)
    return F.lights_layer(img.size, alpha, bulbs, frame, scale) if bulbs else None
