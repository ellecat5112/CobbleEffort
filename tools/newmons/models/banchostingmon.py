"""Bancho Stingmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the delinquent boss insect. A lean crimson-armoured insect-man with a spiky violet
crest and red antennae, a long dark violet coat with a high collar and gold buttons, baggy black trousers tied at the
knee, a segmented gold stinger lance on its left arm, a thin sword in its right hand, red clawed feet and four
translucent wings. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("the delinquent boss insect: crimson armour, a spiky violet crest, a long dark violet coat, baggy black "
        "trousers, a gold stinger lance, a thin sword and four translucent wings")
BASE = {"red": (180, 30, 40), "red_dark": (100, 10, 20), "red_light": (240, 110, 110), "violet": (70, 50, 110),
        "violet_dark": (30, 20, 60), "crest": (170, 110, 200), "crest_dark": (100, 60, 140), "black": (34, 32, 40),
        "black_light": (90, 88, 100), "gold": (230, 186, 60), "gold_dark": (150, 110, 30), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 128), "wing": (200, 230, 250, 120), "wing_vein": (120, 160, 200, 200),
        "eye": (255, 220, 60)}
SHINY = {"red": (40, 120, 70), "red_dark": (16, 70, 30), "red_light": (120, 210, 150), "violet": (160, 120, 40),
         "violet_dark": (100, 70, 16)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light")
COAT = fabric(P, "violet", "violet_dark", axis="y", period=3.0)
TROUSER = fabric(P, "black", "black_light", axis="y", period=2.0)
GOLD = metal(P, "gold", dark="gold_dark")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u * 0.8 + v * 0.2) % 2.6 < 0.2:
        return p["wing_vein"], None
    return p["wing"], None


def build():
    m = Model("banchostingmon")
    mats = {"skin": RED, "chest": RED, "abs": RED, "pelvis": TROUSER, "neck": RED, "deltoid": COAT,
            "upper_arm": COAT, "forearm": RED, "hand": RED, "finger": RED, "claw": RED, "thigh": TROUSER,
            "knee": TROUSER, "shin": RED, "calf": RED, "foot": RED, "talon": RED}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.95, leg_bulk=0.95, digitigrade=True, talons=True, claws=True,
                 name="banchostingmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.3, 2.6, 54.6, 60.4, RED, cut=1)
    m.box(hd, -1.8, 57.4, -3.0, 1.8, 58.4, -2.7, solid(P, "eye", glow=True))
    for i in range(9):                                           # spiky violet crest
        ang = math.radians(-60 + i * 15)
        rod(m, hd, (1.6 * math.sin(ang), 60.0, 0.4), (5.0 * math.sin(ang), 64.0 + 2.0 * math.cos(ang), 3.0), 1,
            strands(P, "crest", "crest_dark"), extend=0.2, t2=2)
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.0, 60.0, -2.0), (sx * 4.0, 66.0, -4.0), 1, solid(P, "red"), extend=0.2)   # antennae
    cb = m.bone("cap", bd, (0, 52, 3))                           # long coat
    cape(m, cb, 53.0, 18.0, 46.0, COAT, z=4.6, flare=0.9, panels=8, sweep=(0, 6))
    m.box(bd, -4.0, 50.0, -1.0, 4.0, 56.0, 3.6, COAT)                                   # high collar
    for j in range(4):
        m.box(bd, 2.6, 36.0 + j * 3.0, -4.6, 3.6, 37.0 + j * 3.0, -4.0, solid(P, "gold"))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 4.0))
        for j, ang in enumerate((25, -15)):
            x0, x1 = sorted((sx * 3.0, sx * 22.0))
            m.box(wb, x0, 46.0, 5.0 + j, x1, 52.0, 5.0 + j, wingf, rotation=(0, sx * 10, sx * ang),
                  pivot=(sx * 3.0, 49.0, 5.0 + j))
    al = a["arm_left"]                                           # segmented gold stinger lance
    el, wr = al["elbow"], al["wrist"]
    for j in range(5):
        c = tuple(e + (w - e) * (j / 4) for e, w in zip(el, wr))
        rod(m, al["bone"], c, (c[0], c[1] - 1.4, c[2]), 5 - j * 0.6, GOLD, extend=0)
    rod(m, al["bone"], wr, (wr[0] + 1.0, wr[1] - 24.0, wr[2] - 3.0), 1, metal(P, "steel", dark="steel_dark"),
        extend=0)
    ar = a["arm_right"]                                          # thin sword
    h = ar["hand"]
    rod(m, ar["bone"], h, (h[0] - 10.0, h[1] + 16.0, h[2] - 4.0), 1, metal(P, "steel", dark="steel_dark"), extend=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        kn = a[nm]["knee"]
        m.round_box(a[nm]["bone"], kn[0], kn[2], 2.4, 2.4, 14.0, 22.0, TROUSER, cut=1)   # baggy at the knee
    return m
