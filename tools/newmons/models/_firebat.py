"""Shared colours and parts for the fire starter line (Sounflame, Operbat, Nosfiretu), after the art of the A. Fakemon
fanpage (names kept): a little red bat with huge ears and flame-yellow wings, an opera bat in a golden mask and a
ruffled collar, and a Nosferatu-like vampire bat in a golden horned mask wrapped in a purple cape of wings.

Shiny: blue flames: deep blue bodies, pale cyan flames and gold, crimson capes.
"""
from __future__ import annotations

import math

from _afake import CUT, ramp_of, solid_of, tongues
from _boxmodel import mix
from _route import along, pal, tone

BASE = {"red": (216, 66, 50), "red_dark": (168, 40, 36), "red_light": (238, 112, 92), "yellow": (246, 198, 82),
        "yellow_light": (252, 228, 142), "orange": (240, 142, 52), "pink": (196, 56, 118), "purple": (112, 90, 192),
        "purple_dark": (76, 60, 142), "purple_light": (150, 132, 222), "eye_purple": (140, 90, 204),
        "white": (246, 246, 246), "claw": (214, 214, 222), "pupil": (40, 20, 30), "mouth": (110, 30, 36)}
SHINY = {"red": (66, 84, 170), "red_dark": (42, 56, 130), "red_light": (110, 130, 210), "yellow": (150, 222, 248),
         "yellow_light": (206, 244, 255), "orange": (90, 170, 236), "pink": (240, 170, 60), "purple": (170, 40, 64),
         "purple_dark": (120, 24, 44), "purple_light": (210, 80, 100), "eye_purple": (250, 190, 70)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)


def flame_spot(x, y):
    """A flame-licked pattern for the lower parts of the wings."""
    return math.sin(x * 1.7 + y * 0.4) + math.sin(y * 1.3 + x * 0.8) > 0.55


def membrane(x0, x1, top, bottom, colour):
    """A wing or cape on a plane in xy: from |x| = x0 at the body to x1 at the tip; kept between bottom(u) and top(u)
    (u = 0 at the body, 1 at the tip); colour(p, u, y, top, bottom) -> colour."""
    def s(x, y, z, face, variant, **k):
        u = (abs(x) - x0) / (x1 - x0)
        if u < -0.02 or u > 1.02:
            return CUT, None
        t, b = top(u), bottom(u)
        if not b < y < t:
            return CUT, None
        return tone(colour(P(variant), u, y, t, b), face), None
    return s


def segments(key, dark, period=1.3):
    """A segmented rod (a tail): rings of `dark` every `period` units."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        L = box.size[2]
        return tone(p[dark] if (along(z, box) * L) % period < 0.3 else p[key], face), None
    return s


__all__ = ["P", "solid", "ramp", "membrane", "segments", "flame_spot", "tongues", "mix"]
