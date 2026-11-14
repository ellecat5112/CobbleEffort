"""Shared parts for Ufly, the Neon Light Pokémon (Bug/Psychic), and its Swarm Form, after @maumesdex's art (name kept):
a plump little purple bug with a lime-green back, two big translucent wings standing up like ears, great teal compound
eyes and glowing teal spots. Its Swarm Form is thousands of them as one great flying saucer.

Shiny: magenta with an orange back and gold lights."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _route import pal, tone

BASE = {"purple": (92, 52, 160), "purple_dark": (58, 30, 112), "purple_light": (140, 96, 214), "lime": (184, 222, 70),
        "lime_dark": (130, 172, 46), "teal": (110, 236, 200), "teal_dark": (40, 150, 136), "wing": (196, 240, 236, 120),
        "wing_rim": (150, 220, 214, 190), "foot": (40, 26, 70), "white": (240, 255, 250)}
SHINY = {"purple": (176, 52, 140), "purple_dark": (120, 26, 96), "purple_light": (226, 104, 188), "lime": (250, 156, 50),
         "lime_dark": (206, 110, 30), "teal": (255, 214, 80), "teal_dark": (200, 150, 30)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def spotted(key, spacing=2.4, r=0.45, salt=0.0):
    """A surface dotted with glowing teal lights on a jittered grid (every one a little Ufly's glow)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a, b = {"up": (x, z), "down": (x, z), "north": (x, y), "south": (x, y), "east": (z, y), "west": (z, y)}[face]
        i, j = math.floor(a / spacing), math.floor(b / spacing)
        h = math.sin(i * 12.9898 + j * 78.233 + salt) * 43758.5453
        h -= math.floor(h)
        if h < 0.45:                                                   # not every cell has a light
            return tone(p[key], face), None
        ca = (i + 0.25 + 0.5 * h) * spacing
        cb = (j + 0.25 + 0.5 * ((h * 7.13) % 1)) * spacing
        if math.hypot(a - ca, b - cb) < r:
            return p["teal"], p["teal"]
        return tone(p[key], face), None
    return s


def compound_eye(p, u, v, r):
    """A great teal compound eye: facets in a lighter grid, a dark rim. (u, v) from its centre."""
    d = math.hypot(u, v)
    if d >= r:
        return None
    if d > r * 0.82:
        return p["teal_dark"], None
    if (round(u * 2) + round(v * 2)) % 2 == 0:
        return p["teal"], p["teal"]
    return tuple(min(255, c + 30) for c in p["teal"]), p["teal"]


def wing():
    """A translucent wing plane (the shell layer), its rim a little stronger. Oval, cut out round it."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        cx = box.lo[0] + box.size[0] / 2
        cy = box.lo[1] + box.size[1] / 2
        cz = box.lo[2] + box.size[2] / 2
        rx, ry, rz = max(box.size[0], 1e-6) / 2, box.size[1] / 2, max(box.size[2], 1e-6) / 2
        u = (x - cx) / rx if box.size[0] else (z - cz) / rz
        d = math.hypot(u, (y - cy) / ry)
        if d > 1:
            return (0, 0, 0, 0), None
        return (p["wing_rim"] if d > 0.82 else p["wing"]), None
    return s


def mini_bug(m, bone, c, s=1.0):
    """A little Ufly (the swarm's members, drifting round it): a purple blob, a lime back, two wing planes."""
    x, y, z = c
    m.round_box(bone, x, z, 1.4 * s, 1.2 * s, y, y + 2.2 * s, spotted("purple", 1.2, 0.3), cut=max(0.4, round(0.5 * s, 1)))
    m.box(bone, x - 1.0 * s, y + 2.0 * s, z - 0.6 * s, x + 1.0 * s, y + 2.8 * s, z + 0.9 * s, solid("lime"))
    for sx in (-1, 1):
        m.box(bone, x + sx * 0.6 * s, y + 2.6 * s, z, x + sx * 0.6 * s + sx * 0.0, y + 4.6 * s, z + 1.6 * s, wing(),
              rotation=(0, 0, sx * 18), pivot=(x + sx * 0.6 * s, y + 2.6 * s, z))
