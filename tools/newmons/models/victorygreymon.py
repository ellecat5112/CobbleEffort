"""Victory Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the dragon warrior of the Xros Wars: an orange-hided dragon-man in heavy gold armour
with silver joints, a gold horned dragon helm, red-and-gold back fins, a long tail, huge clawed talons, and the giant
Dramon Breaker sword of silver and gold held over its shoulder. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 63
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an orange dragon-man in heavy gold armour with a horned gold helm, red-and-gold back fins and the giant Dramon Breaker sword"
BASE = {"orange": (240, 140, 50), "orange_dark": (170, 80, 20), "gold": (240, 196, 60), "gold_dark": (170, 120, 20),
        "silver": (210, 214, 226), "silver_dark": (110, 114, 130), "red": (200, 40, 40), "eye": (90, 220, 120),
        "claw": (240, 240, 244), "blue": (70, 120, 210)}
SHINY = {"orange": (100, 160, 220), "orange_dark": (40, 90, 160), "gold": (200, 210, 230), "gold_dark": (120, 130, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "orange", "orange_dark", size=1.2)
GOLD = armour(P, "gold", "gold_dark", trim="silver", panel=(3.0, 3.0))
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("victorygreymon")
    mats = {"skin": HIDE, "chest": GOLD, "abs": HIDE, "pelvis": GOLD, "deltoid": GOLD, "upper_arm": HIDE,
            "forearm": GOLD, "hand": GOLD, "thigh": HIDE, "knee": SILVER, "shin": GOLD, "calf": GOLD, "foot": HIDE,
            "talon": solid(P, "claw"), "neck": HIDE}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.25, leg_bulk=1.2, digitigrade=True, talons=True, name="victorygreymon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.0, 0, 3.8, 4.0, 47.0, 54.0, GOLD, cut=1)
        spike(m, bd, (sx * 9.0, 53.0, 0), (sx * 0.4, 1, 0.2), 1.6, 6.0, SILVER, tip=0.8)
        for j in range(3):                                                             # back fins
            spike(m, bd, (sx * 3.0, 50.0 - j * 4.0, 4.0), (sx * 0.8, 0.6, 1), 1.6, 9.0 - j * 2.0,
                  solid(P, "red" if j % 2 else "gold"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.2, 4.4, 54.0, 61.0, GOLD, cut=1)
    m.round_box(hd, 0, -5.4, 2.0, 1.6, 55.0, 58.0, HIDE, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.6), 58.4, -4.8, max(sx * 0.8, sx * 2.6), 59.2, -4.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.6, 60.0, 0.6), (sx * 0.4, 1, 0.6), 1.4, 6.0, GOLD, tip=0.8)
    spike(m, hd, (0, 59.0, -5.6), (0, 0.6, -1), 1.4, 4.0, SILVER, tip=0.8)
    tl = m.bone("tail", bd, (0, 30, 4))
    pts = [(0, 30.0, 4.0), (0, 22.0, 12.0), (0, 16.0, 20.0), (0, 14.0, 26.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - i, HIDE, extend=0.6)
    h = a["arm_right"]["hand"]                                                          # Dramon Breaker
    rb = a["arm_right"]["bone"]
    rod(m, rb, (h[0], h[1] - 6.0, h[2]), (h[0], h[1] + 4.0, h[2]), 1, SILVER, extend=0.0)
    m.box(rb, h[0] - 3.4, h[1] + 4.0, h[2] - 1.4, h[0] + 3.4, h[1] + 6.0, h[2] + 1.4, GOLD)
    m.box(rb, h[0] - 2.4, h[1] + 6.0, h[2] - 0.8, h[0] + 2.4, h[1] + 36.0, h[2] + 0.8, SILVER,
          rotation=(0, 0, 25), pivot=(h[0], h[1] + 6.0, h[2]))
    m.box(rb, h[0] - 0.6, h[1] + 8.0, h[2] - 1.0, h[0] + 0.6, h[1] + 30.0, h[2] + 1.0, solid(P, "blue"),
          rotation=(0, 0, 25), pivot=(h[0], h[1] + 6.0, h[2]))
    return m
