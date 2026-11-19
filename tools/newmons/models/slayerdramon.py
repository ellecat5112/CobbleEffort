"""Slayerdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the dragon-slaying dragon-man: a lean warrior in white-silver dragon-scale armour with a
horned dragon helm and violet trim, a long flowing green cloth trailing from its shoulders, wings of golden-orange
flame feathers, and the flexible blade Fragarach coiled round it. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, feathers, metal, scales, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean dragon-man in white-silver scale armour with a horned helm, a flowing green cloth, wings of golden flame feathers and a coiling flexible blade"
BASE = {"silver": (226, 228, 236), "silver_dark": (130, 134, 150), "violet": (120, 90, 180), "green": (40, 100, 90),
        "green_dark": (14, 50, 44), "gold": (250, 190, 60), "orange": (250, 120, 40), "eye": (250, 60, 60),
        "blade": (210, 214, 226)}
SHINY = {"silver": (60, 60, 70), "silver_dark": (24, 24, 30), "green": (120, 40, 60), "green_dark": (60, 14, 26)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", trim="violet", trim_w=0.2)


def clothf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green_dark"] if face == "north" else p["green"], face), None


def build():
    m = Model("slayerdramon")
    mats = {"skin": ARM, "neck": scales(P, "silver", "silver_dark"), "talon": metal(P, "silver"), "claw": metal(P, "silver")}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.9, talons=True, claws=True, digitigrade=True,
                 name="slayerdramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.6, 3.6, 54.0, 60.0, ARM, cut=1)
    m.round_box(hd, 0, -5.0, 1.6, 1.4, 54.4, 57.0, ARM, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.5, sx * 2.7), 57.4, -3.8, max(sx * 2.5, sx * 2.7), 58.2, -2.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 60.0, 0), (sx * 0.4, 1, 0.7), 1.4, 8.0, ARM, tip=0.8)
    cape(m, bd, 52.0, 14.0, 50.0, clothf, z=4.0, flare=2.0, panels=6, seed=10, sweep=(20.0, 15.0))
    wb = m.bone("wings", bd, (0, 50, 5))                                                 # golden flame feather wings
    for sx in (-1, 1):
        for j in range(6):
            ang = math.radians(-30 + j * 18)
            spike(m, wb, (sx * 3.0, 50.0, 5.0 + j * 0.3), (sx * math.cos(ang), math.sin(ang), 0.5), 2.4, 20.0 - j,
                  feathers(P, "gold", "orange"), tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # coiling flexible blade
    ab = a["arm_right"]["bone"]
    prev = w
    for i in range(1, 14):
        ang = i * 0.7
        p_ = (w[0] - 4.0 * math.cos(ang) - 2.0, w[1] + 3.0 * i - 2.0, w[2] - 4.0 * math.sin(ang))
        rod(m, ab, prev, p_, 1, metal(P, "blade"), extend=0.1, t2=2)
        prev = p_
    return m
