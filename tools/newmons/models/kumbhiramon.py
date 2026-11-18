"""Kumbhiramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
rat of the Twelve Devas: a small white mouse warrior with big round ears, a gold-and-white armoured body with a red
waist cord, two pairs of thin golden legs, two great bronze feathered wings, and on each side a long green ring-shaped
vajra staff with golden claw-tips. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import armour, feathers, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a small white mouse warrior in gold armour with big round ears, bronze feathered wings and two long green ring-vajra staves"
BASE = {"white": (246, 246, 250), "white_dark": (180, 180, 196), "gold": (230, 190, 80), "gold_dark": (150, 110, 24),
        "green": (60, 160, 80), "green_dark": (20, 90, 30), "bronze": (170, 120, 70), "bronze_dark": (100, 60, 30),
        "red": (210, 40, 40), "pink": (240, 160, 170), "eye": (220, 40, 40)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "green": (200, 60, 90), "green_dark": (120, 20, 40)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark")
MET = metal(P, "gold", dark="gold_dark")


def ringstaff(m, bone, c, sx):
    x, y, z = c
    for i in range(10):                                                              # green ring
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
        rod(m, bone, (x, y + 4.0 * math.sin(a0), z + 4.0 * math.cos(a0)), (x, y + 4.0 * math.sin(a1), z + 4.0 * math.cos(a1)),
            1, metal(P, "green", dark="green_dark"), extend=0.3, t2=1)
    rod(m, bone, (x - sx * 12.0, y, z), (x + sx * 8.0, y, z), 1, MET, extend=0, t2=1)
    for j in (-1, 1):
        spike(m, bone, (x + sx * 8.0, y, z), (sx, j * 0.4, 0), 0.9, 3.0, MET, tip=0.8)


def build():
    m = Model("kumbhiramon")
    top = m.bone("kumbhiramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0.6, 3.6, 3.0, 14.0, 22.0, GOLD, cut=1)
    m.round_box(bd, 0, 0.6, 3.8, 3.2, 14.0, 15.4, solid(P, "red"), cut=1)
    hd = m.bone("head", bd, (0, 22, 0))
    m.round_box(hd, 0, 0, 3.2, 3.0, 22.0, 28.4, skin(P, "white", dark="white_dark"), cut=1)
    m.round_box(hd, 0, -3.6, 1.6, 1.0, 23.0, 25.4, skin(P, "white", dark="white_dark"), cut=0)
    m.box(hd, -0.5, 24.0, -4.7, 0.5, 24.8, -4.5, solid(P, "pink"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 1.8), 26.0, -3.1, max(sx * 0.8, sx * 1.8), 26.8, -2.9, solid(P, "eye"))
        m.round_box(hd, sx * 4.0, 0.4, 2.4, 0.8, 26.0, 31.0, skin(P, "white", dark="pink"), cut=0)   # big round ears
    for side in (1, -1):                                                             # bronze feathered wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.0, 21.0, 3.0))
        feather_wing(m, wb, (side * 2.0, 21.0, 3.0), 14.0, 10.0, 2, feathers(P, "bronze", "bronze_dark"), side=side,
                     sweep=60, droop=-16.0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 20.0, 0))
        rod(m, ab, (sx * 3.6, 20.0, 0), (sx * 8.0, 19.0, -1.0), 1, GOLD, extend=0.3, t2=1)
        ringstaff(m, ab, (sx * 14.0, 19.0, -1.0), sx)
    for k_, (sz, nm_l, nm_r) in enumerate(((-1, "leg_left", "leg_right"), (1, "leg2_left", "leg2_right"))):
        for sx, nm in ((1, nm_l), (-1, nm_r)):                                       # thin golden legs
            lg = m.bone(nm, bd, (sx * 2.4, 15.0, sz * 1.6))
            kn = (sx * 6.0, 9.0, sz * 3.0)
            rod(m, lg, (sx * 2.4, 15.0, sz * 1.6), kn, 1, MET, extend=0.2, t2=1)
            rod(m, lg, kn, (sx * 6.6, 0.6, sz * 3.6), 1, MET, extend=0.2, t2=1)
    return m
