"""Kokuwamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little machine stag beetle: a grey-steel robot insect with a pincer-jaw head and red eyes, a ribbed armoured body, two
arms ending in plug-claws and electric-plug prongs, four jointed legs with clamp feet and a crackle of yellow sparks
between its jaws. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 2.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a grey-steel robot stag beetle with a pincer-jaw head, red eyes, plug-claw arms, clamp feet and yellow sparks"
BASE = {"grey": (120, 124, 136), "grey_dark": (50, 52, 60), "grey_light": (190, 194, 206), "red": (220, 40, 40),
        "spark": (250, 230, 70), "silver": (210, 214, 224), "silver_dark": (100, 104, 116), "black": (24, 24, 30)}
SHINY = {"grey": (200, 160, 60), "grey_dark": (120, 80, 14), "grey_light": (250, 220, 140)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "grey", "grey_dark", light="grey_light", trim="black", trim_w=0.2, rivets=True)
SIL = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("kokuwamon")
    top = m.bone("kokuwamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 1.0, 3.6, 4.0, 7.0, 15.0, ARM, cut=1)
    hd = m.bone("head", bd, (0, 15, -1))
    m.round_box(hd, 0, -1.0, 3.0, 3.0, 15.0, 20.0, ARM, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 17.0, -4.1, max(sx * 0.6, sx * 2.0), 17.8, -3.9, solid(P, "red", glow=True))
        pts = [(sx * 2.0, 19.6, -1.6), (sx * 3.6, 24.0, -2.4), (sx * 2.0, 27.0, -3.0)]   # pincer jaws
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, ARM, extend=0.3, t2=2)
    m.round_box(hd, 0, -2.6, 1.0, 1.0, 25.6, 27.0, solid(P, "spark", glow=True), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # plug-claw arms
        ab = m.bone(nm, bd, (sx * 3.6, 13.0, -1.0))
        rod(m, ab, (sx * 3.6, 13.0, -1.0), (sx * 7.6, 12.0, -3.0), 1, ARM, extend=0.3, t2=2)
        m.round_box(ab, sx * 8.4, -3.0, 1.2, 1.2, 10.6, 13.2, ARM, cut=0)
        for j in (-1, 1):
            rod(m, ab, (sx * 9.4, 12.0 + j * 0.8, -3.0), (sx * 11.4, 12.0 + j * 0.8, -3.0), 1, SIL, extend=0, t2=1)
    for k_, (sz, nm_l, nm_r) in enumerate(((-1, "leg_left", "leg_right"), (1, "leg2_left", "leg2_right"))):
        for sx, nm in ((1, nm_l), (-1, nm_r)):                                       # four jointed legs
            lg = m.bone(nm, bd, (sx * 3.0, 8.0, sz * 2.0))
            kn = (sx * 5.0, 5.0, sz * 3.0)
            rod(m, lg, (sx * 3.0, 8.0, sz * 2.0), kn, 1, ARM, extend=0.3, t2=2)
            rod(m, lg, kn, (sx * 5.6, 1.0, sz * 3.4), 1, ARM, extend=0.3, t2=2)
            m.round_box(lg, sx * 5.6, sz * 3.4 - 0.6, 1.2, 1.4, 0.0, 1.2, SIL, cut=0)
    return m
