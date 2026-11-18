"""Fumamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the shadow ninja. A lean black-and-gunmetal cyborg ninja in segmented armour with a horned helm and a
red mask-plate, a long black scarf whipping behind, three katana slung across its back, sickle blades on its forearms
and shins, and long jointed clawed feet. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, riveted, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean black-and-gunmetal cyborg ninja with a horned helm and red mask-plate, a long black scarf, three katana "
        "across its back, sickle blades on its forearms and long clawed feet")
BASE = {"black": (40, 40, 52), "black_dark": (14, 14, 22), "gun": (90, 94, 120), "gun_dark": (40, 42, 60),
        "red": (210, 30, 40), "steel": (220, 224, 234), "steel_dark": (110, 114, 126), "violet": (110, 60, 150),
        "eye": (250, 230, 70)}
SHINY = {"black": (230, 230, 236), "black_dark": (160, 160, 176), "gun": (200, 60, 70), "gun_dark": (120, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "gun", "gun_dark", trim="black", trim_w=0.25)
SUIT = riveted(P, "black", "black_dark")
BLADE = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("fumamon")
    mats = {"skin": SUIT, "chest": ARM, "abs": SUIT, "pelvis": ARM, "neck": SUIT, "deltoid": ARM, "upper_arm": SUIT,
            "forearm": ARM, "hand": SUIT, "finger": SUIT, "claw": BLADE, "thigh": ARM, "knee": ARM, "shin": ARM,
            "calf": ARM, "foot": SUIT, "talon": BLADE}
    a = humanoid(m, mats, bulk=0.82, arm_bulk=0.85, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                 name="fumamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 53.6, 59.8, ARM, cut=1)
    m.round_box(hd, 0, -3.2, 1.6, 0.4, 55.0, 58.6, solid(P, "red"), cut=0)            # red mask-plate
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.4, sx * 1.4), 57.4, -3.7, max(sx * 0.4, sx * 1.4), 57.9, -3.5, solid(P, "eye", glow=True))
    spike(m, hd, (0, 59.4, -2.0), (0, 1, -0.3), 1.4, 4.4, solid(P, "red"), tip=0.25)  # horn
    for sx in (-1, 1):                                                                 # spiky helm crest
        spike(m, hd, (sx * 2.0, 58.6, 1.0), (sx * 0.6, 0.4, 1), 1.0, 4.0, ARM, tip=0.25)
    pts = [(0, 51.0, 3.0), (6.0, 56.0, 8.0), (14.0, 60.0, 10.0), (22.0, 58.0, 12.0), (28.0, 62.0, 14.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                   # long whipping scarf
        rod(m, bd, p0, p1, 1, fabric(P, "black", "black_dark"), extend=0.4, t2=max(1, 3 - j // 2))
    for j, (dx, ang) in enumerate(((-3.0, 30), (0.0, 20), (3.0, -25))):                # three katana on the back
        m.box(bd, dx - 0.4, 30.0, 4.4, dx + 0.4, 48.0, 5.0, BLADE, rotation=(0, 0, ang), pivot=(dx, 42.0, 4.7))
        m.box(bd, dx - 0.5, 48.0, 4.3, dx + 0.5, 54.0, 5.1, solid(P, "violet"), rotation=(0, 0, ang),
              pivot=(dx, 42.0, 4.7))
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                       # sickle blades
        jt = a[nm].get("elbow") or a[nm].get("knee")
        sx = 1 if jt[0] > 0 else -1
        p0 = (jt[0] + sx * 0.6, jt[1] - 1.0, jt[2] + 1.0)
        p1 = (jt[0] + sx * 1.6, jt[1] - 8.0, jt[2] + 3.0)
        rod(m, a[nm]["bone"], p0, p1, 1, BLADE, extend=0.2, t2=2)
        spike(m, a[nm]["bone"], p1, (sx * 0.4, -0.3, -1), 0.8, 3.0, BLADE, tip=0.2)
    return m
