"""
Christmas collection, Snorlax line (Munchlax, Snorlax): "Santa Claus".

* the dark body becomes Santa's red suit, shaded from the original so every fold still reads
* the belly becomes the front of the red coat, with a white fur trim down the middle, a black belt
  wrapped all the way round and a big gold buckle
* the other cream areas (face, paws, feet) become fluffy white fur: the beard and cuffs
* snow on top, eyes as in the original
* shiny: "Father Christmas", the old-world version in a deep green coat
"""
from __future__ import annotations

import colorsys
import random

from PIL import Image

from . import _festive as F

EMISSIVE = "retexture"

RED = [(0.0, (70, 6, 12)), (0.45, (168, 18, 28)), (1.0, (232, 64, 62))]
GREEN = [(0.0, (8, 40, 20)), (0.45, (22, 104, 52)), (1.0, (92, 176, 110))]
FUR = [(0.0, (186, 192, 204)), (0.6, (236, 238, 242)), (1.0, (255, 255, 255))]
BELT = (22, 18, 20)
BELT_EDGE = (64, 58, 60)

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
    coat = GREEN if shiny else RED
    fluff = F.value_noise(w, h, max(2, 2 * scale), rng)

    cream = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if a and not eye[y][x]:
                hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
                cream[y][x] = (0.05 <= hh <= 0.2 and l > 0.55) or l > 0.85
    groups = F.components([(x, y) for y in range(h) for x in range(w) if cream[y][x]])

    def solid(g):   # the belly is a compact, filled blob; faces and decals are long or ragged
        xs, ys = [p[0] for p in g], [p[1] for p in g]
        bw, bh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
        return len(g) / (bw * bh) > 0.75 and min(bw, bh) >= 10 and max(bw, bh) <= 2.2 * min(bw, bh)

    candidates = [g for g in groups if solid(g)] or groups
    belly = set(max(candidates, key=len)) if candidates else set()

    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[1]
            if eye[y][x]:
                c = (r, g, b)
            elif (x, y) in belly:
                c = _ramp(coat, 0.35 + l * 0.6)            # the coat front
            elif cream[y][x]:
                c = _ramp(FUR, 0.45 + fluff[y][x] * 0.55)  # beard, cuffs
            else:
                c = _ramp(coat, l * 1.5)                   # the suit
            px[x, y] = tuple(int(v) for v in c) + (a,)

    if belly:
        xs = [p[0] for p in belly]
        ys = [p[1] for p in belly]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        cx = (bx0 + bx1) // 2
        # white fur trim down the middle of the coat
        for y in range(by0, by1 + 1):
            for x in range(cx - 2 * scale, cx + 2 * scale):
                if (x, y) in belly:
                    px[x, y] = _ramp(FUR, 0.5 + fluff[y][x] * 0.5) + (alpha[y][x],)
        # belt: wraps round the whole painted area at waist height (box UV puts the sides next to the front)
        thick = max(3, round((by1 - by0) * 0.14))
        belt_y = by0 + int((by1 - by0) * 0.62)
        for y in range(belt_y, belt_y + thick):
            if not (0 <= y < h):
                continue
            x = cx
            while x > 0 and alpha[y][x - 1]:
                x -= 1
            while x < w and alpha[y][x]:
                if not eye[y][x]:
                    edge = y in (belt_y, belt_y + thick - 1)
                    px[x, y] = (BELT_EDGE if edge else BELT) + (alpha[y][x],)
                x += 1
        # gold buckle, sized to the belly
        bw = max(5, round((bx1 - bx0) * 0.28)) | 1
        bh = thick + 2
        rim = max(1, bh // 5)
        x0, y0 = cx - bw // 2, belt_y - 1
        for y in range(y0, y0 + bh):
            for x in range(x0, x0 + bw):
                if 0 <= x < w and 0 <= y < h and alpha[y][x] and not eye[y][x]:
                    inner = x0 + rim <= x < x0 + bw - rim and y0 + rim <= y < y0 + bh - rim
                    px[x, y] = (BELT if inner else F.GOLD if (x + y) % 3 else F.GOLD_DARK) + (alpha[y][x],)
    F.snow_cap(px, alpha, eye, w, h, rng, scale)
    _cache[key] = img
    return img


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":
        return base.convert("RGBA").copy()
    return _plan(base, eyes, seed, shiny).copy()
