"""Shared colours and parts for the water starter line (Fangfosh, Fishugly, Creepish), after the art of the A. Fakemon
fanpage (names kept): a grimacing little fish on frog legs, a gangly fish-headed walker on long fin legs and a creepy
lagoon fish-man with a black frill.

Shiny: violet fins and limbs, lilac skin, rose heads, magenta eyes.
"""
from __future__ import annotations

import math

from _afake import CUT, ramp_of, solid_of
from _route import pal, tone

BASE = {"cyan": (172, 224, 222), "cyan_dark": (124, 190, 196), "blue": (72, 152, 222), "blue_dark": (42, 104, 182),
        "black": (30, 32, 40), "white": (250, 250, 246), "eye": (44, 74, 164), "pupil": (16, 18, 34),
        "green": (134, 204, 172), "green_dark": (62, 112, 92), "cream": (238, 228, 198), "mouth": (40, 30, 40)}
SHINY = {"cyan": (214, 196, 238), "cyan_dark": (180, 160, 214), "blue": (156, 92, 204), "blue_dark": (110, 60, 160),
         "green": (214, 130, 168), "green_dark": (130, 60, 96), "eye": (200, 60, 120)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)
ramp = ramp_of(P)


def grimace(p, x, y, x_half, y0, y1, pointed):
    """A wide mouth full of teeth on a front face: square teeth (pointed=False) or a zigzag of fangs. -> colour/None."""
    if abs(x) > x_half or not (y0 <= y <= y1):
        return None
    if abs(x) > x_half - 0.3 or y - y0 < 0.3 or y1 - y < 0.3:
        return p["black"]                                                    # the lips' dark outline
    if not pointed:
        return p["black"] if ((x + x_half) % 1.2) < 0.18 or abs(y - (y0 + y1) / 2) < 0.12 else p["white"]
    ph = ((x + x_half) / 1.0) % 1.0
    h = (y1 - y0) * 0.42
    if (y1 - 0.3 - y) < h * (1 - abs(2 * ph - 1)) or (y - y0 - 0.3) < h * (1 - abs(2 * ((ph + 0.5) % 1.0) - 1)):
        return p["white"]
    return p["mouth"]


def ring_eye(p, dx, dy, r):
    """A black-ringed white eye with a black bar across it (Fishugly, Creepish). -> colour/None."""
    d = math.hypot(dx, dy)
    if d > r:
        return None
    if d > r * 0.7 or abs(dy) < r * 0.14:
        return p["black"]
    return p["white"]


def fin(shape, colour):
    """A cut-out fin on a plane: shape(a, b) -> bool on the plane's two in-plane coordinates."""
    def s(x, y, z, face, variant, box=None, **k):
        a, b = (z, y) if box.size[0] == 0 else (x, y)
        if not shape(a, b):
            return CUT, None
        return tone(colour(P(variant), a, b), face), None
    return s
