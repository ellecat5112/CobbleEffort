"""Zeke Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a great machine dragon of gold and silver: a tyrannosaur of interlocking golden armour plates
over silver joints, a horned golden helm with a toothy jaw, swept golden blade-wings, spiked silver gauntlet claws, a
cannon slung beneath one arm, heavy golden legs with silver talons and a long armoured tail. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a great machine tyrannosaur of interlocking golden armour over silver joints with swept golden blade-wings and silver claws"
BASE = {"gold": (236, 200, 90), "gold_dark": (160, 120, 30), "silver": (210, 214, 226), "silver_dark": (110, 114, 130),
        "black": (40, 40, 46), "eye": (255, 60, 60), "mouth": (130, 20, 30), "tooth": (250, 250, 244)}
SHINY = {"gold": (210, 210, 220), "gold_dark": (120, 120, 140), "silver": (230, 190, 90), "silver_dark": (160, 120, 30)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", trim="silver", panel=(3.0, 3.0))
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("zekegreymon")
    mats = {"skin": GOLD, "belly": SILVER, "head": GOLD, "neck": SILVER, "thigh": GOLD, "shin": GOLD, "foot": GOLD,
            "talon": SILVER, "claw": SILVER, "arm": GOLD, "tail": GOLD, "mouth": solid(P, "mouth"),
            "teeth": solid(P, "tooth")}
    a = theropod(m, mats, "zekegreymon", hip_y=18.0, chest=(0, 30.0, -4.0), body_r=7.0, chest_r=6.6)
    bd, hd = a["body"], a["head"]
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 4.0, 34.0, 2.0))
        for j in range(4):                                                             # swept golden blade-wings
            x0, x1 = sorted((sx * 4.0, sx * (26.0 - j * 4.0)))
            m.box(wb, x0, 34.0 - j * 2.4, 2.0 + j, x1, 36.0 - j * 2.4, 3.0 + j, GOLD,
                  rotation=(0, sx * -10, sx * (25 - j * 8)), pivot=(sx * 4.0, 35.0, 2.5 + j))
        spike(m, hd, (sx * 2.6, a["skull_top"], a["skull_z"][1] - 2.0), (sx * 0.3, 1, 0.6), 1.4, 6.0, GOLD, tip=0.8)
    spike(m, hd, (0, a["skull_top"], a["skull_z"][0] + 2.0), (0, 1, -0.4), 1.2, 4.0, SILVER, tip=0.8)
    arm = a["arm_right"]
    h = arm["hand"]
    rod(m, arm["bone"], (h[0], h[1] - 1.0, h[2] + 4.0), (h[0], h[1] - 1.0, h[2] - 8.0), 2, metal(P, "black"), extend=0.0)
    for j in range(5):
        spike(m, bd, (0, 36.0 - j * 3.0, 4.0 + j * 2.0), (0, 1, 0.6), 1.6, 4.0, SILVER, tip=0.8)
    return m
