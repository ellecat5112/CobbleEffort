"""Junkmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
scrap-heap mole: a stitched brown plush mole in a scuffed yellow hard hat with green eyes and buck teeth, riding on
two chunky black tyres, a drill-bit claw on one arm, a plug-cord tail, a bandaged scrap cannon with a green barrel on
its back and stray nuts, bolts and springs flying round it. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 0}
LOOK = "a stitched brown plush mole in a yellow hard hat riding on black tyres, with a drill claw and a scrap cannon on its back"
BASE = {"brown": (170, 120, 70), "brown_dark": (100, 66, 34), "tan": (230, 200, 150), "yellow": (240, 200, 50),
        "yellow_dark": (170, 130, 20), "green": (60, 150, 60), "green_dark": (24, 80, 24), "black": (36, 36, 40),
        "grey": (150, 150, 160), "steel": (210, 214, 224), "steel_dark": (100, 104, 116), "eye": (60, 180, 80),
        "tooth": (250, 250, 240), "stitch": (60, 40, 20), "red": (200, 50, 40)}
SHINY = {"brown": (110, 110, 130), "brown_dark": (60, 60, 76), "yellow": (240, 120, 40), "yellow_dark": (160, 60, 10)}


def P(v):
    return pal(BASE, SHINY, v)


def plushf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.8, y - 14.4) < 0.8:
                return tone(p["eye"], face), None
        if abs(y - 12.0) < 0.9 and abs(abs(x) - 0.5) < 0.4:
            return tone(p["tooth"], face), None
    if abs(x - 1.4) < 0.15 and (y % 1.0) < 0.5:
        return tone(p["stitch"], face), None
    return fabric(P, "brown", "brown_dark", period=1.4)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("junkmon")
    top = m.bone("junkmon", None, (0, 0, 0))
    for sx in (-1, 1):                                                               # chunky tyres
        for t in range(6):
            ang = math.pi * t / 6
            m.box(top, min(sx * 4.0, sx * 6.6), 4.0 - 4.0 * math.sin(ang) * 0.0 + 0.0, -4.0, max(sx * 4.0, sx * 6.6),
                  8.0, 4.0, metal(P, "black", dark="black"), rotation=(math.degrees(ang), 0, 0), pivot=(sx * 5.3, 4.0, 0))
        m.round_box(top, sx * 6.8, 0, 0.4, 1.6, 2.4, 5.6, solid(P, "grey"), cut=0)
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 11.0, 0), 5.6, plushf, layers=5)
    hd = m.bone("head", bd, (0, 16, 0))
    m.round_box(hd, 0, 0, 4.0, 4.0, 16.0, 19.0, metal(P, "yellow", dark="yellow_dark"), cut=2)   # hard hat
    m.round_box(hd, 0, -1.0, 4.6, 5.0, 15.6, 16.4, metal(P, "yellow", dark="yellow_dark"), cut=2)
    m.round_box(hd, 0, -4.1, 2.6, 0.2, 17.2, 17.8, solid(P, "green"), cut=0)
    m.round_box(bd, 0, -5.4, 1.4, 1.0, 10.6, 12.6, skin(P, "tan", dark="brown"), cut=0)          # snout
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 11.0, -1.0))
        if sx < 0:                                                                   # drill-bit claw
            spike(m, ab, (sx * 5.0, 9.0, -3.0), (-0.3, -0.4, -1), 2.4, 6.0, metal(P, "steel", dark="steel_dark"), tip=0.8)
        else:
            m.round_box(ab, sx * 5.6, -2.0, 1.4, 1.4, 8.0, 10.6, fabric(P, "brown", "brown_dark"), cut=0)
    cb = m.bone("cannon", bd, (0, 14, 4))                                             # scrap cannon
    rod(m, cb, (0, 12.0, 5.0), (-2.0, 20.0, 1.0), 3, metal(P, "steel", dark="steel_dark"), extend=0.4)
    rod(m, cb, (-2.0, 20.0, 1.0), (-3.0, 24.0, -1.0), 3, solid(P, "green"), extend=0)
    m.round_box(cb, -3.0, -1.0, 1.8, 1.8, 23.6, 24.4, solid(P, "black"), cut=0)
    m.round_box(cb, 1.4, 6.0, 1.6, 1.0, 13.0, 16.0, solid(P, "tan"), cut=0)                       # bandage patch
    for j, (px, py, pz) in enumerate(((-6.0, 24.0, 0.0), (-5.0, 21.0, -4.0), (2.0, 25.0, -2.0))):    # flying scrap
        m.round_box(cb, px, pz, 0.9, 0.9, py - 0.9, py + 0.9, metal(P, "grey", dark="black"), cut=0)
    tb = m.bone("tail", bd, (0, 8, 5))
    rod(m, tb, (0, 8.0, 5.0), (2.0, 3.0, 9.0), 1, solid(P, "black"), extend=0.2, t2=1)
    m.round_box(tb, 2.0, 9.4, 0.8, 0.8, 2.0, 3.4, solid(P, "red"), cut=0)
    return m
