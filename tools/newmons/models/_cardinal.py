"""Shaders shared by the cardinal line (Cardling, Rubraptor): red plumage, white belly and wing spots, grey beak and
legs, the black mask round the beak. Shiny: a blue jay's blue."""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

BASE = {"red": (214, 30, 40), "red_dark": (150, 18, 30), "red_light": (240, 80, 80), "white": (250, 244, 236),
        "cream": (248, 214, 170), "grey": (150, 156, 168), "grey_dark": (100, 104, 116), "mask": (34, 30, 34),
        "blush": (255, 160, 190), "stripe": (250, 210, 90)}
SHINY = {"red": (60, 120, 220), "red_dark": (34, 70, 160), "red_light": (120, 180, 250), "blush": (190, 210, 255),
         "stripe": (230, 240, 255)}


def P(variant):
    return pal(BASE, SHINY, variant)


def plumage(spots=(), belly=None):
    """Red plumage; white oval spots at the given (x, y, z, r) places (on any face near them); a white belly on the
    front below `belly` (a height)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        for sx, sy, sz, r in spots:
            if math.sqrt(((x - sx) / r) ** 2 + ((y - sy) / (r * 0.7)) ** 2 + ((z - sz) / r) ** 2) < 1:
                return p["white"], None
        if belly is not None and face in ("north", "down") and y < belly:
            return tone(p["white"], face), None
        return tone(p["red"], face), None
    return s


def grey(x, y, z, face, variant, **k):
    return tone(P(variant)["grey"], face), None


def feather(stripes=()):
    """A tail feather plane: red with pale stripes at the given heights along it (cut to a pointed feather by its box)."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if any(abs(z - s_) < 0.35 for s_ in stripes):
            return p["stripe"], None
        return p["red"], None
    return s
