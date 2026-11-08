"""
Shared pixel-art toolkit for the Christmas styles: palette, snow, snowflakes, light garlands.

Fairy lights are split in two: the wire and unlit bulbs are painted into the body texture, and the lit
bulbs live in an extra emissive layer (4 frames) so they glow in the dark and twinkle.
"""
from __future__ import annotations

import colorsys
import hashlib
import math
import random

from PIL import Image

from ._horror import components, find_eye_mask, mix, value_noise  # noqa: F401  (re-exported)

SNOW = (244, 248, 255)
SNOW_SHADE = (206, 220, 238)
WIRE = (22, 58, 30)
BULBS = [(255, 46, 46), (255, 196, 40), (60, 220, 90), (70, 140, 255), (255, 250, 236)]
GOLD = (236, 184, 44)
GOLD_DARK = (150, 104, 18)

LIGHTS = {"name": "lights", "emissive": True, "translucent": True, "frames": 4, "fps": 3}

# original hue (deg) -> christmas hue (deg, may be unwrapped), saturation multiplier
HUE_ANCHORS = [
    (0, -4, 1.15), (30, 0, 1.15),       # reds, oranges -> crimson
    (52, 45, 1.05),                     # yellow -> gold
    (80, 128, 0.75), (165, 140, 0.75),  # greens -> pine
    (195, 200, 0.45), (255, 210, 0.40), # cyan, blue -> icy winter blue
    (300, -22, 0.95), (340, -8, 1.15),  # purple, magenta -> berry crimson
    (360, -4, 1.15),
]


def digest(img: Image.Image | None) -> str:
    return "" if img is None else hashlib.md5(img.convert("RGBA").tobytes()).hexdigest()


def hue_map(h_deg: float):
    for (h0, t0, s0), (h1, t1, s1) in zip(HUE_ANCHORS, HUE_ANCHORS[1:]):
        if h_deg <= h1:
            t = (h_deg - h0) / (h1 - h0)
            return (t0 + (t1 - t0) * t) % 360, s0 + (s1 - s0) * t
    return HUE_ANCHORS[-1][1] % 360, HUE_ANCHORS[-1][2]


def festive_colour(r, g, b, shiny: bool):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if shiny:   # frosted: silver, ice and snow
        cr, cg, cb = colorsys.hls_to_rgb(0.57, min(0.95, l * 0.75 + 0.22), min(0.35, s * 0.3 + 0.05))
        return (int(cr * 255), int(cg * 255), int(cb * 255))
    if s < 0.14:   # greys and whites go a little colder, like snow
        return mix((r, g, b), (int(l * 225), int(l * 238), min(255, int(l * 255 + 10))), 0.5)
    th, sm = hue_map(h * 360)
    cr, cg, cb = colorsys.hls_to_rgb(th / 360, max(0.08, min(0.92, l * 0.96)), max(0.25, min(0.95, s * sm)))
    return (int(cr * 255), int(cg * 255), int(cb * 255))


def opaque_fn(alpha, w, h):
    return lambda x, y: 0 <= x < w and 0 <= y < h and alpha[y][x] > 0


def snow_cap(px, alpha, eye, w, h, rng, scale, allowed=None):
    """Snow settles on the top edge of every painted area (the 'up' faces in Minecraft's box UV layout)."""
    depth_noise = value_noise(w, 1, max(3, 4 * scale), rng)[0]
    width_ok = [[False] * w for _ in range(h)]   # only areas at least 6 px wide get snow
    for y in range(h):
        x = 0
        while x < w:
            if alpha[y][x]:
                x0 = x
                while x < w and alpha[y][x]:
                    x += 1
                if x - x0 >= 6 * scale:
                    for xx in range(x0, x):
                        width_ok[y][xx] = True
            else:
                x += 1
    for x in range(w):
        depth = int(scale * (1 + depth_noise[x] * 2.4))
        for y in range(h):
            if alpha[y][x] and (y == 0 or not alpha[y - 1][x]):
                run = 0
                while y + run < h and alpha[y + run][x]:
                    run += 1
                if run < 4 * scale:
                    continue          # thin slivers (spikes, branches, edges) stay snow-free
                for k in range(min(depth, run // 4)):
                    yy = y + k
                    if yy >= h or not alpha[yy][x] or eye[yy][x] or not width_ok[yy][x] or (allowed and not allowed[yy][x]):
                        break
                    c = SNOW_SHADE if k == depth - 1 else (255, 255, 255) if rng.random() < 0.08 else SNOW
                    px[x, yy] = c + (alpha[yy][x],)


def snowflakes(px, alpha, eye, w, h, rng, scale, count, allowed=None):
    for _ in range(count):
        x, y = rng.randrange(w), rng.randrange(h)
        cells = [(x, y)] + ([(x + d * scale, y) for d in (-1, 1)] + [(x, y + d * scale) for d in (-1, 1)]
                            if rng.random() < 0.5 else [])
        if all(0 <= cx < w and 0 <= cy < h and alpha[cy][cx] and not eye[cy][cx]
               and (not allowed or allowed[cy][cx]) for cx, cy in cells):
            for cx, cy in cells:
                for sy in range(scale):
                    for sx in range(scale):
                        if 0 <= cx + sx < w and 0 <= cy + sy < h and alpha[cy + sy][cx + sx]:
                            px[cx + sx, cy + sy] = (250, 252, 255, alpha[cy + sy][cx + sx])


def plan_garlands(alpha, eye, w, h, rng, scale, allowed=None, per_island=1):
    """Sagging strings of lights across each big painted area. Returns (wire pixels, bulbs)."""
    ok = opaque_fn(alpha, w, h)
    cells = [(x, y) for y in range(h) for x in range(w) if alpha[y][x] and (not allowed or allowed[y][x])]
    wire, bulbs = [], []
    for island in components(cells):
        xs = [p[0] for p in island]
        ys = [p[1] for p in island]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if x1 - x0 < 12 * scale or y1 - y0 < 6 * scale:
            continue
        inside = set(island)
        for n in range(per_island):
            base_y = y0 + int((y1 - y0) * rng.uniform(0.25, 0.7))
            sag = rng.uniform(1.5, 3.5) * scale
            phase0 = rng.randrange(3)
            step = 4 * scale
            swags = max(1, (x1 - x0) // (20 * scale))   # one sagging loop per ~20 px
            for x in range(x0, x1 + 1):
                t = (x - x0) / max(1, x1 - x0)
                y = int(base_y + sag * math.sin(math.pi * ((t * swags) % 1)))
                if (x, y) in inside and not eye[y][x]:
                    wire.append((x, y))
                    if (x - x0) % step == step // 2:
                        bulbs.append({"x": x, "y": y + scale, "colour": BULBS[(len(bulbs)) % len(BULBS)],
                                      "phase": (phase0 + len(bulbs)) % 3})
    bulbs = [b for b in bulbs if all(ok(b["x"] + sx, b["y"] + sy) and not eye[b["y"] + sy][b["x"] + sx]
                                     for sy in range(scale) for sx in range(scale))]
    return wire, bulbs


def paint_garlands(px, alpha, wire, bulbs, scale):
    for x, y in wire:
        px[x, y] = WIRE + (alpha[y][x],)
    for b in bulbs:
        for sy in range(scale):
            for sx in range(scale):
                x, y = b["x"] + sx, b["y"] + sy
                px[x, y] = mix(b["colour"], (30, 30, 30), 0.55) + (alpha[y][x],)


def lights_layer(size, alpha, bulbs, frame: int, scale: int):
    """Only the lit bulbs, for the emissive layer. Each bulb is off one frame in three, so they twinkle."""
    w, h = size
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    o = out.load()
    for b in bulbs:
        if (frame + b["phase"]) % 3 == 0:
            continue
        for sy in range(scale):
            for sx in range(scale):
                o[b["x"] + sx, b["y"] + sy] = b["colour"] + (255,)
    return out
