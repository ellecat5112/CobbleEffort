"""Kakamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
music monkey: an orange monkey with a cream face and big blue eyes, a tall spiky crest of orange-red hair, big
headphones with skull-print speakers, a ragged orange jacket over red trousers with a black belt, grey fists and a long
curling tail with a red tuft. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, fur, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "an orange monkey with a spiky crest, big headphones, a ragged orange jacket, red trousers, grey fists and a curling tail"
BASE = {"orange": (240, 140, 40), "orange_dark": (170, 80, 14), "red": (220, 60, 40), "red_dark": (130, 20, 14),
        "cream": (250, 230, 200), "cream_dark": (210, 180, 150), "eye": (60, 150, 230), "pupil": (16, 16, 20),
        "grey": (110, 110, 120), "grey_dark": (60, 60, 70), "black": (30, 30, 34), "silver": (210, 214, 224)}
SHINY = {"orange": (120, 180, 240), "orange_dark": (40, 100, 180), "red": (240, 200, 60), "red_dark": (170, 130, 20)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "orange", "orange_dark", length=1.0)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.5, y - 21.4)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.1:
                return tone(p["eye"], face), None
        if abs(y - 19.0) < 0.3 and abs(x) < 1.0:
            return tone(p["red_dark"], face), None
    return skin(P, "cream", dark="cream_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kakamon")
    top = m.bone("kakamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 2.6, 2.0, 7.0, 10.4, fabric(P, "red", "red_dark"), cut=1)
    m.round_box(bd, 0, 0, 2.8, 2.2, 10.0, 11.0, solid(P, "black"), cut=1)
    m.round_box(bd, 0, 0, 2.8, 2.2, 10.8, 15.6, fabric(P, "orange", "orange_dark"), cut=1)
    hd = m.bone("head", bd, (0, 16, 0))
    m.round_box(hd, 0, 0, 3.4, 3.0, 15.6, 23.6, FUR, cut=1)
    m.round_box(hd, 0, -2.4, 2.8, 0.8, 16.4, 23.0, facef, cut=1)
    for i in range(5):                                                               # spiky crest
        spike(m, hd, ((i - 2) * 0.9, 23.2, -0.6 + abs(i - 2) * 0.6), ((i - 2) * 0.2, 1, 0.3), 1.4, 6.0 - abs(i - 2) * 1.2,
              strands(P, "orange", "red"), tip=0.8)
    for sx in (-1, 1):                                                               # headphones
        m.round_box(hd, sx * 3.8, 0, 0.8, 2.0, 18.4, 22.4, metal(P, "silver", dark="grey_dark"), cut=1)
        m.round_box(hd, sx * 4.7, 0, 0.2, 1.2, 19.4, 21.4, solid(P, "black"), cut=0)
    rod(m, hd, (-3.6, 22.4, 0), (3.6, 22.4, 0), 1, solid(P, "black"), extend=0, t2=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.8, 14.6, 0))
        rod(m, ab, (sx * 2.8, 14.6, 0), (sx * 4.6, 9.0, -0.6), 1, fabric(P, "orange", "orange_dark"), extend=0.3, t2=2)
        m.round_box(ab, sx * 5.0, -0.8, 1.8, 1.8, 6.0, 9.4, skin(P, "grey", dark="grey_dark"), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.4, 8.0, 0))
        rod(m, lg, (sx * 1.4, 8.0, 0), (sx * 1.6, 1.6, 0), 2, fabric(P, "red", "red_dark"), extend=0.3)
        m.round_box(lg, sx * 1.6, -0.8, 1.4, 2.0, 0.0, 1.6, solid(P, "black"), cut=0)
    tb = m.bone("tail", bd, (0, 9, 2))
    pts = [(0, 9.0, 2.2), (2.0, 10.0, 6.0), (4.0, 15.0, 8.0), (4.0, 20.0, 7.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=1)
    for j in range(3):
        spike(m, tb, pts[-1], ((j - 1) * 0.5, 1, 0), 1.0, 3.0, strands(P, "red", "red_dark"), tip=0.8)
    return m
