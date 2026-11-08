"""
Christmas collection look: "Festive" (the 14 random lines).

* colours moved onto a Christmas palette that keeps the markings readable: reds and oranges become crimson,
  yellows gold, greens pine, blues and cyans icy winter blue, purples berry red; whites turn snowy
* snow has settled on top of every surface, with a few snowflakes caught in the fur
* strings of fairy lights are draped across the body; the bulbs glow in the dark and twinkle
  (an extra emissive layer, 4 frames)
* eyes keep their original colours
* shiny: "frosted": silver, ice and snow all over, with the same twinkling lights
* glowing (emissive) parts keep glowing, recoloured with the same Christmas palette
"""
from __future__ import annotations

import random

from PIL import Image

from . import _festive as F

EMISSIVE = "retexture"
EXTRA_LAYERS = [F.LIGHTS]

_cache: dict = {}


def _plan(base: Image.Image, eyes: Image.Image | None, seed: int, shiny: bool):
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
            else:
                if (r, g, b) not in memo:
                    memo[(r, g, b)] = F.festive_colour(r, g, b, shiny)
                px[x, y] = memo[(r, g, b)] + (a,)
    F.snow_cap(px, alpha, eye, w, h, rng, scale)
    units = max(1, (w * h) // (64 * 64 * scale * scale))
    F.snowflakes(px, alpha, eye, w, h, rng, scale, 8 * units)
    wire, bulbs = F.plan_garlands(alpha, eye, w, h, rng, scale)
    F.paint_garlands(px, alpha, wire, bulbs, scale)
    _cache[key] = (img, alpha, bulbs, scale)
    return _cache[key]


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":   # glowing parts keep glowing, in Christmas colours
        src = base.convert("RGBA")
        out = Image.new("RGBA", src.size)
        s, o = src.load(), out.load()
        for y in range(src.height):
            for x in range(src.width):
                r, g, b, a = s[x, y]
                o[x, y] = F.festive_colour(r, g, b, shiny) + (a,) if a else (0, 0, 0, 0)
        return out
    img, *_ = _plan(base, eyes, seed, shiny)
    return img.copy()


def extra_layer(name, base, eyes, seed, shiny, frame):
    img, alpha, bulbs, scale = _plan(base, eyes, seed, shiny)
    if not bulbs:
        return None
    return F.lights_layer(img.size, alpha, bulbs, frame, scale)
