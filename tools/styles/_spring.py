"""
Shared pixel-art toolkit for the Easter styles: pastel colours, chocolate, painted-egg patterns,
spring daisies and candy sprinkles.
"""
from __future__ import annotations

import colorsys
import math
import random

from PIL import Image

from ._festive import digest, snow_cap  # noqa: F401  (re-exported)
from ._horror import components, find_eye_mask, mix, value_noise  # noqa: F401  (re-exported)

# pastel paints for eggs: pink, butter yellow, mint, sky blue, lavender, peach
PAINTS = [(246, 168, 196), (250, 230, 140), (160, 226, 190), (150, 200, 244), (198, 170, 236), (250, 196, 156)]
WHITE = (255, 253, 248)
DAISY = (255, 255, 250)
DAISY_HEART = (250, 206, 60)
SPRINKLES = [(250, 120, 170), (120, 200, 250), (250, 230, 100), (150, 230, 160), (200, 150, 240), (255, 255, 255)]
CHOC = [(0.0, (40, 20, 10)), (0.4, (92, 52, 28)), (0.75, (140, 86, 50)), (1.0, (196, 140, 96))]
WHITE_CHOC = [(0.0, (190, 168, 130)), (0.6, (240, 226, 196)), (1.0, (255, 248, 230))]
GOLD = [(0.0, (110, 70, 10)), (0.4, (190, 140, 30)), (0.75, (240, 200, 70)), (1.0, (255, 244, 180))]
JEWELS = [(200, 20, 60), (30, 80, 210), (20, 150, 90), (250, 250, 255)]


def ramp(stops, v):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            return mix(c0, c1, (v - p0) / (p1 - p0))
    return stops[-1][1]


def pastel(r, g, b):
    """Same hue, lighter and softer: every colour becomes its pastel version."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if s < 0.1:   # greys/blacks/whites: soft warm grey to cream
        return mix((150, 140, 150), WHITE, l)
    cr, cg, cb = colorsys.hls_to_rgb(h, 0.5 + l * 0.42, max(0.35, min(0.62, s * 0.8)))
    return (int(cr * 255), int(cg * 255), int(cb * 255))


def chocolate(r, g, b, gloss: float = 0.0):
    l = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[1]
    return ramp(CHOC, l * 0.9 + gloss)


def egg_pattern(x, y, y0, band_h, scale, rng_bands):
    """Painted-egg decoration at (x, y): horizontal bands, each solid, zigzag, dotted or striped.

    rng_bands is a list of (kind, colour, colour2) per band; returns a colour.
    """
    band = (y - y0) // band_h
    kind, c1, c2 = rng_bands[band % len(rng_bands)]
    fy = (y - y0) % band_h
    if kind == "zigzag":
        period = 2 * band_h
        tri = abs(((x // scale) % (period // scale)) * scale - band_h)   # triangle wave 0..band_h
        return c2 if fy >= tri * 0.9 - scale else c1
    if kind == "dots":
        cx, cy = (x // (3 * scale)) % 2, (fy // (2 * scale)) % 2
        return c2 if cx == cy and fy not in (0, band_h - 1) else c1
    if kind == "stripe":
        return WHITE if fy < scale or fy >= band_h - scale else c1
    return c1


def make_bands(rng: random.Random, n: int, paints=PAINTS):
    kinds = ["solid", "zigzag", "stripe", "dots"]
    out = []
    for i in range(n):
        c1 = paints[(i * 2 + rng.randrange(2)) % len(paints)]
        c2 = paints[(paints.index(c1) + 3) % len(paints)]
        out.append((kinds[i % len(kinds)], c1, c2))
    return out


def zigzag_band(px, alpha, eye, island, scale, rng, colours):
    """One painted zigzag ribbon across a big area, like the decoration round an Easter egg."""
    xs, ys = [p[0] for p in island], [p[1] for p in island]
    y_mid = min(ys) + int((max(ys) - min(ys)) * rng.uniform(0.35, 0.65))
    amp, period = 2 * scale, 6 * scale
    inside = set(island)
    c_fill, c_line = colours
    for x in range(min(xs), max(xs) + 1):
        tri = abs((x % period) - period / 2) / (period / 2)   # 0..1
        zy = int(y_mid - amp + 2 * amp * tri)
        for k in range(-2 * scale, 2 * scale + 1):
            y = zy + k
            if (x, y) in inside and not eye[y][x]:
                px[x, y] = (c_line if abs(k) >= 2 * scale - (scale - 1) else c_fill) + (alpha[y][x],)


def daisies(px, alpha, eye, w, h, rng, scale, count, allowed=None):
    """Little spring daisies: white petals round a yellow heart."""
    shape = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    for _ in range(count * 4):
        if count <= 0:
            break
        x, y = rng.randrange(scale, w - 2 * scale), rng.randrange(scale, h - 2 * scale)
        cells = [(x + dx * scale + sx, y + dy * scale + sy) for dx, dy in shape + [(0, 0)]
                 for sy in range(scale) for sx in range(scale)]
        if all(0 <= cx < w and 0 <= cy < h and alpha[cy][cx] and not eye[cy][cx]
               and (not allowed or allowed[cy][cx]) for cx, cy in cells):
            for dx, dy in shape + [(0, 0)]:
                for sy in range(scale):
                    for sx in range(scale):
                        cx, cy = x + dx * scale + sx, y + dy * scale + sy
                        px[cx, cy] = (DAISY_HEART if (dx, dy) == (0, 0) else DAISY) + (alpha[cy][cx],)
            count -= 1


def sprinkles(px, alpha, eye, w, h, rng, scale, count):
    for _ in range(count):
        x, y = rng.randrange(w - scale), rng.randrange(h - scale)
        horiz = rng.random() < 0.5
        cells = [(x + (i if horiz else 0), y + (0 if horiz else i)) for i in range(2 * scale)]
        if all(0 <= cx < w and 0 <= cy < h and alpha[cy][cx] and not eye[cy][cx] for cx, cy in cells):
            c = rng.choice(SPRINKLES)
            for cx, cy in cells:
                px[cx, cy] = c + (alpha[cy][cx],)


def islands(alpha, w, h, min_px):
    cells = [(x, y) for y in range(h) for x in range(w) if alpha[y][x]]
    return [i for i in components(cells) if len(i) >= min_px]
