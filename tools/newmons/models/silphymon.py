"""Silphymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fusion of Aquilamon and Tailmon: a lean beast-warrior in a silver-white chest plate with a red
helm-mask and a brown mane, big white-furred paws and gloves with lilac stripes, baggy red trousers, yellow taloned
bird feet with lilac claws, and white feathered wings tipped with red. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, fur, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean beast-warrior in a silver chest plate with a red helm-mask, white-furred gloves, baggy red trousers, yellow talons and red-tipped white wings"
BASE = {"silver": (220, 224, 236), "silver_dark": (130, 134, 150), "red": (210, 50, 40), "red_dark": (120, 20, 14),
        "white": (248, 248, 252), "white_dark": (190, 196, 214), "brown": (120, 80, 50), "lilac": (170, 140, 220),
        "yellow": (250, 200, 60), "eye": (60, 140, 220)}
SHINY = {"red": (60, 100, 210), "red_dark": (20, 40, 130), "yellow": (240, 160, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def glovef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 3.0) < 0.6:
        return tone(p["lilac"], face), None
    return fur(P, "white", "white_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("silphymon")
    mats = {"skin": fur(P, "white", "white_dark", length=1.0), "chest": armour(P, "silver", "silver_dark"),
            "abs": armour(P, "silver", "silver_dark"), "forearm": glovef, "hand": glovef, "finger": glovef,
            "pelvis": fabric(P, "red", "red_dark", axis="y"), "thigh": fabric(P, "red", "red_dark", axis="y"),
            "knee": fabric(P, "red", "red_dark"), "shin": solid(P, "yellow"), "foot": solid(P, "yellow"),
            "talon": solid(P, "lilac")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=1.0, talons=True, digitigrade=True, name="silphymon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 2.8, 54.0, 60.0, fur(P, "white", "white_dark"), cut=1)
    m.round_box(hd, 0, -1.0, 2.8, 3.0, 57.0, 61.0, armour(P, "red", "red_dark"), cut=1)      # red helm-mask
    m.box(hd, -1.8, 57.4, -4.1, 1.8, 58.4, -3.9, solid(P, "eye"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.4, 0), (sx * 0.6, 1, 0.3), 1.2, 4.0, solid(P, "lilac"), tip=0.8)
    for j in range(5):                                                                   # brown mane
        spike(m, hd, ((j - 2) * 1.0, 60.6, 1.6), ((j - 2) * 0.2, 0.4, 1), 1.2, 4.0, strands(P, "brown", "brown"), tip=0.8)
    for sx in (-1, 1):                                                                   # red-tipped white wings
        feather_wing(m, bd, (sx * 3.0, 50.0, 3.0), 22.0, 14.0, 6, feathers(P, "white", "white_dark", tip="red"), side=sx,
                     sweep=25, droop=-10.0)
    return m
