"""Gorimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the cannon ape: a hulking yeti-gorilla with shaggy white fur over dark grey skin, a roaring fanged
face, a headset of tubes over one ear, a leather belt, huge knuckles and a mechanical arm cannon with a violet ribbed
sleeve. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking white-furred yeti-gorilla with dark skin, a roaring fanged face, a tube headset and a mechanical arm "
        "cannon")
BASE = {"fur": (240, 240, 246), "fur_dark": (180, 182, 200), "skin": (70, 76, 90), "skin_dark": (30, 34, 44),
        "violet": (130, 100, 180), "violet_dark": (70, 50, 110), "steel": (170, 176, 190), "steel_dark": (70, 76, 90),
        "mouth": (170, 30, 40), "tooth": (250, 250, 240), "eye": (60, 140, 220), "belt": (110, 70, 40),
        "belt_dark": (60, 36, 14)}
SHINY = {"fur": (90, 80, 70), "fur_dark": (50, 40, 30)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", length=1.6, density=2.0)
SKIN = skin(P, "skin", dark="skin_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("gorimon")
    top = m.bone("gorimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 1.0, 9.0, 7.0, 16.0, 36.0, FUR, cut=3)
    m.round_box(bd, 0, -4.6, 6.0, 2.0, 22.0, 34.0, SKIN, cut=2)                       # dark chest
    m.round_box(bd, 0, 1.0, 9.4, 7.4, 17.0, 19.0, leather(P, "belt", "belt_dark", stitch="steel"), cut=2)
    hd = m.bone("head", bd, (0, 36, -3))
    m.round_box(hd, 0, -3.0, 4.6, 4.4, 34.0, 44.0, FUR, cut=2)
    m.round_box(hd, 0, -6.6, 3.4, 1.6, 34.6, 41.0, SKIN, cut=1)
    m.box(hd, -2.4, 35.0, -8.4, 2.4, 38.0, -8.1, solid(P, "mouth"))
    for j in range(4):
        spike(m, hd, (-1.8 + j * 1.2, 38.0, -8.3), (0, -1, 0), 0.6, 1.4, solid(P, "tooth"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, 35.0, -8.3), (0, 1, 0), 0.8, 1.8, solid(P, "tooth"))
        m.box(hd, min(sx * 0.8, sx * 2.2), 39.4, -8.4, max(sx * 0.8, sx * 2.2), 40.2, -8.2, solid(P, "eye"))
    for j in range(3):                                                                   # tube headset
        rod(m, hd, (-4.6, 40.0 - j * 1.4, -1.0), (-6.0, 36.0 - j * 1.4, 2.0), 1, STEEL, extend=0.2, t2=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 33.0, 0))
        rod(m, ab, (sx * 9.0, 33.0, 0), (sx * 15.0, 22.0, -4.0), 6, FUR, extend=0.6)
        if sx > 0:
            rod(m, ab, (15.0, 22.0, -4.0), (15.0, 10.0, -6.0), 5, FUR, extend=0.6)
            m.round_box(ab, 15.0, -7.0, 3.6, 3.6, 4.0, 10.0, SKIN, cut=1)               # huge knuckles
        else:
            rod(m, ab, (-15.0, 22.0, -4.0), (-17.0, 20.0, -14.0), 6, metal(P, "violet", dark="violet_dark"), extend=0.4)
            rod(m, ab, (-17.0, 20.0, -14.0), (-18.0, 20.0, -22.0), 7, STEEL, extend=0)    # arm cannon
            m.round_box(ab, -18.0, -22.4, 2.4, 0.6, 18.0, 22.0, solid(P, "skin_dark"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 16.0, 0))
        rod(m, lg, (sx * 5.0, 17.0, 0), (sx * 6.0, 4.0, -1.0), 5, FUR, extend=0.6)
        m.round_box(lg, sx * 6.0, -2.0, 3.6, 4.6, 0.0, 4.0, SKIN, cut=1)
    return m
