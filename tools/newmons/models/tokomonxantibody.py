"""Tokomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Tokomon changed by the X-Antibody: a round pink piglet with a pointed arrowhead mark on
its brow, big shiny dark eyes and a happy mouth, little hoof feet, and two long pink ribbon-like ears folding up into
arrow tips. 0.5 blocks.

Front is -z, y is up. Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 25
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a round pink piglet with an arrowhead brow mark, big dark eyes and two long pink ribbon ears folding up into arrow tips"
BASE = {"pink": (250, 196, 210), "pink_dark": (210, 140, 160), "ribbon": (240, 150, 190), "eye": (30, 26, 40),
        "white": (255, 255, 255), "mouth": (190, 70, 90), "hoof": (210, 120, 140)}
SHINY = {"pink": (200, 220, 250), "pink_dark": (140, 160, 210), "ribbon": (130, 170, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 2.2, b - 8.0)
            if d < 1.1:
                return (p["white"] if math.hypot(a - sx * 2.2 + 0.3, b - 8.4) < 0.35 else p["eye"]), None
        if abs(b - 6.0) < 0.3 and abs(a) < 1.0:
            return p["mouth"], None
        if abs(a) < 2.0 - (b - 9.6) and 9.6 < b < 11.4 and abs(a) > 1.2 - (b - 9.6) * 0.6:
            return p["ribbon"], None
    return skin(P, "pink", dark="pink_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tokomonxantibody")
    top = m.bone("tokomonxantibody", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 7.0, 0.6), 5.4, bodyf, layers=5, squash=0.85, ry=4.6)
    for sx in (-1, 1):                                                                 # ribbon ears
        pts = [(sx * 1.6, 11.0, 0), (sx * 4.0, 17.0, 0.4), (sx * 2.0, 21.0, 0.6), (sx * 6.0, 24.0, 0.6)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, solid(P, "ribbon"), extend=0.3, t2=2)
        spike(m, bd, pts[-1], (sx * 0.8, 0.6, 0), 1.8, 2.4, solid(P, "ribbon"), tip=0.8)
    for sx, sz in ((1, -1), (-1, -1), (1, 1), (-1, 1)):
        m.round_box(top, sx * 2.6, sz * 2.4, 0.9, 0.9, 0.0, 2.6, solid(P, "hoof"), cut=0)
    return m
