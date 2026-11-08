"""
Stone Statue collection look: the Pokémon as a solid stone statue.

* granite-grey stone, mapped from the original's light and shade, so the markings remain as carved relief
* mottled stone with grain and speckles, fine chisel strokes
* weathered edges: sunlit top edges, darker undersides, small chips
* dark cracks, and patches of moss and lichen
* blank, carved eyes, like a real statue
* no glow: statues don't light up, so glowing (emissive) layers are switched off
* shiny: polished white marble with grey veins and gilded eyes
"""
from __future__ import annotations

import math
import random

from PIL import Image

from ._festive import digest
from ._horror import find_eye_mask, mix, value_noise

EMISSIVE = "disable"

STONE = [(0.0, (60, 60, 62)), (0.35, (110, 110, 112)), (0.65, (162, 161, 160)), (0.85, (200, 199, 196)), (1.0, (224, 223, 220))]
MARBLE = [(0.0, (150, 148, 152)), (0.5, (214, 212, 214)), (1.0, (250, 248, 246))]
VEIN = (118, 122, 134)
GOLD = (214, 176, 60)
CRACK = (38, 36, 34)
MOSS = [(84, 108, 56), (104, 128, 64), (122, 142, 72)]
LICHEN = (176, 174, 96)

_cache: dict = {}


def ramp(stops, v):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            return mix(c0, c1, (v - p0) / (p1 - p0))
    return stops[-1][1]


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
    mottle = value_noise(w, h, max(3, 5 * scale), rng)
    moss = value_noise(w, h, max(4, 7 * scale), rng)
    vein_n = value_noise(w, h, max(6, 10 * scale), rng)
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
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            v = 0.3 + 0.6 * lum + (mottle[y][x] - 0.5) * 0.14 + rng.uniform(-0.04, 0.04)
            if shiny:
                c = ramp(MARBLE, 0.35 + 0.6 * lum + (mottle[y][x] - 0.5) * 0.08)
                if abs(math.sin(x * 0.18 + y * 0.09 + vein_n[y][x] * 5)) < 0.17:   # ~1-2 px wide, continuous
                    c = mix(c, VEIN, 0.55)                      # marble veins
                if eye[y][x]:
                    c = GOLD                                    # gilded eyes
            else:
                if eye[y][x]:
                    v -= 0.12                                   # blank, carved eyes: just a little deeper
                elif ((2 * x + y) // scale) % (7) == 0 and mottle[y][x] > 0.45:
                    v -= 0.07                                   # chisel strokes
                c = ramp(STONE, v)
                if rng.random() < 0.04:
                    c = mix(c, (30, 28, 26) if rng.random() < 0.6 else (230, 226, 216), 0.35)   # granite speckle
            # weathered edges: sunlit top edges, darker undersides, the odd chip
            if not opaque(x, y - 1):
                c = mix(c, (236, 232, 222), 0.25)
            elif not opaque(x, y + 1):
                c = mix(c, (30, 28, 26), 0.25)
            elif not all(opaque(x + dx, y) for dx in (-1, 1)) and rng.random() < 0.18:
                c = mix(c, (40, 38, 36), 0.35)
            px[x, y] = tuple(int(v_) for v_ in c) + (a,)

    units = max(1, (w * h) // (64 * 64 * scale * scale))
    # cracks
    for _ in range((1 if shiny else 3) * units):
        x, y = rng.randrange(w), rng.randrange(h)
        ang = rng.uniform(0, 2 * math.pi)
        for _ in range(rng.randint(5, 12) * scale):
            if opaque(x, y) and not eye[y][x]:
                px[x, y] = (mix(px[x, y][:3], CRACK, 0.75)) + (alpha[y][x],)
            ang += rng.uniform(-0.7, 0.7)
            x += int(round(math.cos(ang)))
            y += int(round(math.sin(ang)))
    # moss and lichen (not on polished marble)
    if not shiny:
        for y in range(h):
            for x in range(w):
                if alpha[y][x] and not eye[y][x] and moss[y][x] > 0.83:   # just the odd mossy patch
                    t = min(1.0, (moss[y][x] - 0.83) * 8)
                    px[x, y] = mix(px[x, y][:3], rng.choice(MOSS), 0.3 + 0.35 * t) + (alpha[y][x],)
        for _ in range(3 * units):
            x, y = rng.randrange(w), rng.randrange(h)
            if alpha[y][x] and not eye[y][x]:
                px[x, y] = LICHEN + (alpha[y][x],)
    _cache[key] = img
    return img


def retexture(base, eyes, seed, shiny, frame: int = 0, layer=False):
    if layer:   # non-glowing layers (e.g. wings) become stone too; glowing ones are disabled by EMISSIVE
        return plan(base, None, seed, shiny).copy()
    return plan(base, eyes, seed, shiny).copy()
