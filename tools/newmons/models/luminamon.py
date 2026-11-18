"""Luminamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little light angel: a round white-and-pink body with a pink belly and little white mitten hands, a big white head
with large pink eyes and a tiny smile, a golden halo, and two long white feathered ears that sweep up into wings.
25 blocks tall.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 4
LOOK = "a round white-and-pink angel with large pink eyes, a golden halo and two long feathered ears sweeping up into wings"
BASE = {"white": (250, 250, 252), "white_dark": (200, 200, 214), "pink": (250, 180, 210), "pink_dark": (220, 120, 170),
        "eye": (220, 60, 140), "pupil": (40, 20, 30), "gold": (250, 220, 90)}
SHINY = {"pink": (170, 210, 250), "pink_dark": (100, 150, 220), "eye": (60, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 17.4)
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.4:
                return tone(p["eye"], face), None
        if abs(y - 14.8 + 0.2 * x * x) < 0.2 and abs(x) < 1.0:
            return tone(p["pupil"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("luminamon")
    top = m.bone("luminamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 7.0, 0), 5.0, skin(P, "pink", dark="pink_dark"), layers=4, squash=1.0)
    hd = m.bone("head", bd, (0, 12, 0))
    m.round_box(hd, 0, 0, 4.4, 3.8, 11.6, 20.0, headf, cut=2)
    hb = m.bone("ring_halo", hd, (0, 21, 0))
    for i in range(10):
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
        rod(m, hb, (5.0 * math.cos(a0), 21.0, 5.0 * math.sin(a0)), (5.0 * math.cos(a1), 21.0, 5.0 * math.sin(a1)), 1,
            solid(P, "gold", glow=True), extend=0.2, t2=1)
    for sx in (-1, 1):                                                               # feathered wing-ears
        pts = [(sx * 2.4, 19.6, 0), (sx * 4.0, 26.0, 1.0), (sx * 6.0, 31.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, feathers(P, "white", "white_dark"), extend=0.4)
        for j in range(4):
            spike(m, hd, (sx * (5.0 + j * 0.4), 29.0 - j * 1.4, 1.0), (sx, 0.3 - j * 0.2, 0.2), 1.2, 3.0,
                  feathers(P, "white", "white_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.6, 8.0, 0))
        rod(m, ab, (sx * 4.6, 8.0, 0), (sx * 7.6, 7.0, -1.0), 1, skin(P, "pink", dark="pink_dark"), extend=0.3, t2=2)
        m.round_box(ab, sx * 8.4, -1.0, 1.2, 1.2, 6.0, 8.0, solid(P, "white"), cut=0)
    return m
