"""Black Shoutmon X7 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net, an anime still): the dark fusion of seven Digimon, a towering black armoured dragon-knight. Black and
gunmetal plates with gold V-crest horns on its helm, a dragon's head on one shoulder, great armoured gauntlets, gold
trim, a tall broad sword and swept mechanical wing-fins. 35 blocks tall.

Front is -z, y is up. 74 units tall; no level known (Ultimate used).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a towering black armoured dragon-knight fused from seven Digimon: gold V-crest horns, a dragon head on one "
        "shoulder, armoured gauntlets, gold trim, a tall broad sword and mechanical wing-fins")
BASE = {"black": (40, 40, 48), "black_light": (120, 122, 140), "gun": (90, 92, 104), "gun_dark": (40, 40, 48),
        "gold": (236, 196, 60), "gold_dark": (160, 120, 30), "eye": (90, 240, 120), "steel": (200, 204, 216)}
SHINY = {"black": (230, 226, 236), "black_light": (255, 255, 255), "gun": (190, 190, 206), "gun_dark": (110, 110, 126),
         "eye": (255, 80, 80)}


def P(v):
    return pal(BASE, SHINY, v)


BLACK = armour(P, "black", "black", light="black_light", trim="gold", trim_w=0.35)
GUN = armour(P, "gun", "gun_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("blackshoutmonx7")
    mats = {"skin": GUN, "chest": BLACK, "abs": GUN, "pelvis": BLACK, "deltoid": BLACK, "forearm": BLACK,
            "hand": BLACK, "finger": BLACK, "thigh": BLACK, "knee": GOLD, "shin": BLACK, "foot": BLACK,
            "talon": GOLD}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.4, leg_bulk=1.4, digitigrade=True, talons=True,
                 name="blackshoutmonx7", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.4, 61.0, BLACK, cut=1)
    m.box(hd, -2.0, 57.4, -3.6, 2.0, 58.4, -3.2, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                           # gold V-crest
        rod(m, hd, (0, 59.0, -3.4), (sx * 8.0, 68.0, -2.0), 2, GOLD, extend=0.3, t2=1)
    shell(m, bd, (0, 0, 0.6), 6.4, 42.0, 51.0, -85, 85, 9, 1.4, BLACK)
    sh = a["arm_left"]["shoulder"]                               # dragon head on its left shoulder
    db = m.bone("dragon", a["arm_left"]["bone"], sh)
    m.round_box(db, sh[0] + 4.0, -2.0, 3.0, 4.0, 48.0, 54.0, BLACK, cut=1)
    m.box(db, sh[0] + 2.0, 48.0, -10.0, sh[0] + 6.0, 51.0, -5.0, GUN)
    m.box(db, sh[0] + 2.8, 52.0, -6.4, sh[0] + 5.2, 52.8, -6.0, solid(P, "eye", glow=True))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        h = a[nm]["hand"]
        m.round_box(a[nm]["bone"], h[0], h[2], 3.6, 3.6, h[1] - 4.0, h[1] + 3.0, BLACK, cut=1)
    sw = m.bone("sword", a["arm_right"]["bone"], a["arm_right"]["hand"])
    h = a["arm_right"]["hand"]
    m.box(sw, h[0] - 3.0, h[1] - 44.0, h[2] - 0.6, h[0] + 3.0, h[1] - 2.0, h[2] + 0.6, metal(P, "steel", dark="gun"))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # mechanical wing-fins
        wb = m.bone(nm, bd, (sx * 4.0, 50.0, 4.0))
        for j in range(4):
            rod(m, wb, (sx * 4.0, 50.0, 4.0), (sx * (14.0 + j * 3), 64.0 - j * 6, 8.0 + j), 2, BLACK, extend=0.3,
                t2=1)
    return m
