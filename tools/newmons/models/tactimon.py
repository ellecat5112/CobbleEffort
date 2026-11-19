"""Tactimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the demon general: black and blood-red armour edged in gold, a horned black helm with a gold crest
and a red face-plate, spiked pauldrons, a ragged black-and-crimson cape, and the sealed blade Jagamaru, a huge curved
black katana bound in a red cord, held upright. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a demon general in black and blood-red armour edged in gold, a horned helm, a ragged cape and a huge sealed black katana"
BASE = {"black": (40, 38, 44), "black_dark": (14, 12, 16), "red": (170, 30, 34), "red_dark": (90, 10, 14),
        "gold": (226, 180, 70), "gold_dark": (140, 96, 30), "steel": (180, 184, 196), "eye": (90, 255, 140),
        "cord": (200, 40, 40), "blade": (60, 58, 66), "edge": (230, 230, 240)}
SHINY = {"red": (40, 110, 190), "red_dark": (14, 50, 110), "cord": (40, 110, 190)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", trim="gold", panel=(3.0, 3.0))
RED = armour(P, "red", "red_dark", trim="gold", panel=(2.6, 2.6))
GOLD = metal(P, "gold", dark="gold_dark")


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["red"] if face == "north" else p["black"]
    return tone(c, face), None


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and x < box.lo[0] + 0.5:
        return tone(p["edge"], face), None
    return tone(p["blade"], face), None


def build():
    m = Model("tactimon")
    mats = {"skin": ARM, "chest": RED, "abs": ARM, "pelvis": ARM, "deltoid": RED, "upper_arm": ARM,
            "forearm": RED, "hand": ARM, "thigh": ARM, "knee": GOLD, "shin": RED, "foot": ARM, "talon": GOLD,
            "neck": ARM}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.2, leg_bulk=1.15, talons=True, name="tactimon")
    bd = a["body"]
    m.round_box(bd, 0, -0.2, 6.2, 4.6, 30.0, 32.6, GOLD, cut=1)                         # belt
    ball(m, bd, (0, 31.2, -4.8), 1.2, solid(P, "eye", glow=True), layers=1)
    for sx in (-1, 1):                                                                 # tassets
        m.box(bd, min(sx * 1.0, sx * 6.0), 20.0, -4.6, max(sx * 1.0, sx * 6.0), 30.0, -3.6, RED)
        m.round_box(bd, sx * 7.4, 0, 3.6, 3.6, 49.0, 54.0, RED, cut=1)                   # pauldrons
        for j in range(3):
            spike(m, bd, (sx * (6.0 + j * 1.6), 53.6, 0), (sx * 0.5, 1, 0), 1.0, 4.0 + j, GOLD, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.4, 3.6, 54.0, 62.0, ARM, cut=1)
    m.box(hd, -2.4, 55.0, -4.2, 2.4, 59.0, -3.4, RED)                                    # face plate
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 58.0, -4.5, max(sx * 0.6, sx * 2.0), 58.8, -4.1, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 3.0, 60.0, -0.5), (sx * 0.8, 1, 0.2), 1.4, 6.0, GOLD, tip=0.8)
    spike(m, hd, (0, 61.6, -2.6), (0, 1, -0.3), 1.6, 6.0, GOLD, tip=0.8)                 # crest
    cb = m.bone("cape", bd, (0, 53, 4))
    cape(m, cb, 53.0, 15.0, 44.0, capef, z=4.6, flare=0.7, panels=7, seed=3)
    h = a["arm_right"]["hand"]                                                          # Jagamaru, upright
    sb = a["arm_right"]["bone"]
    m.box(sb, h[0] - 0.6, h[1] - 6.0, h[2] - 0.6, h[0] + 0.6, h[1] + 3.0, h[2] + 0.6, fabric(P, "cord", "red_dark"))
    m.box(sb, h[0] - 2.0, h[1] + 3.0, h[2] - 1.2, h[0] + 2.0, h[1] + 4.0, h[2] + 1.2, GOLD)
    for j in range(7):                                                                 # curved blade
        y0 = h[1] + 4.0 + j * 4.0
        dx = -0.06 * (j * 4.0) ** 1.3 / 4.0
        m.box(sb, h[0] + dx - 1.4, y0, h[2] - 0.5, h[0] + dx + 1.0, y0 + 4.2, h[2] + 0.5, bladef)
    for j in range(3):
        m.box(sb, h[0] - 1.6, h[1] + 8.0 + j * 7.0, h[2] - 0.7, h[0] + 1.2, h[1] + 8.8 + j * 7.0, h[2] + 0.7,
              solid(P, "cord"))
    return m
