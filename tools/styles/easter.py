"""
Easter collection look: "Pastel" (the 16 random lines).

* every colour becomes its soft pastel version (same hue, lighter and gentler), so each Pokémon still
  looks like itself, just springtime
* each big painted area gets a hand-painted zigzag ribbon, like the decoration round an Easter egg
* little spring daisies (white petals, yellow hearts) dotted about
* eyes keep their original colours
* shiny: "chocolate": glossy milk chocolate with rainbow candy sprinkles
* glowing (emissive) parts keep glowing, in pastel
"""
from __future__ import annotations

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
    gloss = S.value_noise(w, h, max(3, 5 * scale), rng)
    img = Image.new("RGBA", (w, h))
    px = img.load()
    memo = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
            elif eye[y][x]:
                px[x, y] = (r, g, b, a)
            elif shiny:
                px[x, y] = tuple(int(v) for v in S.chocolate(r, g, b, (gloss[y][x] - 0.5) * 0.25)) + (a,)
            else:
                if (r, g, b) not in memo:
                    memo[(r, g, b)] = S.pastel(r, g, b)
                px[x, y] = memo[(r, g, b)] + (a,)
    units = max(1, (w * h) // (64 * 64 * scale * scale))
    if shiny:
        S.sprinkles(px, alpha, eye, w, h, rng, scale, 30 * units)
    else:
        for n, island in enumerate(S.islands(alpha, w, h, 150 * scale * scale)[:4]):
            c = S.PAINTS[(seed + n) % len(S.PAINTS)]
            S.zigzag_band(px, alpha, eye, island, scale, rng, (c, S.mix(c, (80, 60, 90), 0.35)))
        S.daisies(px, alpha, eye, w, h, rng, scale, 3 * units)
    _cache[key] = img
    return img


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":
        src = base.convert("RGBA")
        out = Image.new("RGBA", src.size)
        s, o = src.load(), out.load()
        for y in range(src.height):
            for x in range(src.width):
                r, g, b, a = s[x, y]
                o[x, y] = S.pastel(r, g, b) + (a,) if a else (0, 0, 0, 0)
        return out
    return _plan(base, eyes, seed, shiny).copy()
