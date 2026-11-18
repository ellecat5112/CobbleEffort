"""Rinkmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): an ice-skating cyborg: a lean figure in a white suit under blue armour, a crested blue helm with
swept-back blue spikes and a yellow visor, a yellow lightning-bolt horn, white gauntlets, long white streamer-wings
behind, and big blue skate boots on curved silver blades. 1 block.

Front is -z, y is up. 60 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(1, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lean ice-skating cyborg in a white suit under blue armour, a spiked blue helm, a yellow bolt horn and skate boots on silver blades"
BASE = {"blue": (60, 130, 220), "blue_dark": (20, 60, 150), "white": (240, 244, 252), "white_dark": (190, 196, 214),
        "yellow": (250, 210, 50), "visor": (250, 230, 80), "steel": (210, 214, 226), "steel_dark": (110, 114, 126)}
SHINY = {"blue": (220, 60, 140), "blue_dark": (140, 20, 80)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", trim="white", trim_w=0.2)
SUIT = fabric(P, "white", "white_dark", axis="y", period=3.0)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("rinkmon")
    mats = {"skin": SUIT, "chest": ARM, "deltoid": ARM, "shin": ARM, "calf": ARM, "foot": ARM, "hand": SUIT,
            "finger": SUIT}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="rinkmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.0, ARM, cut=1)
    m.box(hd, -1.8, 57.0, -3.3, 1.8, 57.8, -3.1, solid(P, "visor", glow=True))
    for j in range(6):                                                                   # swept-back spikes
        spike(m, hd, ((j % 3 - 1) * 1.2, 59.0 - (j // 3) * 1.6, 1.0), ((j % 3 - 1) * 0.3, 0.6, 1), 1.2, 7.0, ARM, tip=0.8)
    m.box(hd, -0.4, 60.0, -2.0, 0.4, 64.0, -1.2, solid(P, "yellow"), rotation=(0, 0, 20), pivot=(0, 60.0, -1.6))
    m.box(hd, -0.4, 63.0, -2.0, 0.4, 67.0, -1.2, solid(P, "yellow"), rotation=(0, 0, -25), pivot=(0, 63.0, -1.6))
    for sx in (-1, 1):                                                                   # streamer-wings
        for j in range(3):
            m.box(bd, min(sx * 3.0, sx * 6.0), 26.0 + j * 4.0, 4.0 + j * 0.3, max(sx * 3.0, sx * 6.0), 50.0, 4.0 + j * 0.3,
                  SUIT, rotation=(16 + j * 4, -sx * 20, sx * (6 + j * 6)), pivot=(sx * 3.0, 50.0, 4.0))
    for side in ("leg_left", "leg_right"):                                               # skate blades
        an = a[side]["ankle"]
        m.box(a[side]["bone"], an[0] - 0.4, 0.0, an[2] - 6.0, an[0] + 0.4, 1.0, an[2] + 4.0, STEEL)
        spike(m, a[side]["bone"], (an[0], 0.6, an[2] - 6.0), (0, 0.6, -1), 0.8, 2.0, STEEL, tip=0.8)
    return m
