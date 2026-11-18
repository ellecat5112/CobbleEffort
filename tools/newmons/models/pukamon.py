"""Pukamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little grey sea-lizard baby with big blue eyes, two tiny fangs, a flickering orange flame crest on
its head, flipper arms, a pale belly patch and a curled tail fin. 0.5 blocks.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a little grey sea-lizard baby with big blue eyes, tiny fangs, an orange flame crest, flipper arms and a curled tail fin"
BASE = {"grey": (150, 146, 140), "grey_dark": (90, 86, 80), "belly": (220, 236, 246), "eye": (40, 70, 160),
        "white": (255, 255, 255), "black": (20, 20, 24), "flame": (240, 110, 30), "flame_tip": (250, 190, 60)}
SHINY = {"grey": (110, 170, 200), "grey_dark": (50, 100, 140)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "grey", dark="grey_dark", var=0.03)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.6, y - 11.4)
            if d < 0.35:
                return tone(p["white"], face), None
            if d < 1.0:
                return tone(p["eye"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pukamon")
    top = m.bone("pukamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.round_box(bd, 0, 1.0, 2.6, 2.4, 2.0, 8.0, SKIN, cut=1)
    m.round_box(bd, 0, -1.2, 1.6, 1.0, 3.0, 6.0, solid(P, "belly"), cut=0)
    hd = m.bone("head", bd, (0, 8, 0))
    ball(m, hd, (0, 11.0, -0.6), 3.2, headf, layers=3, ry=2.8)
    m.round_box(hd, 0, -4.0, 2.4, 1.4, 8.8, 10.6, SKIN, cut=0)                            # snout
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.2, 8.8, -5.0), (0, -1, 0), 0.8, 1.0, solid(P, "white"), tip=0.8)
        spike(m, bd, (sx * 2.4, 6.0, -0.6), (sx * 0.8, -0.6, -0.4), 1.4, 4.0, SKIN, tip=0.8)   # flippers
    for j in range(3):                                                                   # flame crest
        spike(m, hd, (0, 13.6, -0.4 + j * 0.8), (0.2 * (j - 1), 1, 0.3), 1.2, 3.0 - j * 0.6,
              solid(P, "flame" if j else "flame_tip", glow=True), tip=0.8)
    tl = m.bone("tail", bd, (0, 3, 3))
    pts = [(0, 3.0, 3.0), (0, 1.0, 6.0), (1.6, 2.0, 8.6)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, SKIN, extend=0.2, t2=2)
    spike(m, tl, pts[-1], (0.6, 1, 0.4), 1.2, 2.4, solid(P, "black"), tip=0.8)
    return m
