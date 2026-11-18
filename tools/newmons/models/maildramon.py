"""Maildramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor Digimon of sincerity: a silver armoured griffin-dragon standing on four legs with gold-ringed joints and gold
talons, a long blue-plumed beaked head under a gold-crested helm, a curved breastplate with a red gem, and two great
golden wings rising above it. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import armour, feathers, gem, metal, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.6)
KIND = "quadruped"
K = 3
LOOK = "a silver armoured griffin-dragon on four legs with gold talons, a blue-plumed beaked head, a red chest gem and great golden wings"
BASE = {"silver": (220, 224, 234), "silver_dark": (110, 116, 130), "gold": (240, 200, 70), "gold_dark": (160, 120, 20),
        "gold_light": (255, 240, 170), "blue": (60, 90, 200), "blue_dark": (20, 40, 120), "red": (220, 40, 40),
        "red_light": (255, 160, 150), "black": (30, 30, 34), "eye": (40, 40, 40)}
SHINY = {"silver": (80, 80, 96), "silver_dark": (30, 30, 40)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def build():
    m = Model("maildramon")
    top = m.bone("maildramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 1.0, 4.6, 7.0, 10.0, 20.0, ARM, cut=2)
    m.round_box(bd, 0, -6.4, 3.4, 1.6, 14.0, 24.0, ARM, cut=1)                         # curved breastplate
    m.round_box(bd, 0, -8.1, 1.2, 0.4, 18.0, 20.4, gem(P, "red", "red_light"), cut=0)
    hd = m.bone("head", bd, (0, 26, -5))
    rod(m, hd, (0, 22.0, -5.0), (0, 30.0, -6.0), 2, ARM, extend=0.6)
    m.round_box(hd, 0, -6.0, 2.2, 3.0, 29.0, 34.0, ARM, cut=1)
    spike(m, hd, (0, 31.0, -9.0), (0, -0.4, -1), 1.4, 3.0, GOLD, tip=0.8)
    spike(m, hd, (0, 34.0, -6.0), (0, 1, 0), 1.0, 4.0, GOLD, tip=0.8)                         # gold crest
    for j in range(5):                                                               # blue plume
        rod(m, hd, (0, 33.0, -4.0), (0.6 * (j - 2), 29.0 - j * 0.6, 2.0 + j * 0.6), 1, strands(P, "blue", "blue_dark"),
            extend=0.2, t2=1)
    for side in (1, -1):                                                             # great golden wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 20.0, 2.0))
        feather_wing(m, wb, (side * 3.0, 20.0, 2.0), 14.0, 8.0, 2, feathers(P, "gold", "gold_dark", tip="gold_light"),
                     side=side, sweep=70, droop=-24.0)
    for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                       (-1, 1, "leg_back_right")):
        lg = m.bone(nm, bd, (sx * 3.4, 11.0, sz * 4.0))
        kn = (sx * 4.0, 5.0, sz * 4.0 - 1.0)
        rod(m, lg, (sx * 3.4, 11.0, sz * 4.0), kn, 2, ARM, extend=0.4)
        m.round_box(lg, kn[0], kn[2], 1.6, 1.6, kn[1] - 0.6, kn[1] + 0.8, GOLD, cut=0)
        rod(m, lg, kn, (sx * 4.0, 1.0, sz * 4.0), 1, ARM, extend=0.3, t2=2)
        for j in range(3):
            spike(m, lg, (sx * 4.0 + (j - 1) * 0.9, 0.8, sz * 4.0 - 1.0), ((j - 1) * 0.3, -0.2, -1), 0.9, 2.4, GOLD, tip=0.8)
    return m
