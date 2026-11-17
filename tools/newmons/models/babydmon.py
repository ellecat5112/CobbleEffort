"""Babydmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
baby dragon shaped like a seahorse. A green body with an orange-yellow banded belly, a round head with a big violet
eye, two pink-tipped horn-ears, tiny green wing fins and a long tail curling into a pale blue spiral. Tiny.

Front is -z, y is up. 30 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, local, plane, scales, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(0.5, HEIGHT, 0.4)
KIND = "floater"
K = 4
LOOK = ("a seahorse-shaped baby dragon: green with a yellow banded belly, a big violet eye, pink-tipped horn-ears, tiny "
        "wing fins and a tail curling into a pale blue spiral")
BASE = {"green": (70, 180, 80), "green_dark": (30, 110, 40), "belly": (250, 200, 80), "belly_dark": (220, 150, 40),
        "pink": (240, 80, 150), "black": (40, 40, 50), "tail": (170, 220, 250), "eye": (160, 100, 220),
        "pupil": (30, 20, 40), "white": (250, 250, 250)}
SHINY = {"green": (80, 140, 230), "green_dark": (30, 70, 160), "tail": (250, 200, 230)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "green", dark="green_dark", var=0.03)


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.6:
        band = (y % 1.4) / 1.4
        return tone(p["belly_dark"] if band < 0.18 else p["belly"], face), None
    return BODY(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 1.0, y - 24.0, 1.6, "eye")
        if c is not None:
            return c, None
    return BODY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("babydmon")
    top = m.bone("babydmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    for i in range(5):                                           # the body, bulging at the belly
        r = 3.4 + math.sin((i + 0.5) / 5 * math.pi) * 1.0
        m.round_box(bd, 0, 0.4 - i * 0.2, r, r * 0.9, 10.0 + i * 2.4, 12.6 + i * 2.4, bellyf, cut=1)
    hd = m.bone("head", bd, (0, 22, 0))
    ball(m, hd, (0, 24.0, 0.0), 3.8, headf, layers=4)
    m.box(hd, -1.8, 21.6, -7.0, 1.8, 24.0, -2.6, BODY)                                   # snout
    for sx in (-1, 1):                                           # horn-ears
        rod(m, hd, (sx * 1.6, 27.0, 1.0), (sx * 3.4, 30.0, 3.0), 2, solid(P, "black"), extend=0.2)
        spike(m, hd, (sx * 3.4, 30.0, 3.0), (sx * 0.4, 0.6, 0.6), 1.4, 1.8, solid(P, "pink"))
        m.box(bd, min(sx * 3.6, sx * 7.0), 15.0, 0.0, max(sx * 3.6, sx * 7.0), 18.0, 0.0, BODY,
              rotation=(0, sx * 20, sx * 20), pivot=(sx * 3.6, 16.0, 0))                 # wing fins
    tl = m.bone("tail", bd, (0, 10, 0))
    p = (0.0, 10.0, 0.0)
    for j in range(12):                                          # the tail curling into a spiral
        ang = j * 0.6
        r = 3.6 - j * 0.24
        q = (0.0, 6.0 - r * math.cos(ang) * 0.9 - j * 0.2, 2.0 + r * math.sin(ang))
        rod(m, tl, p, q, max(1, round(2.6 - j * 0.18)), solid(P, "tail") if j > 4 else BODY, extend=0.3)
        p = q
    return m
