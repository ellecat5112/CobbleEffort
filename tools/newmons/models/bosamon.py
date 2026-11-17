"""Bosamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a shaggy baby. A round fluffy cream head, its brown face peeking out from under a thick fringe with
a little frown and sleepy eyes, two long flat ears tipped olive-green swept back, and a small round tail. Baby II.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(0.5, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a round fluffy cream baby with a brown face under a thick fringe and two long olive-tipped ears swept back"
BASE = {"cream": (246, 230, 170), "cream_dark": (196, 170, 100), "cream_tip": (255, 248, 220), "face": (130, 90, 60),
        "face_dark": (80, 50, 30), "olive": (130, 130, 40), "line": (40, 26, 20)}
SHINY = {"cream": (200, 220, 250), "cream_dark": (130, 150, 200), "cream_tip": (240, 248, 255), "olive": (200, 80, 140)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "cream", "cream_dark", tip="cream_tip", length=1.2)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.8) < 0.8 and abs(y - 8.8) < 0.18:                  # sleepy eye lines
                return tone(p["line"], face), None
        if abs(y - 6.6 - abs(x) * 0.5) < 0.18 and abs(x) < 0.8:                  # little frown
            return tone(p["line"], face), None
    return tone(p["face"], face), None


def earf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and z > box.lo[2] + box.size[2] - 3.0:
        return tone(p["olive"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bosamon")
    top = m.bone("bosamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 9.0, 0.6), 7.4, FUR, layers=6)
    m.round_box(bd, 0, -5.2, 3.8, 1.8, 4.6, 10.6, facef, cut=1)                    # the brown face
    for i in range(7):                                                            # the thick fringe
        x = -3.6 + i * 1.2
        spike(m, bd, (x, 11.6, -5.6), (0, -0.8, -0.5), 1.8, 2.4, FUR, tip=0.8)
    hd = m.bone("head", bd, (0, 14, 0))
    for sx in (-1, 1):                                                            # long flat ears swept back
        rod(m, hd, (sx * 2.0, 14.0, 0.0), (sx * 4.0, 21.0, 9.0), 3, earf, extend=0.4, t2=1)
    m.round_box(bd, 0, 7.6, 1.8, 1.4, 6.0, 9.6, FUR, cut=1)                       # tail
    return m
