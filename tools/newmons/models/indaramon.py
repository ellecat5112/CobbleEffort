"""Indaramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the warrior deity Indara: a tall lean purple warrior with a long white mane and pointed ears, red
ribbons knotted at the throat, golden shoulder plates, a golden belt, enormous flared trousers banded red and crimson
ending in gold-studded cuffs, and a giant golden spiked conch shell slung across its back on green cords. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a lean purple warrior with a white mane, red ribbons, golden shoulder plates, huge flared red-banded trousers "
        "and a giant golden spiked conch shell on its back")
BASE = {"purple": (90, 60, 140), "purple_dark": (40, 24, 80), "purple_light": (160, 130, 210), "white": (240, 240, 246),
        "white_dark": (170, 170, 190), "red": (220, 40, 50), "red_dark": (130, 14, 30), "crimson": (160, 20, 40),
        "gold": (240, 200, 80), "gold_dark": (160, 120, 30), "gold_light": (255, 240, 170), "green": (60, 160, 70),
        "eye": (240, 60, 40)}
SHINY = {"purple": (40, 110, 120), "purple_dark": (14, 50, 60), "purple_light": (110, 190, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "purple", dark="purple_dark", light="purple_light")
GOLD = armour(P, "gold", "gold_dark", light="gold_light")


def pantsf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y % 2.0) < 1.2 else p["crimson"], face), None


def build():
    m = Model("indaramon")
    mats = {"skin": SKIN, "chest": SKIN, "abs": SKIN, "pelvis": GOLD, "neck": SKIN, "deltoid": GOLD,
            "upper_arm": SKIN, "forearm": SKIN, "hand": SKIN, "finger": SKIN, "thigh": SKIN, "knee": SKIN,
            "shin": SKIN, "calf": SKIN, "foot": SKIN, "toe": SKIN}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.8, name="indaramon")
    bd = a["body"]
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                               # enormous flared trousers
        lg = a[nm]["bone"]
        for j in range(6):
            r = 3.0 + j * 0.9
            m.round_box(lg, sx * (3.0 + j * 0.6), 0.0, r, r, 28.0 - (j + 1) * 4.6, 28.0 - j * 4.6 + 0.4, pantsf,
                        cut=max(1, int(r * 0.3)))
        m.round_box(lg, sx * 6.6, 0.0, 8.2, 8.2, 0.0, 2.0, GOLD, cut=3)
        for j in range(5):
            ang = math.radians(-60 + j * 30)
            m.box(lg, sx * 6.6 + 8.0 * math.sin(ang) - 0.6, 0.6, -8.3 * math.cos(ang) - 0.6,
                  sx * 6.6 + 8.0 * math.sin(ang) + 0.6, 1.4, -8.3 * math.cos(ang), solid(P, "white"))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.4, SKIN, cut=1)
    m.round_box(hd, 0, -3.0, 1.4, 1.2, 55.0, 57.6, SKIN, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.0), 57.8, -3.3, max(sx * 0.8, sx * 2.0), 58.6, -3.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.8, 60.0, 0.6), (sx * 0.3, 1, 0.3), 1.2, 4.0, SKIN, tip=0.8)   # pointed ears
    for i in range(9):                                                              # long white mane
        ang = math.radians(-90 + i * 22)
        rod(m, hd, (2.2 * math.sin(ang), 60.4, 0.6 + math.cos(ang)), (3.6 * math.sin(ang), 40.0, 4.0), 2,
            strands(P, "white", "white_dark"), extend=0.3, t2=1)
    for sx in (-1, 1):                                                              # red ribbons at the throat
        rod(m, bd, (0, 52.0, -3.0), (sx * 3.0, 48.0, -4.0), 1, fabric(P, "red", "red_dark"), extend=0.3, t2=2)
    sh = m.bone("shell", bd, (0, 48, 6))                                            # giant golden spiked conch
    c = (6.0, 50.0, 10.0)
    for j in range(5):
        r = 9.0 - j * 1.6
        m.round_box(sh, c[0] - j * 2.6, c[2], r, r * 0.8, c[1] - r * 0.8, c[1] + r * 0.8, GOLD, cut=max(1, int(r * 0.35)))
        for t in range(6):
            ang = 2 * math.pi * t / 6
            spike(m, sh, (c[0] - j * 2.6, c[1] + r * 0.8 * math.sin(ang), c[2] + r * 0.8 * math.cos(ang)),
                  (0, math.sin(ang), math.cos(ang)), 1.4, 3.0, metal(P, "gold_light", dark="gold"), tip=0.8)
    spike(m, sh, (c[0] - 12.0, c[1], c[2]), (-1, 0, 0), 2.0, 6.0, GOLD, tip=0.8)
    rod(m, sh, (-4.0, 52.0, -3.6), (8.0, 40.0, 5.0), 1, solid(P, "green"), extend=0, t2=1)     # green cords
    return m
