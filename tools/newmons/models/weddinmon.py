"""Weddinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the wedding fairy: a lady whose gown is a towering tiered wedding cake frilled with white lace,
strawberries and pink icing, a pink dress bodice and long white gloves, a tall pink beehive hairdo crowned with a
golden trophy cup, blonde ringlets, a lace fan in one hand, and a fluffy white tail. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a lady in a towering tiered wedding-cake gown with lace and strawberries, a pink beehive hairdo with a golden cup and a lace fan"
BASE = {"cream": (252, 248, 240), "cream_dark": (210, 200, 190), "pink": (240, 150, 180), "pink_dark": (190, 90, 130),
        "red": (220, 40, 50), "gold": (240, 200, 70), "gold_dark": (170, 130, 30), "skin": (250, 226, 214),
        "skin_dark": (210, 176, 164), "hair": (240, 220, 140), "hair_dark": (190, 160, 70), "lace": (255, 255, 255)}
SHINY = {"pink": (160, 200, 240), "pink_dark": (90, 130, 190), "red": (90, 60, 200)}


def P(v):
    return pal(BASE, SHINY, v)


CAKE = fabric(P, "cream", "cream_dark", axis="x", period=1.6)
PINK = fabric(P, "pink", "pink_dark")


def tierf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and face != "up" and (y - box.lo[1]) < 0.8:
        return tone(p["lace"] if int((x + z) * 1.5) % 2 else p["pink"], face), None
    if face in ("north", "south", "east", "west") and (int(x * 1.3 + 40) + int(z * 1.3 + 40)) % 5 == 0 and \
            abs(y - (box.lo[1] + box.size[1] * 0.6 if box else 0)) < 0.5:
        return tone(p["red"], face), None
    return CAKE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("weddinmon")
    mats = {"skin": skin(P, "skin", dark="skin_dark"), "chest": PINK, "abs": PINK, "pelvis": CAKE, "deltoid": PINK,
            "upper_arm": fabric(P, "lace", "cream_dark"), "forearm": fabric(P, "lace", "cream_dark"),
            "hand": fabric(P, "lace", "cream_dark"), "thigh": CAKE, "knee": CAKE, "shin": CAKE, "calf": CAKE,
            "foot": solid(P, "pink_dark"), "neck": skin(P, "skin", dark="skin_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.85, name="weddinmon")
    bd = a["body"]
    for j, (r, y0, y1) in enumerate(((12.0, 0.0, 10.0), (10.0, 10.0, 19.0), (8.0, 19.0, 27.0), (6.2, 27.0, 33.0))):
        m.round_box(bd, 0, 0.6, r, r * 0.9, y0, y1, tierf, cut=3 if r > 7 else 2)          # cake tiers
        for i in range(8):
            ang = i * 2 * math.pi / 8
            ball(m, bd, (r * 0.9 * math.cos(ang), y1 + 0.2, 0.6 + r * 0.8 * math.sin(ang)), 0.8, solid(P, "red"),
                 layers=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, skin(P, "skin", dark="skin_dark"), cut=1)
    for j in range(5):                                                                    # pink beehive
        r = 3.8 - abs(j - 1.5) * 0.4
        m.round_box(hd, 0, 0.6, r, r, 60.0 + j * 2.0, 62.0 + j * 2.0, PINK, cut=1)
    m.round_box(hd, 0, 0.6, 1.4, 1.4, 70.0, 72.0, metal(P, "gold", dark="gold_dark"), cut=0)   # golden cup
    m.round_box(hd, 0, 0.6, 2.0, 2.0, 72.0, 74.0, metal(P, "gold", dark="gold_dark"), cut=1)
    for sx in (-1, 1):                                                                    # ringlets
        for j in range(3):
            ball(m, hd, (sx * 3.4, 58.0 - j * 2.4, 0.6), 1.0, strands(P, "hair", "hair_dark"), layers=1)
    h = a["arm_left"]["hand"]                                                             # lace fan
    for j in range(6):
        ang = (j - 2.5) * 0.3
        m.box(a["arm_left"]["bone"], h[0] - 0.4, h[1], h[2] - 0.2, h[0] + 0.4, h[1] + 7.0, h[2] + 0.2,
              solid(P, "lace" if j % 2 else "pink"), rotation=(0, 0, math.degrees(ang)), pivot=(h[0], h[1], h[2]))
    tl = m.bone("tail", bd, (0, 20, 10))
    for j in range(4):
        ball(m, tl, (2.0 + j * 2.0, 14.0 + j * 1.0, 12.0 + j * 1.2), 2.4 - j * 0.3, fur(P, "lace", "cream_dark"), layers=2)
    return m
