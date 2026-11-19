"""Thetismon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a jellyfish sea-goddess: a navy armoured helm crowned with crackling golden lightning, a puffed
violet jelly dress of round lobes, a sun brooch, purple armoured legs and boots, a heavy navy gauntlet that fires
bolts, and long trailing white-and-pink ribbon tentacles with green stinger tips. 25 blocks.

Front is -z, y is up. 70 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, skin, solid
from _jellyhat import ribbon, spark
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a jellyfish sea-goddess with a lightning-crowned navy helm, a puffed violet jelly dress, a heavy gauntlet and long white-and-pink ribbon tentacles"
BASE = {"navy": (40, 40, 90), "navy_dark": (14, 14, 40), "violet": (180, 140, 240), "violet_dark": (110, 70, 180),
        "white": (240, 240, 250), "pink": (240, 150, 200), "green": (120, 230, 90), "gold": (250, 210, 60),
        "spark": (255, 240, 80), "skin": (250, 222, 216), "skin_dark": (210, 170, 166), "purple": (110, 70, 160),
        "purple_dark": (60, 30, 100), "eye": (255, 230, 100)}
SHINY = {"violet": (120, 210, 240), "violet_dark": (60, 140, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def ribbonf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 10.0:
        return tone(p["green"], face), p["green"]
    return tone(p["pink"] if int(y / 6) % 2 else p["white"], face), None


NAVY = armour(P, "navy", "navy_dark", trim="gold", panel=(3.0, 3.0))
PURP = armour(P, "purple", "purple_dark", trim="pink", panel=(3.0, 3.0))
JELLY = fabric(P, "violet", "violet_dark")


def build():
    m = Model("thetismon")
    mats = {"skin": skin(P, "skin", dark="skin_dark"), "chest": JELLY, "abs": JELLY, "pelvis": JELLY,
            "deltoid": NAVY, "upper_arm": JELLY, "forearm": NAVY, "hand": NAVY, "thigh": PURP, "knee": PURP,
            "shin": PURP, "calf": PURP, "foot": PURP, "neck": JELLY}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.95, name="thetismon")
    bd = a["body"]
    for i, (x, y, z, r) in enumerate(((0, 28, -2, 6.0), (-5, 30, 0, 5.0), (5, 30, 0, 5.0), (0, 32, 4, 5.4),
                                      (-4, 36, -3, 4.4), (4, 36, -3, 4.4), (0, 44, -3, 4.6))):
        ball(m, bd, (x, y, z), r, JELLY, layers=3)                                     # puffed jelly dress
    ball(m, bd, (0, 49.0, -4.6), 1.6, solid(P, "gold", glow=True), layers=1)           # sun brooch
    for j in range(8):
        ang = j * math.pi / 4
        spike(m, bd, (2.2 * math.cos(ang), 49.0 + 2.2 * math.sin(ang), -4.8), (math.cos(ang), math.sin(ang), 0), 0.8,
              1.4, solid(P, "gold"), tip=0.8)
    h = a["arm_left"]["hand"]                                                           # heavy gauntlet
    m.round_box(a["arm_left"]["bone"], h[0], h[2], 3.2, 3.4, h[1] - 3.0, h[1] + 7.0, NAVY, cut=1)
    spark(m, a["arm_left"]["bone"], (h[0] + 2.0, h[1] - 3.0, h[2] - 3.0), 2.4, solid(P, "spark", glow=True), seed=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 53.0, 60.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, 0.6, 4.0, 4.2, 56.0, 63.0, NAVY, cut=2)                            # navy helm
    m.box(hd, -3.0, 56.6, -4.0, 3.0, 57.4, -3.6, solid(P, "eye", glow=True))
    for j in range(7):                                                                  # lightning crown
        ang = (j - 3) * 0.4
        spike(m, hd, (math.sin(ang) * 3.0, 62.6, math.cos(ang) * 0.5), (math.sin(ang), 1, 0.2), 1.4,
              5.0 + (j % 2) * 3.0, solid(P, "spark", glow=True), tip=0.8)
    rb = m.bone("ribbons", bd, (0, 52, 2))                                              # ribbon tentacles
    for i, sx in enumerate((-1, 1, -1, 1)):
        pts = [(sx * 3.0, 54.0 - i * 2.0, 3.0), (sx * (10.0 + i * 2.0), 62.0 - i * 6.0, 5.0),
               (sx * (16.0 + i), 46.0 - i * 6.0, 7.0), (sx * (14.0 + i), 26.0 - i * 4.0, 6.0),
               (sx * (10.0 + i * 2.0), 6.0 + i * 2.0, 3.0)]
        ribbon(m, rb, pts, 2.0, ribbonf)
    return m
