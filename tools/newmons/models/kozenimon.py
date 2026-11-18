"""Kozenimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
one-coin Digimon: a round silver coin stamped with a big "1", two black button eyes, stubby gold-ringed limbs with
white mitten hands and white feet. Baby II stage, half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a round silver coin stamped with a big 1, black button eyes and stubby limbs with white hands and feet"
BASE = {"silver": (210, 214, 224), "silver_dark": (110, 114, 126), "black": (24, 24, 30), "white": (250, 250, 250),
        "gold": (230, 190, 70)}
SHINY = {"silver": (240, 200, 90), "silver_dark": (170, 120, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def coinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(x - 0.6) < 0.4 and 7.0 < y < 12.0 or (abs(y - 11.4 - (x - 0.6) * 0.8) < 0.3 and -0.6 < x < 0.6):
            return tone(p["silver_dark"], face), None
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.6, y - 9.6) < 0.8:
                return tone(p["black"], face), None
        if abs(math.hypot(x, y - 9.6) - 4.4) < 0.25:
            return tone(p["silver_dark"], face), None
    return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kozenimon")
    top = m.bone("kozenimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for i in range(8):                                                               # the coin: a disc of slabs
        ang = 180.0 * i / 8
        m.box(bd, -5.0, 8.4, -1.0, 5.0, 10.8, 1.0, coinf, rotation=(0, 0, ang), pivot=(0, 9.6, 0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 9.0, 0))
        rod(m, ab, (sx * 4.6, 9.0, 0), (sx * 6.4, 8.0, 0), 1, solid(P, "gold"), extend=0, t2=1)
        m.round_box(ab, sx * 7.4, 0, 1.2, 1.2, 7.0, 9.4, solid(P, "white"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 4.0, 0))
        rod(m, lg, (sx * 1.8, 5.0, 0), (sx * 2.0, 2.0, 0), 1, solid(P, "gold"), extend=0, t2=1)
        m.round_box(lg, sx * 2.2, -0.6, 1.4, 1.8, 0.0, 2.0, solid(P, "white"), cut=0)
    return m
