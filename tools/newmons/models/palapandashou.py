"""PalaPandashou (a Digimon of the CobbleEffort: Digital crossover; after the manga panel on wikimon.net): a giant
panda warrior-sage: a towering panda with a roaring face, a shaggy white mane, a heavy padded grey jacket with a
ribbed collar and black bands, and great black-furred arms. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage (no level on wikimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a towering panda warrior-sage with a roaring face, a shaggy white mane, a padded grey jacket and great black-furred arms"
BASE = {"white": (240, 240, 236), "white_dark": (180, 180, 176), "black": (36, 34, 36), "black_dark": (12, 12, 14),
        "grey": (150, 150, 156), "grey_dark": (90, 90, 96), "mouth": (180, 40, 50), "tooth": (250, 250, 240)}
SHINY = {"black": (130, 80, 50), "black_dark": (70, 40, 20)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fur(P, "white", "white_dark", length=1.4)
BLACK = fur(P, "black", "black_dark", length=1.4)
JACKET = fabric(P, "grey", "grey_dark", axis="x", period=2.0)


def build():
    m = Model("palapandashou")
    mats = {"skin": BLACK, "chest": JACKET, "abs": JACKET, "pelvis": JACKET, "neck": WHITE, "deltoid": JACKET,
            "thigh": BLACK, "knee": BLACK, "hand": BLACK, "finger": BLACK}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.4, leg_bulk=1.3, hand_pose="fist", name="palapandashou")
    bd = a["body"]
    m.round_box(bd, 0, 0.4, 3.6, 3.6, 50.0, 54.0, fabric(P, "grey", "grey_dark", axis="y", period=1.0), cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    ball(m, hd, (0, 58.6, -0.4), 4.0, WHITE, layers=5, ry=3.6)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.6, -3.6, 1.2, 0.4, 58.0, 60.2, solid(P, "black"), cut=0)
        ball(m, hd, (sx * 3.4, 62.0, 0), 1.4, BLACK, layers=2)
    m.box(hd, -1.6, 55.6, -4.25, 1.6, 57.4, -4.05, solid(P, "mouth"))
    for i in range(10):                                                                  # shaggy white mane
        ang = math.radians(-90 + i * 20)
        spike(m, hd, (3.6 * math.sin(ang), 60.0, 1.0 + math.cos(ang)), (math.sin(ang), 0.5, 0.5), 1.8, 5.0, WHITE,
              tip=0.8)
    return m
