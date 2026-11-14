"""Shared colours and parts for the CobbleEffortian (Ghost/Fire) Gastly line, after @tomats_art's art: red bodies with
yellow spots, horns, white cyclops eyes, yellow-orange flame gas, red-and-yellow flames, a blue ghost tongue."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _boxmodel import spike
from _route import pal, tone

BASE = {"red": (218, 40, 44), "red_dark": (150, 20, 34), "red_light": (240, 90, 80), "yellow": (250, 206, 60),
        "orange": (242, 140, 40), "orange_dark": (200, 96, 30), "gas": (255, 190, 50, 105), "gas_hot": (255, 230, 120, 125),
        "white": (250, 250, 250), "pupil": (30, 26, 34), "mouth": (80, 50, 110), "fang": (255, 255, 255),
        "blue": (70, 180, 230, 170), "blue_light": (150, 220, 250, 150), "mask": (36, 30, 36), "iris": (250, 210, 60),
        "claw": (246, 160, 60)}
SHINY = {"red": (70, 110, 220), "red_dark": (40, 60, 160), "red_light": (120, 160, 240), "yellow": (170, 240, 255),
         "gas": (120, 220, 255, 105), "gas_hot": (200, 245, 255, 125), "orange": (110, 190, 240), "orange_dark": (70, 140, 210),
         "blue": (255, 120, 180, 170), "blue_light": (255, 180, 210, 150), "claw": (150, 220, 255)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def red_spotted(spots, eye=None):
    """Red skin with yellow spots at (x, y, r) on the side faces; `eye(x, y, z, face, variant)` paints the front."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if eye:
            e = eye(x, y, z, face, variant)
            if e:
                return e, None
        for sx, sy, r in spots:
            if face in ("north", "east", "west") and (x - sx) ** 2 + (y - sy) ** 2 < r * r and face != "north" or \
                    face == "north" and (x - sx) ** 2 + (y - sy) ** 2 < r * r:
                return p["yellow"], None
        return tone(p["red_light"] if face == "up" else p["red"], face), None
    return s


def flame_shader(x, y, z, face, variant, **k):
    """A red flame, yellow towards its root."""
    p = P(variant)
    box = k.get("box")
    t = 0.5
    if box is not None:
        t = (y - box.lo[1]) / max(1e-6, box.size[1])
    c = p["yellow"] if t < 0.35 and (int(x * 2 + z * 2) % 3) else p["red"]
    return tone(c, face), None


def gas(m, bone, c, r, hot=False):
    """A translucent, glowing puff of flame gas."""
    def s(x, y, z, face, variant, **k):
        col = P(variant)["gas_hot" if hot else "gas"]
        return col, col[:3]
    m.round_box(bone, c[0], c[2], r, r, c[1] - r, c[1] + r, s, cut=max(0.5, r * 0.45))


def flames(m, bone, base, n, length, width, spread=0.6, up=(0, 1, 0)):
    """A fan of flame tongues from a point."""
    for i in range(n):
        a = (i - (n - 1) / 2) * spread
        d = (math.sin(a) + up[0], math.cos(a) * up[1] + 0.2, up[2])
        spike(m, bone, base, d, width, length * (0.75 + 0.25 * math.cos(a)), flame_shader, tip=width * 0.45)
