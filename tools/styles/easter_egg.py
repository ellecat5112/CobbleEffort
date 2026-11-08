"""
Easter collection, Togepi line (Togepi, Togetic, Togekiss): "Easter Egg".

* the white shell / body becomes a hand-painted Easter egg: pastel bands of solid colour, zigzags,
  polka dots and white pin-stripes running round it, still shaded so the shape reads
* Togepi's red and blue triangles stay, repainted as bright raspberry and periwinkle so they look like
  part of the decoration
* everything else (face, arms, wings' undersides) goes pastel; eyes as in the original
* shiny: a golden Fabergé egg, gold bands set with ruby, sapphire, emerald and pearl
"""
from __future__ import annotations

import colorsys
import random

from PIL import Image

from . import _spring as S

EMISSIVE = "retexture"

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
    band_h = 3 * scale
    bands = S.make_bands(rng, 8)
    img = Image.new("RGBA", (w, h))
    px = img.load()
    shell = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            shade = 0.78 + 0.25 * l
            if eye[y][x]:
                c = (r, g, b)
            elif l > 0.8 or (l > 0.66 and s < 0.35):            # the white shell / body (incl. bluish whites)
                shell[y][x] = True
                if shiny:
                    fy = y % band_h
                    c = S.ramp(S.GOLD, 0.45 + 0.5 * l - (0.25 if fy == 0 else 0))
                else:
                    c = tuple(min(255, v * shade) for v in S.egg_pattern(x, y, 0, band_h, scale, bands))
            elif s > 0.4 and (hh < 0.05 or hh > 0.93):           # red triangles
                c = (214, 160, 40) if shiny else (226, 60, 120)
            elif s > 0.35 and 0.5 < hh < 0.72:                   # blue triangles
                c = (150, 20, 50) if shiny else (100, 120, 236)
            else:
                c = S.ramp(S.GOLD, l * 0.8) if shiny else S.pastel(r, g, b)
            px[x, y] = tuple(int(v) for v in c) + (a,)
    if shiny:   # jewels set along the gold bands
        for y in range(0, h, band_h * 2):
            for x in range(rng.randrange(2 * scale), w, 4 * scale):
                if all(0 <= x + sx < w and 0 <= y + sy < h and shell[y + sy][x + sx]
                       for sy in range(scale) for sx in range(scale)):
                    c = S.JEWELS[(x // (4 * scale) + y // band_h) % len(S.JEWELS)]
                    for sy in range(scale):
                        for sx in range(scale):
                            px[x + sx, y + sy] = c + (alpha[y + sy][x + sx],)
    _cache[key] = img
    return img


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":
        return base.convert("RGBA").copy()
    return _plan(base, eyes, seed, shiny).copy()
