"""
Christmas collection, Trubbish line (Trubbish, Garbodor): "Christmas Gift".

* the whole body is wrapped in candy-stripe gift paper (red with white diagonal stripes), still shaded
  from the original so the shape reads
* every big wrapped area gets a green satin ribbon tied crosswise, the biggest one a ribbon bow on top,
  and there's a little white gift tag on a string
* eyes as in the original, so it's still a Trubbish peeking out of the wrapping
* shiny: gold foil paper with a red ribbon
"""
from __future__ import annotations

import colorsys
import random

from PIL import Image

from . import _festive as F

EMISSIVE = "retexture"

PAPER = ((198, 22, 34), (250, 244, 240))       # red, white stripe
PAPER_SHINY = ((214, 166, 42), (250, 226, 132))  # gold foil
RIBBON = ((24, 128, 58), (12, 74, 32))           # satin green, edge
RIBBON_SHINY = ((200, 24, 36), (110, 8, 16))

_cache: dict = {}


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
    paper, stripe = PAPER_SHINY if shiny else PAPER
    ribbon, ribbon_edge = RIBBON_SHINY if shiny else RIBBON
    img = Image.new("RGBA", (w, h))
    px = img.load()
    period = 6 * scale
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            if eye[y][x]:
                px[x, y] = (r, g, b, a)
                continue
            l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[1]
            shade = 0.72 + 0.45 * l
            c = stripe if (x + y) % period < 2 * scale else paper
            px[x, y] = tuple(int(min(255, v * shade)) for v in c) + (a,)

    def band(x, y):
        if 0 <= x < w and 0 <= y < h and alpha[y][x] and not eye[y][x]:
            px[x, y] = ribbon + (alpha[y][x],)

    islands = [i for i in F.components([(x, y) for y in range(h) for x in range(w) if alpha[y][x]])
               if len(i) > 80 * scale * scale]
    islands.sort(key=len, reverse=True)
    for n, island in enumerate(islands):
        xs, ys = [p[0] for p in island], [p[1] for p in island]
        cx, cy = (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2
        inside = set(island)
        rw = 3 * scale
        for (x, y) in island:
            if abs(x - cx) < rw // 2 + scale or abs(y - cy) < rw // 2 + scale:
                edge = abs(x - cx) == rw // 2 + scale - 1 and abs(y - cy) >= rw // 2 + scale or \
                       abs(y - cy) == rw // 2 + scale - 1 and abs(x - cx) >= rw // 2 + scale
                if not eye[y][x]:
                    px[x, y] = (ribbon_edge if edge else ribbon) + (alpha[y][x],)
        if n == 0:
            # bow: two loops and two tails around the knot
            for dy in range(-3 * scale, 3 * scale + 1):
                for dx in range(-6 * scale, 6 * scale + 1):
                    loop = ((abs(dx) - 3 * scale) / (3 * scale)) ** 2 + (dy / (2.2 * scale)) ** 2
                    x, y = cx + dx, cy + dy
                    if (x, y) in inside and not eye[y][x]:
                        if 0.55 < loop <= 1.0:
                            px[x, y] = ribbon_edge + (alpha[y][x],)
                        elif loop <= 0.55 or (abs(dx) <= scale and abs(dy) <= scale):
                            px[x, y] = ribbon + (alpha[y][x],)
            # gift tag on a string, off to one side
            tx, ty = min(xs) + 2 * scale, min(ys) + 2 * scale
            for y in range(ty, ty + 4 * scale):
                for x in range(tx, tx + 6 * scale):
                    if (x, y) in inside and not eye[y][x]:
                        px[x, y] = ((250, 248, 236) if x > tx and y > ty else (150, 140, 120)) + (alpha[y][x],)
            for k in range(tx + 6 * scale, min(cx, tx + 14 * scale)):
                y = ty + 2 * scale + (k - tx) // (4 * scale)
                if (k, y) in inside:
                    px[k, y] = (200, 30, 40, alpha[y][k])
    F.snow_cap(px, alpha, eye, w, h, rng, scale)
    _cache[key] = img
    return img


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":
        return base.convert("RGBA").copy()
    return _plan(base, eyes, seed, shiny).copy()
