"""Soundbirdmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sonic bat-bird: a small round navy body with a red speaker-cone face, sweeping navy wings ripped
into scythe shapes and studded with red speaker eyes, and a forked tail. 1 block. Child stage.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a small round navy bat-bird with a red speaker-cone face and scythe-ripped wings studded with red speaker eyes"
BASE = {"navy": (40, 50, 110), "navy_dark": (14, 18, 50), "red": (210, 40, 50), "black": (24, 20, 24)}
SHINY = {"navy": (130, 40, 140), "navy_dark": (60, 14, 70), "red": (250, 200, 60)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = armour(P, "navy", "navy_dark")


def speakerf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    r = math.hypot(x, y - 10.0)
    return tone(p["black"] if r < 0.8 or abs(r - 2.0) < 0.3 else p["red"], face), None


def build():
    m = Model("soundbirdmon")
    top = m.bone("soundbirdmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 10.0, 0.6), 3.4, NAVY, layers=3)
    m.round_box(bd, 0, -3.4, 2.4, 0.8, 7.6, 12.4, speakerf, cut=0)                           # speaker face
    for sx in (-1, 1):                                                                   # scythe wings
        pts = [(sx * 3.0, 11.0, 1.0), (sx * 9.0, 15.0, 2.0), (sx * 16.0, 13.0, 3.0), (sx * 18.0, 8.0, 3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 2, NAVY, extend=0.3)
        m.box(bd, min(sx * 3.0, sx * 16.0), 7.0, 2.0, max(sx * 3.0, sx * 16.0), 13.0, 2.0, NAVY,
              rotation=(0, 0, sx * 8), pivot=(sx * 3.0, 11.0, 2.0))
        for j in range(3):
            ball(m, bd, (sx * (6.0 + j * 4.0), 11.0 + (1 - j) * 0.6, 1.4), 0.9, solid(P, "red"), layers=1)
    for sx in (-1, 1):
        spike(m, bd, (0, 8.0, 3.4), (sx * 0.3, -0.6, 1), 1.0, 5.0, NAVY, tip=0.8)          # forked tail
    return m
