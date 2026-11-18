"""Manekimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
lucky cat: a white beckoning cat with yellow eyes, a red bib collar with a golden bell, pink paw pads, a brown-tipped
tail and a brush-like tuft, holding up a red paper-lantern drum topped with a giant white beckoning paw. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, fur, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a white beckoning cat with yellow eyes, a red bib with a gold bell, holding up a red drum topped with a giant white paw"
BASE = {"white": (250, 250, 250), "white_dark": (196, 196, 206), "red": (210, 40, 40), "red_dark": (130, 14, 18),
        "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "pink": (240, 150, 170), "brown": (150, 100, 60),
        "eye": (240, 210, 40), "pupil": (24, 20, 20)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=0.7)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.6) < 0.8 and abs(y - 19.6) < 0.6:
                return tone(p["pupil"] if abs(x - sx * 1.6) < 0.25 else p["eye"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("manekimon")
    top = m.bone("manekimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.4, 3.0, 2.6, 6.0, 14.6, FUR, cut=1)
    m.round_box(bd, 0, -2.0, 2.4, 1.0, 12.0, 14.6, fabric(P, "red", "red_dark"), cut=1)        # red bib
    m.round_box(bd, 0, -3.2, 0.8, 0.8, 11.4, 12.8, metal(P, "gold", dark="gold_dark"), cut=0)
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, 0, 3.2, 3.0, 14.6, 22.0, headf, cut=1)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 21.6, 0.4), (sx * 0.4, 1, 0.2), 1.4, 2.6, FUR, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.0, 13.6, 0))
        rod(m, ab, (sx * 3.0, 13.6, 0), (sx * 4.4, 9.6 if sx < 0 else 18.0, -0.6), 1, FUR, extend=0.3, t2=1)
    ab = "arm_left"                                                                   # red drum + giant paw
    m.round_box(ab, 4.6, -0.6, 3.0, 3.0, 20.0, 27.0, fabric(P, "red", "red_dark"), cut=1)
    m.round_box(ab, 4.6, -0.6, 3.2, 3.2, 26.6, 27.6, metal(P, "gold", dark="gold_dark"), cut=1)
    m.round_box(ab, 4.6, -0.6, 4.0, 2.4, 27.6, 34.0, FUR, cut=2)
    for j in range(3):
        m.round_box(ab, 3.0 + j * 1.6, -2.8, 0.6, 0.2, 31.6, 33.4, solid(P, "pink"), cut=0)
    m.round_box(ab, 4.6, -2.8, 1.6, 0.2, 28.6, 30.6, solid(P, "pink"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 6.0, 0))
        rod(m, lg, (sx * 1.6, 6.4, 0), (sx * 1.8, 1.4, 0), 1, FUR, extend=0.3, t2=2)
        m.round_box(lg, sx * 1.8, -0.8, 1.2, 1.8, 0.0, 1.4, FUR, cut=0)
    tb = m.bone("tail", bd, (0, 7, 2))
    pts = [(0, 7.0, 2.4), (1.0, 3.0, 6.0), (2.0, 1.0, 10.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=1)
    spike(m, tb, pts[-1], (0.3, 0.4, 1), 1.4, 3.0, strands(P, "brown", "brown"), tip=0.8)
    return m
