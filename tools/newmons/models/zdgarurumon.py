"""Z'd Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Metal Garurumon's upright cyborg form: a towering wolf mech of dark blue-violet armour with gold
plating on its chest stamped Z'd, a snarling metal wolf head with red eyes, a huge black cannon on its back, gatling
pods on its arms, fists armed with long green crystal claws, and heavy armoured legs with green talons. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a towering blue-violet wolf mech with gold chest plating, a snarling metal wolf head, a huge back cannon and green crystal claws"
BASE = {"blue": (90, 90, 180), "blue_dark": (34, 34, 90), "gold": (240, 200, 60), "gold_dark": (170, 120, 20),
        "black": (40, 40, 46), "black_dark": (14, 14, 18), "green": (60, 200, 120), "green_light": (180, 255, 210),
        "steel": (200, 204, 216), "eye": (255, 50, 50), "mouth": (160, 20, 30), "tooth": (250, 250, 244)}
SHINY = {"blue": (90, 150, 120), "blue_dark": (30, 80, 50)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", panel=(3.0, 3.0))
GOLD = armour(P, "gold", "gold_dark", panel=(2.4, 2.4))
CRYS = gem(P, "green", "green_light", glow=False)


def build():
    m = Model("zdgarurumon")
    mats = {"skin": ARM, "chest": GOLD, "abs": ARM, "pelvis": ARM, "deltoid": ARM, "upper_arm": metal(P, "black"),
            "forearm": ARM, "hand": ARM, "finger": ARM, "claw": CRYS, "thigh": ARM, "knee": GOLD, "shin": ARM,
            "calf": ARM, "foot": ARM, "talon": CRYS, "neck": metal(P, "black")}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.4, leg_bulk=1.45, digitigrade=True, claws=True, talons=True,
                 name="zdgarurumon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -2.0, 3.4, 5.4, 54.0, 60.0, ARM, cut=1)
    m.box(hd, -3.0, 54.4, -9.0, 3.0, 56.0, -5.0, solid(P, "mouth"))
    for j in range(5):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.6, 56.0, -8.6 + j * 0.9), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 3.0), 58.0, -7.0, max(sx * 1.2, sx * 3.0), 58.8, -6.6, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.6, 60.0, 0), (sx * 0.3, 1, 0.4), 1.6, 5.0, ARM, tip=0.8)
    rod(m, bd, (0, 40.0, 6.0), (0, 72.0, 2.0), 3, metal(P, "black", dark="black_dark"), extend=0.0)   # back cannon
    m.round_box(bd, 0, 2.6, 4.2, 4.2, 70.0, 74.0, metal(P, "black", dark="black_dark"), cut=1)
    for nm in ("arm_left", "arm_right"):                                               # gatling pods
        e = a[nm]["elbow"]
        sx = 1 if nm == "arm_left" else -1
        for j in range(3):
            rod(m, a[nm]["bone"], (e[0] + sx * 3.0, e[1] + (j - 1) * 1.4, e[2]), (e[0] + sx * 3.0, e[1] + (j - 1) * 1.4,
                e[2] - 8.0), 1, metal(P, "steel"), extend=0.0)
    return m
