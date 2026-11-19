"""Curler Rotom (Electric/Fairy), after the user's Rotom doodle sheet (artist not named): Rotom inside a curling
wand. A bronze-brown handle with dizzy spiral eyes and a dotted grin, a hanging loop on top, a grey heating rod
wound with a spiral coming out of its base, and a black cord curling away.

Front is -z, y is up. 28 units tall; about 0.9 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _rotomform import palette, solid
from _route import tone

P = palette({"aura": (240, 150, 210), "aura_light": (255, 225, 245), "bronze": (176, 120, 60), "bronze_dark": (120, 78, 34)},
            {"bronze": (150, 160, 200), "bronze_dark": (90, 100, 140)})
HEIGHT = 28
SCALE = round(0.9 * 16 / HEIGHT, 3)
HITBOX = [0.6, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = "a bronze curling wand with dizzy spiral eyes, a dotted grin, a hanging loop and a grey spiral heating rod"


def handle(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - 1.3 * sx, y - 21.0
            d = math.hypot(dx, dy)
            if d < 1.2:
                a = math.atan2(dy, dx)
                return (p["black"] if abs(((d * 3.2 - a / math.pi) % 1.0) - 0.5) < 0.22 else p["white"]), None   # spiral eyes
        if 17.6 <= y <= 18.8 and abs(x) <= 1.8:
            return (p["black"] if abs((x + 1.8) % 0.9 - 0.45) < 0.25 else p["bronze_dark"]), None               # dotted grin
    return tone(p["bronze"], face), None


def wand(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["grey_dark"] if (y * 1.4 + math.atan2(z, x) / math.pi) % 1.0 < 0.3 else p["grey_light"], face), None


def build() -> Model:
    m = Model("rotom_curler")
    top = m.bone("rotom_curler", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 2.8, 2.6, 14, 25, handle, cut=0.9)                          # the handle (its face)
    pts = [(math.sin(a) * 2.2, 27 + math.cos(a) * 2.2, 0.6) for a in [i * math.pi / 4 for i in range(-3, 4)]]
    for a, b in zip(pts, pts[1:]):
        rod(m, bd, a, b, 0.8, solid(P, "bronze_dark"), extend=0.3)                  # hanging loop
    m.round_box(bd, 0, 0, 1.4, 1.4, 1, 14, wand, cut=0.5)                            # heating rod
    m.round_box(bd, 0, 0, 1.0, 1.0, 0, 1.2, solid(P, "black"), cut=0.3)
    cord = m.bone("tail", bd, (2.4, 15, 1))
    pts = [(2.4, 15, 1.5), (5, 13, 3), (6, 9, 5), (4, 6, 7), (6, 3, 9)]
    for a, b in zip(pts, pts[1:]):
        rod(m, cord, a, b, 0.9, solid(P, "black"), extend=0.4)
    return m
