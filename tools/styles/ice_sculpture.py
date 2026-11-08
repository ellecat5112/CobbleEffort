"""
Ice Sculpture collection look: the Pokémon carved out of a block of ice.

* recoloured in clear glacier-ice blues, mapped from the original's light and shade, so every marking
  is still there, as if chiselled into the ice
* faceted chisel planes (each facet catches the light a little differently)
* light streaks refracting through the ice, a few hairline cracks and trapped air bubbles
* a frosted white rim along every edge
* eyes carved as deeper-blue hollows
* a twinkling layer of glints that glow in the dark (extra emissive layer, 4 frames)
* shiny: "Aurora Ice", the same sculpture shimmering teal-to-violet like the northern lights
* glowing (emissive) parts become an icy cyan glow
"""
from __future__ import annotations

import colorsys
import math
import random

from PIL import Image

from ._festive import digest
from ._horror import find_eye_mask, mix, value_noise

EMISSIVE = "retexture"
EXTRA_LAYERS = [{"name": "glints", "emissive": True, "translucent": True, "frames": 4, "fps": 4}]

ICE = [(0.0, (28, 70, 120)), (0.35, (70, 140, 190)), (0.65, (150, 205, 235)), (0.85, (215, 238, 252)), (1.0, (250, 253, 255))]
FROST = (238, 248, 255)
HOLLOW = (22, 58, 104)

_cache: dict = {}


def ramp(v):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(ICE, ICE[1:]):
        if v <= p1:
            return mix(c0, c1, (v - p0) / (p1 - p0))
    return ICE[-1][1]


def aurora(c, x, y, w, h):
    """Shiny: keep the ice's lightness, shift the hue teal -> violet across the sculpture."""
    _, l, _ = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255)
    hue = 0.48 + 0.32 * ((x / max(1, w)) * 0.6 + (y / max(1, h)) * 0.4)
    r, g, b = colorsys.hls_to_rgb(hue, l * 0.9, 0.68)
    return (int(r * 255), int(g * 255), int(b * 255))


def facets(w, h, cell, rng):
    """Jittered-grid Voronoi cells: returns a per-pixel brightness offset, one value per facet."""
    gw, gh = w // cell + 2, h // cell + 2
    pts = [[(gx * cell + rng.uniform(0, cell), gy * cell + rng.uniform(0, cell), rng.uniform(-0.07, 0.07))
            for gx in range(gw)] for gy in range(gh)]
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        gy = y // cell
        for x in range(w):
            gx = x // cell
            best, val = 1e9, 0.0
            for yy in range(max(0, gy - 1), min(gh, gy + 2)):
                for xx in range(max(0, gx - 1), min(gw, gx + 2)):
                    px_, py_, v = pts[yy][xx]
                    d = (px_ - x) ** 2 + (py_ - y) ** 2
                    if d < best:
                        best, val = d, v
            out[y][x] = val
    return out


def plan(base, eyes, seed, shiny):
    key = (digest(base), digest(eyes), seed, shiny)
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye = find_eye_mask(base, eyes)
    facet = facets(w, h, max(3, 5 * scale), rng)
    cloud = value_noise(w, h, max(4, 8 * scale), rng)
    img = Image.new("RGBA", (w, h))
    px = img.load()

    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and alpha[y][x]

    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            if eye[y][x]:
                c = HOLLOW
            else:
                lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                v = 0.25 + 0.68 * lum + facet[y][x] + (cloud[y][x] - 0.5) * 0.12
                c = ramp(v)
                # frosted rim along the edges of every painted area
                if not all(opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    c = mix(c, FROST, 0.55)
            px[x, y] = tuple(int(v) for v in c) + (a,)

    units = max(1, (w * h) // (64 * 64 * scale * scale))
    # refraction streaks: thin diagonal bands of brighter ice
    for _ in range(3 * units):
        k = rng.randrange(-h, w)
        width = rng.choice((1, 1, 2)) * scale
        for y in range(h):
            for d in range(width):
                x = y + k + d
                if opaque(x, y) and not eye[y][x]:
                    px[x, y] = mix(px[x, y][:3], (255, 255, 255), 0.28) + (alpha[y][x],)
    # hairline cracks
    for _ in range(2 * units):
        x, y = rng.randrange(w), rng.randrange(h)
        ang = rng.uniform(0, 2 * math.pi)
        for _ in range(rng.randint(5, 12) * scale):
            if opaque(x, y) and not eye[y][x]:
                px[x, y] = mix(px[x, y][:3], (245, 252, 255), 0.7) + (alpha[y][x],)
            ang += rng.uniform(-0.6, 0.6)
            x += int(round(math.cos(ang)))
            y += int(round(math.sin(ang)))
    # trapped air bubbles
    for _ in range(10 * units):
        x, y = rng.randrange(w), rng.randrange(h)
        if opaque(x, y) and not eye[y][x]:
            px[x, y] = (236, 248, 255, alpha[y][x])
    if shiny:
        for y in range(h):
            for x in range(w):
                if alpha[y][x] and not eye[y][x]:
                    px[x, y] = aurora(px[x, y][:3], x, y, w, h) + (alpha[y][x],)

    # glints: little four-point sparkles, each lit in one or two of the four frames
    glints = []
    for _ in range(4 * units):
        x, y = rng.randrange(scale, w - scale), rng.randrange(scale, h - scale)
        arms = [(x + dx * scale, y + dy * scale) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if opaque(x, y) and not eye[y][x] and all(opaque(ax, ay) for ax, ay in arms):
            glints.append((x, y, arms, {rng.randrange(4), rng.randrange(4)}))
    _cache[key] = (img, glints, scale)
    return _cache[key]


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer == "emissive":   # glowing parts become an icy cyan glow
        src = base.convert("RGBA")
        out = Image.new("RGBA", src.size)
        s, o = src.load(), out.load()
        for y in range(src.height):
            for x in range(src.width):
                r, g, b, a = s[x, y]
                v = max(r, g, b) / 255
                o[x, y] = (int(120 * v), int(230 * v), int(255 * v), a) if a else (0, 0, 0, 0)
        return out
    return plan(base, eyes, seed, shiny)[0].copy()


def extra_layer(name, base, eyes, seed, shiny, frame):
    img, glints, scale = plan(base, eyes, seed, shiny)
    if not glints:
        return None
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    o = out.load()
    for x, y, arms, frames in glints:
        if frame in frames:
            for sy in range(scale):
                for sx in range(scale):
                    o[x + sx, y + sy] = (255, 255, 255, 255)
            for ax, ay in arms:
                o[ax, ay] = (200, 236, 255, 220)
    return out
