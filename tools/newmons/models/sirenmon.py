"""Sirenmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the singer of the skies: a pale bird-spirit in a flowing white coat with a red beret and a red bow
tie, a shy hidden face, four great translucent ice-blue fin-wings edged with dots, little clawed feet, and streams of
musical staves curling round it. 25 blocks.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, feathers, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a pale bird-spirit singer in a white coat with a red beret and bow tie, four ice-blue fin-wings and curling musical staves"
BASE = {"white": (246, 248, 252), "white_dark": (190, 200, 220), "red": (180, 30, 40), "red_dark": (100, 10, 16),
        "fin": (190, 230, 250, 180), "black": (30, 30, 34), "staff": (40, 40, 46), "beak": (240, 200, 120)}
SHINY = {"white": (60, 56, 80), "white_dark": (30, 26, 40), "fin": (250, 200, 230, 180)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "white", "white_dark", axis="y", period=3.0)


def staffr(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y * 2.0) % 1.0 < 0.25:
        return tone(p["staff"], face), None
    return (255, 255, 255, 0), None


def build():
    m = Model("sirenmon")
    top = m.bone("sirenmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(6):                                                                   # flowing white coat
        r = 3.6 + i * 0.8
        m.round_box(bd, 0, 0, r, r * 0.8, 30.0 - (i + 1) * 3.6, 30.0 - i * 3.6 + 0.2, COAT, cut=1)
    m.round_box(bd, 0, 0, 4.0, 3.4, 30.0, 34.0, feathers(P, "white", "white_dark"), cut=1)
    m.box(bd, -1.6, 32.0, -3.8, 1.6, 33.6, -3.4, solid(P, "red"))                            # red bow tie
    hd = m.bone("head", bd, (0, 34, 0))
    ball(m, hd, (0, 37.0, -0.4), 3.6, feathers(P, "white", "white_dark"), layers=3)
    spike(m, hd, (0, 36.0, -3.6), (0, -0.4, -1), 1.0, 1.6, solid(P, "beak"), tip=0.8)
    m.round_box(hd, 0.6, 0, 4.0, 4.0, 39.0, 41.0, fabric(P, "red", "red_dark", axis="x"), cut=2)   # red beret
    ball(m, hd, (0.6, 41.0, 0), 2.0, fabric(P, "red", "red_dark", axis="x"), layers=1)
    for sx in (-1, 1):                                                                   # four fin-wings
        for j, (ang, ln) in enumerate(((30, 18.0), (-30, 14.0))):
            x0, x1 = sorted((sx * 3.0, sx * (3.0 + ln)))
            m.box(bd, x0, 28.0, 2.0 + j * 0.4, x1, 38.0, 2.0 + j * 0.4, solid(P, "fin", glow=True),
                  rotation=(0, -sx * 15, sx * ang), pivot=(sx * 3.0, 32.0, 2.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 1.4, 12.0, 0))
        rod(m, lg, (sx * 1.4, 12.0, 0), (sx * 1.6, 6.0, -1.0), 1, solid(P, "black"), extend=0.2, t2=2)
    for sx in (-1, 1):                                                                   # musical staves
        pts = [(sx * 6.0, 46.0, 4.0), (sx * 14.0, 40.0, 6.0), (sx * 12.0, 24.0, 4.0), (sx * 18.0, 12.0, 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, solid(P, "staff"), extend=0.2, t2=2)
            ball(m, bd, p1, 0.8, solid(P, "black"), layers=1)
    return m
