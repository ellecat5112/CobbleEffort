"""Shared colours for Sparkling and its Swarm Form (the user's design and art, artist not named; our name): a tiny
black starling with a yellow hood and crest, huge glowing magenta eyes in a dark mask, a black beak, white wing
patches and pale legs. Its Swarm Form is thousands of them flying as one giant bird: black, dotted all over with
their glowing magenta eyes, yellow across the shoulders and neck, white birds tumbling from its chest.

Shiny: a white bird with a sky-blue hood and gold eyes."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _route import pal, tone

BASE = {"black": (40, 40, 46), "charcoal": (64, 64, 72), "yellow": (250, 230, 40), "yellow_dark": (214, 186, 24),
        "eye": (232, 60, 224), "eye_dark": (30, 22, 34), "mask": (78, 78, 88), "white": (248, 248, 250),
        "leg": (206, 206, 214), "beak": (34, 34, 38)}
SHINY = {"black": (232, 232, 240), "charcoal": (204, 206, 220), "yellow": (110, 200, 250), "yellow_dark": (70, 160, 220),
         "eye": (250, 200, 50), "white": (150, 150, 170), "mask": (170, 174, 194), "beak": (90, 90, 104)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def eye_on(p, u, v, r):
    """A big round eye: glowing magenta ring, dark middle, a white glint. (u, v) from its centre."""
    d = math.hypot(u, v)
    if d >= r:
        return None
    if math.hypot(u - r * 0.3, v - r * 0.35) < r * 0.22:
        return p["white"], None
    if d < r * 0.45:
        return p["eye_dark"], None
    return p["eye"], p["eye"]


def dotted(key, spacing=2.6, r=0.42, salt=0.0):
    """A surface covered in tiny birds: their glowing magenta eyes as dots on a jittered grid."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        a, b = {"up": (x, z), "down": (x, z), "north": (x, y), "south": (x, y), "east": (z, y), "west": (z, y)}[face]
        i, j = math.floor(a / spacing), math.floor(b / spacing)
        h = math.sin(i * 12.9898 + j * 78.233 + salt) * 43758.5453
        h -= math.floor(h)
        ca = (i + 0.25 + 0.5 * h) * spacing
        cb = (j + 0.25 + 0.5 * ((h * 7.13) % 1)) * spacing
        if math.hypot(a - ca, b - cb) < r:
            return p["eye"], p["eye"]
        return tone(p[key], face), None
    return s
