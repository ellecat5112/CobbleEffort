"""Lykamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the only picture on wikimon.net, a rough
manga sketch): the wolf demon king: a hulking grey wolf-man with a shaggy mane of spiky fur, curved horns, a fanged
muzzle, heavy fur-wrapped shoulders and arms, and great clawed hands. Colours chosen from the sketch's mood (grey
fur, dark horns, red eyes). 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fur, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking grey wolf-man with a shaggy spiked mane, curved horns, a fanged muzzle, heavy furred shoulders and great claws"
BASE = {"grey": (150, 150, 160), "grey_dark": (70, 70, 80), "grey_light": (210, 210, 220), "horn": (50, 46, 50),
        "eye": (230, 40, 40), "mouth": (120, 30, 40), "tooth": (250, 248, 236), "claw": (40, 36, 40)}
SHINY = {"grey": (110, 70, 140), "grey_dark": (50, 24, 70), "grey_light": (190, 160, 220)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "grey", "grey_dark", tip="grey_light", length=1.8)


def build():
    m = Model("lykamon")
    mats = {"skin": FUR, "chest": FUR, "abs": FUR, "pelvis": FUR, "neck": FUR, "deltoid": FUR, "upper_arm": FUR,
            "forearm": FUR, "hand": FUR, "finger": FUR, "claw": solid(P, "claw"), "thigh": FUR, "knee": FUR, "shin": FUR,
            "calf": FUR, "foot": FUR, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.3, leg_bulk=1.2, claws=True, talons=True, digitigrade=True, name="lykamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.6, 3.2, 3.6, 53.6, 60.6, FUR, cut=1)
    m.round_box(hd, 0, -6.0, 1.8, 2.4, 53.6, 57.0, FUR, cut=1)
    m.round_box(hd, 0, -7.6, 1.6, 0.8, 53.4, 54.6, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 58.0, -5.3, max(sx * 1.0, sx * 2.4), 58.8, -5.1, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.0, 54.6, -8.0), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
        pts = [(sx * 2.4, 60.0, -1.0), (sx * 5.0, 63.0, 0.0), (sx * 6.0, 61.0, 3.0), (sx * 5.0, 58.0, 4.0)]   # curved horns
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 - j // 2, solid(P, "horn"), extend=0.4)
    for i in range(16):                                                              # shaggy spiked mane
        ang = math.radians(-120 + i * 16)
        spike(m, hd if i % 2 else bd, (4.0 * math.sin(ang), 56.0 + 2.0 * math.cos(ang), 1.6), (math.sin(ang), 0.5, 0.8), 2.4,
              8.0, strands(P, "grey", "grey_dark"), tip=0.8)
    for sx in (-1, 1):                                                               # heavy fur shoulders
        m.round_box(bd, sx * 9.0, 0, 4.0, 4.0, 46.0, 54.0, FUR, cut=2)
    return m
