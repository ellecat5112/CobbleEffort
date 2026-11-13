"""Shared colours and shaders for the minnow fossil line (Minnolith, Placofin): ancient armoured fish inspired by
minnows and guppies, after the fakemon art by Fionn Keeley (@fionnkeeley, @miscfionn, aegiro) that the user shared;
names and models are our own.

Shiny: a goldfish-orange body with deep red-brown fins, like a fancy guppy.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

BASE = {"blue": (156, 210, 234), "blue_shade": (112, 172, 210), "blue_light": (196, 232, 246),
        "white": (238, 236, 230), "white_shade": (206, 204, 200), "fin": (132, 112, 118), "fin_light": (168, 150, 154),
        "fin_tip": (236, 232, 228), "eye": (30, 26, 30), "eye_white": (242, 240, 228), "leg": (202, 190, 142),
        "seam": (90, 120, 150)}
SHINY = {"blue": (244, 166, 72), "blue_shade": (214, 126, 46), "blue_light": (252, 204, 120), "fin": (150, 56, 48),
         "fin_light": (196, 90, 72), "seam": (160, 90, 40), "leg": (230, 200, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def finf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["fin"] if face not in ("up",) else p["fin_light"], face), None


def fin_tipped(y_tip):
    """A brown spike fin with a pale tip above y_tip."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if y > y_tip:
            return tone(p["fin_tip"], face), None
        return finf(x, y, z, face, variant)
    return s


def legf(x, y, z, face, variant, **k):
    return tone(P(variant)["leg"], face), None


def round_eye(face, u, v, cu, cv, r, p, ring=False):
    """A big round dark eye with a white glint (and a pale ring if ring)."""
    d = math.hypot(u - cu, v - cv)
    if d < r:
        if math.hypot(u - cu + r * 0.35, v - cv - r * 0.35) < r * 0.3:
            return p["eye_white"]
        return p["eye"]
    if ring and d < r * 1.6:
        return p["eye_white"]
    return None
