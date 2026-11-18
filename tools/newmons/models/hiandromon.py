"""Hi Andromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the high android: a tall gunmetal-black cyborg with red cables at every joint, a sleek helmeted
head, two spiked heads mounted on its shoulders (one blue, one red), a huge clawed right arm, long legs on clawed
steel feet. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall gunmetal-black cyborg with red cables at its joints, a helmeted head, a blue and a red spiked head on "
        "its shoulders and a huge clawed right arm")
BASE = {"black": (60, 60, 68), "black_dark": (20, 20, 26), "black_light": (130, 130, 144), "red": (200, 30, 40),
        "blue": (50, 70, 170), "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "eye": (250, 200, 40)}
SHINY = {"black": (200, 200, 210), "black_dark": (120, 120, 134), "black_light": (250, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light", trim="red", trim_w=0.25)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("hiandromon")
    mats = {"skin": riveted(P, "red", "black_dark"), "chest": ARM, "abs": ARM, "pelvis": ARM, "deltoid": ARM,
            "forearm": ARM, "thigh": ARM, "shin": ARM, "calf": ARM, "foot": STEEL, "talon": STEEL, "claw": STEEL,
            "hand": ARM, "finger": ARM}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                 name="hiandromon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 3.0, 53.6, 60.0, ARM, cut=1)
    m.box(hd, -1.6, 57.2, -3.5, 1.6, 58.0, -3.3, solid(P, "eye", glow=True))
    for sx, col in ((1, "red"), (-1, "blue")):                                            # shoulder heads
        m.round_box(bd, sx * 8.0, 0.4, 2.6, 2.6, 51.0, 56.0, armour(P, col, "black_dark", trim="steel"), cut=1)
        spike(m, bd, (sx * 9.6, 55.0, 0.4), (sx, 0.6, 0), 1.2, 3.0, STEEL, tip=0.8)
        m.box(bd, sx * 8.0 - 1.0, 53.6, -2.4, sx * 8.0 + 1.0, 54.2, -2.2, solid(P, "eye", glow=True))
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                  # huge claw arm
    m.round_box(ar, h[0], h[2] - 1.0, 3.6, 3.6, h[1] - 1.0, h[1] + 6.0, ARM, cut=1)
    for j in range(3):
        ang = math.radians(-60 + j * 60)
        pts = [(h[0], h[1] - 1.0, h[2] - 1.0), (h[0] + 4.0 * math.sin(ang), h[1] - 6.0, h[2] - 4.0),
               (h[0] + 3.0 * math.sin(ang), h[1] - 10.0, h[2] - 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ar, p0, p1, 1, STEEL, extend=0.3, t2=2)
    return m
