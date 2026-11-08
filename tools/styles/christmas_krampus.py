"""
Christmas collection, Phantump line (Phantump, Trevenant): "Krampus".

* the body becomes Krampus's shaggy black-brown goat fur, with long dark streaks running down
* the leafy parts become ridged ram's horn, ivory fading to charcoal
* the eyes burn red, and glow in the dark (an extra emissive layer; any existing glow turns red too)
* a long red tongue lolls down from the face
* heavy iron chains wrap round the body, with gold bells hanging from them
* a little snow on top
* shiny: a white-furred Krampus with gold horns
"""
from __future__ import annotations

import colorsys
import random

from PIL import Image

from . import _festive as F

EMISSIVE = "retexture"
EXTRA_LAYERS = [{"name": "glare", "emissive": True, "translucent": True}]

FUR = [(0.0, (10, 7, 6)), (0.5, (44, 30, 22)), (1.0, (96, 70, 50))]
FUR_SHINY = [(0.0, (120, 116, 112)), (0.5, (196, 192, 186)), (1.0, (246, 244, 238))]
HORN = [(0.0, (34, 30, 28)), (0.5, (120, 108, 92)), (1.0, (222, 210, 182))]
HORN_SHINY = [(0.0, (110, 76, 14)), (0.5, (196, 150, 40)), (1.0, (252, 220, 120))]
EYE_RED = (255, 36, 18)
TONGUE = (196, 28, 54)
TONGUE_DARK = (120, 10, 30)
IRON = (120, 122, 130)
IRON_DARK = (44, 44, 50)

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
    streak = [rng.uniform(-0.18, 0.18) for _ in range(w)]          # long fur strands run down each column
    clump = F.value_noise(w, h, max(2, 3 * scale), rng)
    fur, horn = (FUR_SHINY, HORN_SHINY) if shiny else (FUR, HORN)
    img = Image.new("RGBA", (w, h))
    px = img.load()
    used = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if eye[y][x]:
                c = EYE_RED
            elif 0.17 <= hh <= 0.47 and s > 0.2:      # leaves -> ridged horn
                c = _ramp(horn, l * 0.8 + (0.15 if (y // scale) % 3 == 0 else 0))
            else:
                c = _ramp(fur, l * 0.75 + streak[x] + (clump[y][x] - 0.5) * 0.3)
            px[x, y] = tuple(int(v) for v in c) + (a,)

    ok = lambda x, y: 0 <= x < w and 0 <= y < h and alpha[y][x] and not eye[y][x]
    # the tongue: from below the eyes, down the middle of the face
    eye_groups = F.components([(x, y) for y in range(h) for x in range(w) if eye[y][x]])
    if eye_groups:
        pair = sorted(eye_groups, key=len, reverse=True)[:2]
        cx = sum(sum(p[0] for p in g) / len(g) for g in pair) / len(pair)
        top = max(p[1] for g in pair for p in g) + 2 * scale
        cx = int(cx)
        length = 9 * scale
        for k in range(length):
            half = scale if k < length - 2 * scale else max(1, scale // 2)
            for dx in range(-half, half + (1 if scale > 1 else 0)):
                x, y = cx + dx, top + k
                if ok(x, y):
                    px[x, y] = (TONGUE_DARK if dx == 0 and k > scale else TONGUE) + (alpha[y][x],)
                    used[y][x] = True
    # chains round the body, with bells
    islands = sorted((i for i in F.components([(x, y) for y in range(h) for x in range(w) if alpha[y][x]])
                      if len(i) > 120 * scale * scale), key=len, reverse=True)[:3]
    for island in islands:
        ys = [p[1] for p in island]
        cy = min(ys) + int((max(ys) - min(ys)) * rng.uniform(0.55, 0.8))
        inside = set(island)
        row = sorted(x for x, y in island if y == cy)
        for i, x in enumerate(row):
            link = (x // (3 * scale)) % 2
            for dy in range(-scale, 2 * scale):
                y = cy + dy
                if (x, y) not in inside or eye[y][x] or used[y][x]:
                    continue
                if link == 0:   # flat oval link
                    edge = dy in (-scale, 2 * scale - 1)
                    px[x, y] = (IRON if edge else IRON_DARK) + (alpha[y][x],)
                elif 0 <= dy < scale:   # edge-on link
                    px[x, y] = IRON + (alpha[y][x],)
        for x in row[2 * scale::12 * scale]:
            for dy in range(2 * scale, 5 * scale):
                for dx in range(-scale, scale + 1):
                    bx, by = x + dx, cy + dy
                    if (bx, by) in inside and not eye[by][bx] and not used[by][bx]:
                        px[bx, by] = (F.GOLD_DARK if dy == 4 * scale or abs(dx) == scale else F.GOLD) + (alpha[by][bx],)
    F.snow_cap(px, alpha, eye, w, h, rng, scale)
    _cache[key] = (img, eye)
    return _cache[key]


def _red_glow(base):
    base = base.convert("RGBA")
    out = Image.new("RGBA", base.size)
    s, o = base.load(), out.load()
    for y in range(base.height):
        for x in range(base.width):
            r, g, b, a = s[x, y]
            v = max(r, g, b) / 255
            o[x, y] = (int(255 * v), int(40 * v), int(20 * v), a) if a else (0, 0, 0, 0)
    return out


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":
        return _red_glow(base)
    return _plan(base, eyes, seed, shiny)[0].copy()


def extra_layer(name, base, eyes, seed, shiny, frame):
    img, eye = _plan(base, eyes, seed, shiny)
    if not any(any(row) for row in eye):
        return None
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    o = out.load()
    for y, row in enumerate(eye):
        for x, v in enumerate(row):
            if v:
                o[x, y] = EYE_RED + (255,)
    return out
