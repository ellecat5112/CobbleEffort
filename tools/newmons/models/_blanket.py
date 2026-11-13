"""Shared colours and shaders for the pigs-in-a-blanket line (Wrapiglet, Croissoar): baked crescent-roll dough with
golden layered ridges, and little pigs. After the fakemon art from the r/fakemon community the user shared (artist
not named); names and models are our own.

Shiny: pain au chocolat (dark chocolate-brown crust, cocoa layers) and a pale cream pig with a rosy snout.
"""
from __future__ import annotations

import math

from _boxmodel import mix
from _route import pal, tone

BASE = {"dough": (232, 170, 84), "dough_light": (250, 210, 128), "dough_dark": (190, 120, 52), "crumb": (246, 220, 170),
        "pig": (222, 104, 120), "pig_dark": (180, 70, 92), "pig_tan": (234, 188, 140), "pig_tan_dark": (200, 150, 104),
        "snout": (170, 66, 56), "nostril": (84, 30, 30), "hoof": (156, 62, 54), "eye": (34, 24, 24),
        "ear": (246, 222, 180), "tie": (176, 60, 52)}
SHINY = {"dough": (128, 78, 46), "dough_light": (170, 112, 70), "dough_dark": (82, 46, 28), "crumb": (210, 170, 130),
         "pig": (246, 228, 214), "pig_dark": (210, 186, 172), "pig_tan": (246, 232, 214), "pig_tan_dark": (214, 196, 176),
         "snout": (236, 150, 160), "nostril": (150, 70, 80), "hoof": (220, 140, 140), "ear": (252, 240, 226),
         "tie": (230, 120, 130)}


def P(v):
    return pal(BASE, SHINY, v)


def layers(t, n=3.2):
    """Croissant layering: 0..1 across each layer (darker in the creases between layers)."""
    return (t / n) % 1.0


def dough_shade(p, t, face):
    """Golden baked dough: lighter in the middle of each layer, darker in the creases, glossy on top."""
    c = mix(p["dough"], p["dough_light"], 0.55 * math.sin(math.pi * t) ** 0.6)
    if t < 0.12 or t > 0.92:
        c = mix(c, p["dough_dark"], 0.55)                                  # thin crease between layers
    if face == "up":
        c = mix(c, p["dough_light"], 0.35)
    return tone(c, face)


def snoutf(cx, cy, w, h):
    """A flat pig snout on a north face centred at (cx, cy): two dark nostrils."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if math.hypot((x - cx - sx * w * 0.3) / (w * 0.13), (y - cy) / (h * 0.22)) < 1:
                    return p["nostril"], None
        return tone(p["snout"], face), None
    return s


def hooff(x, y, z, face, variant, **k):
    return tone(P(variant)["hoof"], face), None
