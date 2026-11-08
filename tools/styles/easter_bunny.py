"""
Easter collection, Lopunny line (Buneary, Lopunny): "Easter Bunny".

* the brown fur becomes soft white bunny fur, with a faint lavender shadow so the shape reads
* the cream fluff becomes pastel-pink fluff; the existing pinks get rosier
* a few spring daisies tucked into the fur, and a painted-egg zigzag ribbon on the biggest area
* eyes as in the original
* shiny: a chocolate bunny: glossy milk-chocolate fur, white-chocolate fluff with dark drizzle,
  and a gold-foil trim
"""
from __future__ import annotations

import colorsys
import random

from PIL import Image

from . import _spring as S

EMISSIVE = "retexture"

FUR = [(0.0, (150, 140, 170)), (0.45, (222, 216, 236)), (1.0, (255, 254, 252))]
FLUFF = [(0.0, (206, 120, 150)), (0.5, (246, 178, 204)), (1.0, (255, 222, 234))]
FOIL = (232, 190, 60)

_cache: dict = {}


def _plan(base, eyes, seed, shiny):
    key = (S.digest(base), S.digest(eyes), seed, shiny)
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye = S.find_eye_mask(base, eyes)
    soft = S.value_noise(w, h, max(2, 2 * scale), rng)
    img = Image.new("RGBA", (w, h))
    px = img.load()
    fur = [[False] * w for _ in range(h)]
    fluff = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if eye[y][x]:
                c = (r, g, b)
            elif s > 0.35 and (hh > 0.9 or hh < 0.02) and l > 0.45:     # existing pinks (shiny fluff is pink)
                if shiny:
                    fluff[y][x] = True
                    c = S.ramp(S.WHITE_CHOC, 0.4 + 0.6 * l)
                else:
                    c = (240, 120, 160)
            elif l > 0.58 and 0.05 <= hh <= 0.2:                        # cream fluff
                fluff[y][x] = True
                c = S.ramp(S.WHITE_CHOC, 0.4 + 0.6 * l) if shiny else S.ramp(FLUFF, 0.3 + 0.7 * soft[y][x])
            else:                                                        # brown fur
                fur[y][x] = True
                c = S.chocolate(r, g, b, (soft[y][x] - 0.5) * 0.3) if shiny else \
                    S.ramp(FUR, 0.25 + l * 0.9 + (soft[y][x] - 0.5) * 0.2)
            px[x, y] = tuple(int(v) for v in c) + (a,)
    units = max(1, (w * h) // (64 * 64 * scale * scale))
    if shiny:
        # dark chocolate drizzle across the white chocolate, and a gold-foil trim along fur edges
        for y in range(h):
            for x in range(w):
                if fluff[y][x] and (x + 2 * (y // (2 * scale))) % (5 * scale) == 0:
                    px[x, y] = (60, 30, 14, alpha[y][x])
                if fur[y][x] and y + 1 < h and not alpha[y + 1][x] and rng.random() < 0.7:
                    px[x, y] = FOIL + (alpha[y][x],)
    else:
        big = S.islands(alpha, w, h, 150 * scale * scale)
        if big:
            S.zigzag_band(px, alpha, eye, max(big, key=len), scale, rng, (S.PAINTS[4], S.PAINTS[0]))
        S.daisies(px, alpha, eye, w, h, rng, scale, 4 * units, allowed=fur)
    _cache[key] = img
    return img


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":
        return base.convert("RGBA").copy()
    return _plan(base, eyes, seed, shiny).copy()
