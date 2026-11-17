"""Copymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official pixel
art on wikimon.net): the copycat. A small rosy-pink figure with a pointed head curl, two big round goggle-ring eyes,
a stubby snout, a little coat with its hands in its pockets, and short legs. Child stage.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a small rosy-pink figure with a pointed head curl, two big goggle-ring eyes, a little coat and hands in its pockets"
BASE = {"pink": (230, 160, 170), "pink_dark": (180, 100, 120), "pink_light": (250, 210, 216), "coat": (210, 130, 150),
        "coat_dark": (160, 80, 100), "ring": (170, 80, 100), "eye": (250, 236, 240)}
SHINY = {"pink": (160, 200, 240), "pink_dark": (100, 140, 200), "pink_light": (210, 230, 255), "coat": (120, 170, 230),
         "coat_dark": (70, 110, 180), "ring": (60, 100, 170)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "pink", dark="pink_dark", light="pink_light", var=0.03)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.4, y - 20.4)
            if d < 2.0:
                return tone(p["ring"] if d > 1.4 or d < 0.5 else p["eye"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("copymon")
    top = m.bone("copymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 3.6, 3.0, 6.0, 15.0, fabric(P, "coat", "coat_dark", axis="y", period=1.6), cut=1)
    for sx in (-1, 1):                                                      # hands in pockets
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 3.6, 13.0, 0))
        rod(m, ab, (sx * 3.6, 13.0, 0), (sx * 3.8, 9.0, -1.6), 2, fabric(P, "coat", "coat_dark"), extend=0.4)
    hd = m.bone("head", bd, (0, 15, 0))
    ball(m, hd, (0, 20.0, 0), 5.0, headf, layers=5)
    m.box(hd, -1.4, 16.6, -5.8, 1.4, 18.4, -4.4, SKIN)                     # stubby snout
    pts = [(0, 24.6, 0), (1.6, 27.0, 0.6), (3.6, 27.4, 1.0), (4.0, 25.6, 1.0)]  # pointed head curl
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 2, SKIN, extend=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 7.0, 0))
        rod(m, lg, (sx * 1.8, 7.0, 0), (sx * 2.0, 1.4, 0), 2, SKIN, extend=0.3)
        m.box(lg, sx * 2.0 - 1.4, 0.0, -2.4, sx * 2.0 + 1.4, 1.6, 1.0, SKIN)
    return m
