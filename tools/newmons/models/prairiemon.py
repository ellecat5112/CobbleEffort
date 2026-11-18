"""Prairiemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of sincerity: a sitting prairie dog with a sleek tan coat and cream belly,
whiskered alert face with a dark crest stripe, long silver drill-claw gauntlets on its forearms tipped with red
talons, big hind feet and a tail ending in a curved silver blade. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a sitting tan prairie dog with a cream belly, whiskers, silver drill-claw gauntlets tipped red and a curved blade tail"
BASE = {"tan": (190, 140, 70), "tan_dark": (120, 80, 30), "cream": (250, 236, 190), "cream_dark": (210, 190, 140),
        "dark": (80, 60, 40), "silver": (210, 214, 226), "silver_dark": (100, 104, 120), "red": (200, 40, 30),
        "black": (20, 20, 24), "white": (250, 250, 250)}
SHINY = {"tan": (150, 150, 160), "tan_dark": (80, 80, 96)}


def P(v):
    return pal(BASE, SHINY, v)


def coatf(x, y, z, face, variant, box=None, **k):
    if face == "north" and abs(x) < 3.6 and 8.0 < y < 30.0:
        return fur(P, "cream", "cream_dark", length=1.2)(x, y, z, face, variant, box=box, **k)
    return fur(P, "tan", "tan_dark", length=1.4)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 35.2) < 0.6:
                return tone(p["black"], face), None
        if math.hypot(x, y - 33.0) < 0.5:
            return tone(p["black"], face), None
    if face == "up" and abs(x) < 0.8:
        return tone(p["dark"], face), None
    return coatf(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("prairiemon")
    top = m.bone("prairiemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 12.0, 1.0), 7.6, coatf, layers=5, ry=7.0)                             # haunches
    m.round_box(bd, 0, 0, 5.4, 4.6, 16.0, 26.0, coatf, cut=2)
    m.round_box(bd, 0, -0.4, 4.0, 3.6, 25.6, 30.0, coatf, cut=1)
    hd = m.bone("head", bd, (0, 30, 0))
    m.round_box(hd, 0, -0.6, 3.2, 3.4, 30.0, 37.0, headf, cut=1)
    m.round_box(hd, 0, -3.8, 1.8, 1.4, 31.6, 34.4, headf, cut=0)
    for sx in (-1, 1):
        ball(m, hd, (sx * 2.6, 37.0, 0.4), 0.9, coatf, layers=1)
        for j in range(3):                                                               # whiskers
            m.box(hd, min(sx * 1.6, sx * 6.0), 32.6 + j * 0.6, -4.8, max(sx * 1.6, sx * 6.0), 32.6 + j * 0.6, -4.8,
                  solid(P, "black"), rotation=(0, 0, sx * (j - 1) * 10), pivot=(sx * 1.6, 32.6 + j * 0.6, -4.8))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # drill-claw gauntlets
        ab = m.bone(nm, bd, (sx * 4.6, 24.0, -2.0))
        rod(m, ab, (sx * 4.6, 24.0, -2.0), (sx * 4.0, 18.0, -6.0), 2, coatf, extend=0.3)
        m.round_box(ab, sx * 4.0, -6.6, 2.0, 2.0, 12.0, 19.0, STEEL, cut=1)
        for j in range(3):
            m.round_box(ab, sx * 4.0, -6.6, 2.2, 2.2, 13.0 + j * 2.0, 13.6 + j * 2.0, solid(P, "silver_dark"), cut=1)
        for f in range(3):
            spike(m, ab, (sx * 4.0 + (f - 1) * 1.2, 12.0, -6.6), ((f - 1) * 0.1, -1, -0.1), 1.0, 7.0, solid(P, "red"),
                  tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 6.0, 0))
        m.round_box(lg, sx * 5.4, -3.0, 2.2, 4.6, 0.0, 2.6, coatf, cut=1)                 # big hind feet
        for f in range(3):
            spike(m, lg, (sx * 5.4 + (f - 1) * 1.2, 0.8, -7.4), (0, -0.2, -1), 0.8, 1.6, solid(P, "cream"), tip=0.8)
    tl = m.bone("tail", bd, (0, 8, 7))
    rod(m, tl, (0, 8.0, 7.0), (0, 4.0, 13.0), 2, coatf, extend=0.3)
    m.box(tl, -0.4, 2.0, 12.0, 0.4, 14.0, 16.0, STEEL, rotation=(-30, 0, 0), pivot=(0, 4.0, 13.0))  # blade tail
    return m
