"""Vritramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the beast spirit of flame: a towering crimson armoured dragon-man with gold-edged plates, a horned
silver dragon helm, great blade-wings sheathed in fire, a ribbed golden belly, silver-taloned feet, and a long whip
of a crimson tail. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a towering crimson armoured dragon-man with a horned silver helm, flame-sheathed blade-wings and a long crimson tail"
BASE = {"red": (200, 30, 40), "red_dark": (110, 10, 16), "gold": (240, 196, 60), "gold_dark": (170, 120, 20),
        "silver": (210, 214, 226), "silver_dark": (110, 114, 130), "flame": (255, 150, 40, 210), "eye": (255, 230, 80)}
SHINY = {"red": (50, 60, 150), "red_dark": (16, 20, 80), "flame": (120, 200, 255, 210)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", trim="gold", panel=(3.0, 3.0))
SILVER = metal(P, "silver", dark="silver_dark")


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 3.0:
        return tone(p["gold"] if (y % 2.4) > 0.5 else p["gold_dark"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vritramon")
    mats = {"skin": RED, "chest": RED, "abs": bellyf, "pelvis": RED, "deltoid": RED, "upper_arm": RED, "forearm": RED,
            "hand": SILVER, "finger": SILVER, "claw": SILVER, "thigh": RED, "knee": SILVER, "shin": RED, "calf": RED,
            "foot": SILVER, "talon": SILVER, "neck": RED}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.25, leg_bulk=1.2, digitigrade=True, claws=True, talons=True,
                 name="vritramon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.0, 0, 3.8, 4.0, 47.0, 54.0, RED, cut=1)
        spike(m, bd, (sx * 9.0, 53.0, 0), (sx * 0.3, 1, 0), 1.6, 6.0, SILVER, tip=0.8)
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 50.0, 4.0))
        for j in range(3):                                                             # flame-sheathed blade wings
            d = (sx * (0.9 - j * 0.2), 0.6 + j * 0.3, 0.4)
            spike(m, wb, (sx * 3.0, 50.0 - j * 3.0, 4.0), d, 2.6, 20.0 - j * 4.0, metal(P, "gold", dark="gold_dark"),
                  tip=0.8)
            spike(m, wb, (sx * 3.4, 49.0 - j * 3.0, 5.0), d, 4.0, 16.0 - j * 3.0, solid(P, "flame", glow=True), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.0, 4.4, 54.0, 61.0, SILVER, cut=1)
    m.round_box(hd, 0, -5.6, 1.8, 1.6, 55.0, 58.0, RED, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.4), 58.6, -4.8, max(sx * 0.8, sx * 2.4), 59.4, -4.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.2, 60.4, 0), (sx * 0.4, 1, 0.5), 1.4, 7.0, SILVER, tip=0.8)
    spike(m, hd, (0, 60.6, -3.0), (0, 1, -0.2), 1.2, 5.0, metal(P, "gold"), tip=0.8)
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (2.0, 20.0, 12.0), (6.0, 10.0, 18.0), (10.0, 4.0, 22.0), (14.0, 4.0, 26.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 3 - i), RED, extend=0.5)
    return m
