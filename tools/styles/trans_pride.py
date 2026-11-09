"""
Trans Pride collection look: the Pokémon wears the transgender pride flag.

* the flag's five horizontal stripes (light blue, pink, white, pink, light blue) run across the WHOLE body from head
  to toe: the generator tells this style the height of every texel on the model (WANTS_HEIGHTS), so a stripe lines
  up across head, arms, body and legs instead of following the texture layout
* each stripe keeps the original's light and shade, so markings, fur and plating still read; outlines stay dark
* the eyes keep their own colours
* glowing parts glow in the flag's colours, by the same stripes
* shiny: pastel glitter over the stripes, plus a layer of sparkles that twinkle and glow in the dark
"""
from __future__ import annotations

import random

from PIL import Image

from ._horror import find_eye_mask, mix

EMISSIVE = "retexture"
WANTS_HEIGHTS = True

BLUE = (91, 206, 250)
PINK = (245, 169, 184)
WHITE = (255, 255, 255)
STRIPES = [BLUE, PINK, WHITE, PINK, BLUE]          # top to bottom
OUTLINE = (52, 40, 70)
GLITTER = [(255, 255, 255), (214, 238, 255), (255, 220, 232)]

EXTRA_LAYERS = [{"name": "sparkle", "emissive": True, "translucent": True, "frames": 4, "fps": 4}]


def stripe(h):
    """Stripe colour for a height (1 = top of the model)."""
    return STRIPES[min(4, max(0, int((1 - h) * 5)))]


def height_lookup(base, heights):
    """height(x, y) for the texture's pixels: the model's texel heights when given, else the texture rows."""
    w, h = base.size
    if heights is None:
        return lambda x, y: 1 - (y + 0.5) / h
    gh, gw = heights.shape

    def at(x, y):
        v = heights[min(gh - 1, y * gh // h), min(gw - 1, x * gw // w)]
        return 1 - (y + 0.5) / h if v != v else float(v)       # NaN: a texel no face uses
    return at


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False, heights=None):
    rng = random.Random(seed)
    src = base.convert("RGBA")
    w, h = src.size
    sp = src.load()
    out = Image.new("RGBA", (w, h))
    op = out.load()
    eye = find_eye_mask(src, None if layer else eyes)
    height = height_lookup(src, heights)
    for y in range(h):
        for x in range(w):
            r, g, b, a = sp[x, y]
            if not a:
                op[x, y] = (0, 0, 0, 0)
                continue
            if eye[y][x] and not layer:
                op[x, y] = (r, g, b, a)                       # eyes keep their own colours
                continue
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            c = stripe(height(x, y))
            if layer == "emissive":
                c = tuple(int(v * (0.75 + 0.25 * lum)) for v in c)
            elif lum < 0.12:
                c = mix(c, OUTLINE, 0.7)                      # outlines and deep shadows stay dark
            else:
                f = 0.72 + 0.4 * lum                          # keep the original's shading inside the stripe
                c = tuple(min(255, int(v * f)) for v in c)
            if shiny and layer != "emissive" and rng.random() < 0.07:
                c = mix(c, rng.choice(GLITTER), 0.6)          # pastel glitter
            op[x, y] = tuple(int(v) for v in c) + (a,)
    return out


def extra_layer(name, base, eyes, seed, shiny, frame, heights=None):
    """Shinies only: little four-point sparkles that twinkle (a different scatter each frame) and glow."""
    if name != "sparkle" or not shiny:
        return None
    src = base.convert("RGBA")
    w, h = src.size
    sp = src.load()
    rng = random.Random(f"{seed}:sparkle:{frame}")
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()
    scale = max(1, w // 64)
    n = max(6, (w * h) // (110 * scale * scale))
    for _ in range(n):
        x, y = rng.randrange(w), rng.randrange(h)
        if not sp[x, y][3]:
            continue
        c = rng.choice([WHITE, BLUE, PINK]) + (255,)
        op[x, y] = c
        if rng.random() < 0.5:                                # a four-point star
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx * scale, y + dy * scale
                if 0 <= xx < w and 0 <= yy < h and sp[xx, yy][3]:
                    op[xx, yy] = c[:3] + (170,)
    return out
