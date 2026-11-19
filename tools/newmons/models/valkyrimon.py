"""Valkyrimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the winged warrior of the north: a knight in white-and-silver armour with a gold-trimmed winged
helm and a visor, white feathered wings with red tips, a long blue sash and belted scabbard, a quiver of arrows on
its back, a long sword in hand, and the little golden bird Freyjamon perched on its shoulder. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, leather, metal, solid
from _route import pal, tone

HEIGHT = 63
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a knight in white-and-silver armour with a winged helm, red-tipped white wings, a blue sash, a quiver, a long sword and a little golden bird"
BASE = {"white": (240, 242, 248), "white_dark": (170, 176, 196), "silver": (200, 206, 220), "silver_dark": (110, 116, 134),
        "gold": (236, 196, 70), "gold_dark": (170, 120, 30), "blue": (50, 110, 200), "blue_dark": (20, 50, 120),
        "red": (210, 40, 40), "brown": (130, 90, 50), "brown_dark": (70, 44, 20), "eye": (90, 200, 255),
        "steel": (226, 230, 240)}
SHINY = {"white": (60, 60, 76), "white_dark": (20, 20, 30), "blue": (190, 50, 70), "blue_dark": (110, 16, 30)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "white", "white_dark", trim="gold", panel=(3.0, 3.0))
SILVER = armour(P, "silver", "silver_dark", trim="gold", panel=(2.4, 2.4))


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 20.0:
        return tone(p["red"], face), None
    return feathers(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("valkyrimon")
    mats = {"skin": SILVER, "chest": ARM, "abs": SILVER, "pelvis": ARM, "deltoid": ARM, "upper_arm": SILVER,
            "forearm": ARM, "hand": SILVER, "thigh": SILVER, "knee": ARM, "shin": ARM, "calf": ARM, "foot": ARM,
            "talon": metal(P, "gold"), "neck": SILVER}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.05, name="valkyrimon")
    bd = a["body"]
    m.box(bd, -1.6, 14.0, -4.4, 1.6, 34.0, -3.6, fabric(P, "blue", "blue_dark"))           # blue sash
    m.round_box(bd, 0, 0, 5.4, 4.0, 30.0, 32.0, leather(P, "brown", "brown_dark"), cut=1)
    rod(m, bd, (-5.0, 30.0, -1.0), (-6.0, 12.0, 2.0), 1, leather(P, "brown", "brown_dark"), extend=0.0)  # scabbard
    m.round_box(bd, 2.0, 5.0, 1.4, 1.4, 38.0, 54.0, leather(P, "brown", "brown_dark"), cut=0)  # quiver
    for j in range(3):
        spike(m, bd, (1.4 + j * 0.6, 54.0, 5.0), (0, 1, 0), 0.8, 3.0, solid(P, "red"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.2, 3.4, 54.0, 61.6, ARM, cut=1)
    m.box(hd, -2.6, 57.0, -3.9, 2.6, 58.4, -3.4, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                                  # winged helm
        for j in range(4):
            spike(m, hd, (sx * 3.0, 59.0 + j * 0.8, 0.6), (sx * 0.8, 0.9, 0.4), 1.2, 6.0 - j, feathers(P, "white",
                  "white_dark"), tip=0.8)
    spike(m, hd, (0, 61.4, -1.0), (0, 1, -0.4), 1.2, 4.0, metal(P, "gold"), tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 48.0, 4.0))
        feather_wing(m, wb, (sx * 3.0, 48.0, 4.0), 24.0, 14.0, 3, wingf, side=sx, sweep=25, droop=-6.0)
    h = a["arm_right"]["hand"]                                                          # long sword
    rb = a["arm_right"]["bone"]
    m.box(rb, h[0] - 2.0, h[1] - 0.4, h[2] - 0.8, h[0] + 2.0, h[1] + 0.8, h[2] + 0.8, metal(P, "gold"))
    m.box(rb, h[0] - 0.9, max(0.4, h[1] - 24.0), h[2] - 0.4, h[0] + 0.9, h[1] - 0.4, h[2] + 0.4, metal(P, "steel"))
    bb = m.bone("bird", bd, (7.0, 53.0, 0))                                             # Freyjamon
    ball(m, bb, (7.6, 55.0, 0), 1.6, feathers(P, "gold", "gold_dark"), layers=2)
    spike(m, bb, (7.6, 55.0, -1.4), (0, 0, -1), 0.8, 1.2, solid(P, "red"), tip=0.8)
    for sx in (-1, 1):
        spike(m, bb, (7.6 + sx * 1.2, 55.4, 0), (sx, 0.6, 0.4), 0.9, 2.6, feathers(P, "gold", "gold_dark"), tip=0.8)
    return m
