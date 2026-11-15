"""Shared parts for the penguin line (Awkwaddle, Waddical; the user's "Snowy Routes" art, artist not named, names kept):
navy-backed penguins with white bellies and swim goggles; Awkwaddle clutches a blue swim ring, Waddical is a tall surfer
with olive-gold bands on its flippers and legs, its goggles pushed up, carrying a see-through surfboard.

Shiny: teal-backed with orange goggles and a pink board."""
from __future__ import annotations

import math

from _afake import ramp_of, solid_of
from _route import pal, tone

BASE = {"navy": (44, 46, 84), "navy_light": (72, 76, 124), "white": (244, 246, 250), "belly_shade": (212, 218, 232),
        "beak": (62, 62, 74), "feet": (242, 198, 60), "feet_dark": (66, 66, 78), "rim": (120, 186, 236),
        "lens": (214, 238, 252, 170), "eye": (30, 30, 40), "ring": (86, 166, 238), "ring_light": (214, 236, 252),
        "band": (196, 182, 70), "board": (190, 226, 248, 120), "board_rim": (150, 200, 236, 210), "drop": (150, 210, 250)}
SHINY = {"navy": (36, 104, 112), "navy_light": (64, 140, 148), "rim": (246, 146, 60), "ring": (246, 120, 150),
         "band": (240, 120, 60), "board": (250, 196, 220, 120), "board_rim": (240, 150, 190, 210)}


def palette():
    def P(v):
        return pal(BASE, SHINY, v)
    return P, solid_of(P), ramp_of(P)


P, solid, ramp = palette()


def penguin(belly_y, belly_rx, cy, ry, extra=None):
    """Navy back and sides, a white oval belly on the front (|x| < belly_rx over belly_y ± ry around cy)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if extra:
            c = extra(x, y, z, face, p)
            if c is not None:
                return c
        if face == "north" and belly_y[0] < y < belly_y[1]:
            w = belly_rx * math.sqrt(max(0.0, 1 - ((y - cy) / ry) ** 2))
            if abs(x) < w:
                return tone(p["white"] if abs(x) < w - 0.6 else p["belly_shade"], face), None
        if face == "up":
            return tone(p["navy_light"], face), None
        return tone(p["navy"], face), None
    return s


def lens(p, u, v, r, eye=True):
    """A goggle lens: a light-blue rim round a pale see-through lens, an eye showing behind it."""
    d = math.hypot(u, v)
    if d > r:
        return None
    if d > r * 0.72:
        return p["rim"]
    if eye and math.hypot(u, v + r * 0.1) < r * 0.32:
        return p["eye"] if math.hypot(u + r * 0.12, v - r * 0.02) > r * 0.1 else p["white"]
    return p["lens"]
