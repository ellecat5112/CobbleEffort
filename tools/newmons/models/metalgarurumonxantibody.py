"""Metal Garurumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): Metal Garurumon changed by the X-Antibody into an upright war machine: a
towering armoured warrior of blue steel plates trimmed gold, a wolf's head helm with a gold crest, a great gatling
cannon for its right arm, a missile pod and a long rail cannon over its shoulders, blade fins at its back and legs
ending in pink-red claws. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("an upright war machine of blue steel plates trimmed gold, a wolf's head helm, a gatling cannon right arm, a "
        "missile pod and rail cannon over its shoulders and pink-red claws")
BASE = {"blue": (60, 80, 170), "blue_dark": (24, 30, 90), "blue_light": (130, 150, 230), "gold": (240, 190, 70),
        "gold_dark": (160, 110, 20), "steel": (90, 96, 116), "steel_dark": (40, 42, 54), "claw": (230, 60, 110),
        "eye": (250, 60, 60), "hatch": (30, 30, 40)}
SHINY = {"blue": (220, 224, 236), "blue_dark": (140, 144, 160), "blue_light": (250, 250, 255), "gold": (90, 200, 250)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", light="blue_light", trim="gold", trim_w=0.25, rivets=True)
GOLD = armour(P, "gold", "gold_dark", trim="blue_dark", trim_w=0.2)
GUN = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("metalgarurumonxantibody")
    mats = {"skin": ARM, "neck": GUN, "upper_arm": GUN, "thigh": GUN, "knee": GOLD, "hand": ARM, "finger": ARM,
            "claw": solid(P, "claw"), "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.2, leg_bulk=1.2, claws=True, talons=True, digitigrade=True,
                 name="metalgarurumonxantibody")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # big shoulder armour
        m.round_box(bd, sx * 9.0, 0.0, 3.6, 4.0, 47.0, 54.0, ARM, cut=1)
        for j in range(3):
            spike(m, bd, (sx * 11.0, 52.0 - j * 2.0, 1.0 + j), (sx * 0.7, 0.7, 0.4), 1.6, 5.0, GOLD, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.0, 3.4, 54.0, 60.0, ARM, cut=1)                           # wolf-head helm
    m.round_box(hd, 0, -6.0, 2.0, 3.0, 54.4, 57.6, ARM, cut=1)
    m.box(hd, -1.6, 54.0, -8.6, 1.6, 54.6, -4.0, solid(P, "hatch"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 2.6), 58.0, -4.5, max(sx * 1.2, sx * 2.6), 58.8, -4.3, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 60.0, -0.6), (sx * 0.4, 1, 0.5), 1.6, 5.0, ARM, tip=0.8)        # ears
    spike(m, hd, (0, 60.0, -2.0), (0, 0.8, 1), 1.6, 6.0, GOLD, tip=0.8)                         # gold crest
    ar = a["arm_right"]                                                                  # gatling cannon arm
    el, wr = ar["elbow"], ar["wrist"]
    rod(m, ar["bone"], el, (wr[0], wr[1] + 2.0, wr[2] - 2.0), 7, ARM, extend=0.8)
    cx, cy, cz = wr[0], wr[1] - 1.0, wr[2] - 4.0
    for i in range(6):
        ang = 2 * math.pi * i / 6
        bx, by = cx + 1.8 * math.cos(ang), cy + 1.8 * math.sin(ang)
        rod(m, ar["bone"], (bx, by, cz), (bx, by - 12.0, cz - 6.0), 1, GUN, extend=0.2)
    m.round_box(ar["bone"], cx, cz - 0.4, 3.0, 3.0, cy - 2.0, cy + 2.0, GOLD, cut=1)
    ox, oy, oz = 10.0, 58.0, 2.0                                                         # shoulder missile pod
    m.round_box(bd, ox, oz, 3.4, 3.4, oy - 3.0, oy + 4.0, ARM, cut=1)
    for i in range(3):
        for j in range(2):
            m.box(bd, ox - 2.6 + i * 1.8, oy - 1.8 + j * 2.4, oz - 3.5, ox - 1.4 + i * 1.8, oy - 0.6 + j * 2.4,
                  oz - 3.3, solid(P, "gold", glow=True))
    rod(m, bd, (-6.0, 56.0, 4.0), (-14.0, 68.0, -8.0), 2, GUN, extend=0.4, t2=3)          # long rail cannon
    for sx in (-1, 1):                                                                   # back blade fins
        for j in range(3):
            spike(m, bd, (sx * 3.0, 50.0 - j * 4.0, 4.0), (sx * 0.6, 0.4, 1), 1.6, 9.0 - j * 2.0, GOLD, tip=0.8)
    return m
