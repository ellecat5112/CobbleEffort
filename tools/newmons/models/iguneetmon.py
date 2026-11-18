"""Iguneetmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the punk lizard: a lean reptile-man with a white face, a red-and-white spiked mohawk, a grey
combat vest over a black shirt with a grenade clip, grey cargo trousers, heavy boots with red soles, a chunky gauntlet
and a huge silver hoop blade (a ring with a spade-shaped blade) carried over his shoulder. Child stage, 1 block tall.

Front is -z, y is up. 64 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, leather, metal, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean punk lizard-man with a red-and-white mohawk, a grey combat vest, cargo trousers, heavy boots and a huge "
        "silver hoop blade over his shoulder")
BASE = {"white": (240, 240, 244), "white_dark": (170, 172, 186), "red": (220, 40, 40), "red_dark": (130, 14, 18),
        "grey": (140, 144, 150), "grey_dark": (70, 72, 80), "black": (36, 36, 40), "black_dark": (12, 12, 14),
        "steel": (220, 224, 232), "steel_dark": (90, 94, 106), "eye": (240, 60, 40), "green": (80, 110, 50),
        "tan": (200, 170, 130)}
SHINY = {"red": (60, 140, 230), "red_dark": (20, 70, 150), "grey": (120, 110, 80), "grey_dark": (60, 50, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SCALE_SKIN = scales(P, "white", "white_dark", size=0.9)
VEST = fabric(P, "grey", "grey_dark", axis="y", seam="black")
PANTS = fabric(P, "grey", "grey_dark", axis="y")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("iguneetmon")
    mats = {"skin": SCALE_SKIN, "chest": VEST, "abs": fabric(P, "black", "black_dark"), "pelvis": PANTS,
            "neck": SCALE_SKIN, "deltoid": VEST, "upper_arm": SCALE_SKIN, "forearm": STEEL, "hand": SCALE_SKIN,
            "finger": SCALE_SKIN, "claw": solid(P, "white"), "thigh": PANTS, "knee": PANTS, "shin": PANTS,
            "calf": PANTS, "foot": leather(P, "black", "black_dark"), "toe": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.85, leg_bulk=0.85, claws=True, name="iguneetmon")
    bd = a["body"]
    m.round_box(bd, 3.0, -3.6, 0.8, 0.8, 44.0, 46.0, solid(P, "green"), cut=0)            # grenade clip
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 3.2, 54.0, 60.0, SCALE_SKIN, cut=1)
    m.round_box(hd, 0, -3.6, 1.6, 1.6, 54.4, 57.0, SCALE_SKIN, cut=1)                      # snout
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.2), 57.6, -3.9, max(sx * 1.0, sx * 2.2), 58.4, -3.6, solid(P, "eye", glow=True))
    for i in range(7):                                                                 # red-and-white mohawk
        spike(m, hd, (0, 59.6, -2.4 + i * 1.0), (0, 1, 0.3 + i * 0.15), 1.4, 7.0 - abs(i - 3) * 0.8,
              strands(P, "red" if i % 2 == 0 else "white", "red_dark"), tip=0.8)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.2, 58.6, 0.4), (sx, 0.6, 0.6), 1.0, 3.0, strands(P, "white", "white_dark"), tip=0.8)
    hnd = a["arm_left"]["hand"]                                                         # huge hoop blade
    hb = a["arm_left"]["bone"]
    m.round_box(hb, hnd[0], hnd[2], 2.0, 2.0, hnd[1] - 1.0, hnd[1] + 2.0, STEEL, cut=1)
    c = (hnd[0] + 8.0, hnd[1] + 12.0, hnd[2] + 3.0)
    n = 18
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        p0 = (c[0] + 13.0 * math.cos(a0), c[1] + 13.0 * math.sin(a0), c[2])
        p1 = (c[0] + 13.0 * math.cos(a1), c[1] + 13.0 * math.sin(a1), c[2])
        rod(m, hb, p0, p1, 1, STEEL, extend=0.3, t2=3)
    spike(m, hb, (c[0] + 9.2, c[1] - 9.2, c[2]), (1, -1, 0), 3.6, 10.0, STEEL, tip=0.8)
    return m
