"""Harpymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
Armor harpy of courage-turned-sincerity: a slender figure in white with great white feathered wings for arms, a
silver helmet with a red feather crest, a red-and-silver chest plate, a dark face mask, long white tail streamers and
grey talons. Adult stage, 15 blocks tall.

Front is -z, y is up. 60 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender white harpy with great feathered wings, a silver helmet with a red crest, a red-and-silver chest plate "
        "and long white tail streamers")
BASE = {"white": (246, 246, 250), "white_dark": (190, 192, 206), "silver": (210, 214, 224), "silver_dark": (110, 114, 126),
        "red": (200, 30, 40), "red_dark": (120, 10, 16), "face": (190, 140, 100), "grey": (90, 90, 100), "gold": (230, 200, 90)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "red": (60, 140, 220)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fabric(P, "white", "white_dark", axis="y")
PLATE = armour(P, "red", "red_dark", trim="silver", trim_w=0.4)


def build():
    m = Model("harpymon")
    mats = {"skin": WHITE, "chest": PLATE, "foot": metal(P, "grey", dark="silver_dark"), "talon": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.9, talons=True, digitigrade=True, name="harpymon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 53.6, 59.6, skin(P, "face", dark="grey"), cut=1)
    m.round_box(hd, 0, 0.0, 2.6, 3.0, 57.4, 61.0, metal(P, "silver", dark="silver_dark"), cut=1)
    for j in range(4):
        spike(m, hd, (0, 60.6, -1.0 + j * 1.2), (0, 1, 0.6), 1.0, 6.0 - j, solid(P, "red"), tip=0.8)
    for side in (1, -1):                                                              # wing arms
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 50.0, 1.0))
        feather_wing(m, wb, (side * 5.0, 50.0, 1.0), 22.0, 12.0, 3, feathers(P, "white", "white_dark", tip="gold"),
                     side=side, sweep=10, droop=10.0)
    for j in range(3):                                                                # long tail streamers
        pts = [((j - 1) * 2.0, 32.0, 3.0), ((j - 1) * 3.0, 20.0, 6.0), ((j - 1) * 3.6, 6.0, 4.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, WHITE, extend=0.3, t2=2)
    return m
