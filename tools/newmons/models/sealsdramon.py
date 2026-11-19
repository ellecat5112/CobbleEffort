"""Sealsdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a special-forces dragon soldier: a lean dragon in dark gunmetal combat armour with ribbed plates,
a blank goggled helm with a red eye-lens and a single horn, a red blade-fin down its back, a combat knife reversed in
one hand, and a heavy armoured tail. 15 blocks.

Front is -z, y is up. 58 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 58
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean dragon soldier in dark gunmetal combat armour, a goggled helm with a red lens and horn, a red back fin and a combat knife"
BASE = {"gun": (60, 66, 74), "gun_dark": (20, 24, 28), "steel": (180, 184, 196), "steel_dark": (90, 94, 108),
        "red": (210, 30, 40), "lens": (250, 60, 60)}
SHINY = {"gun": (80, 110, 70), "gun_dark": (30, 50, 24)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "gun", "gun_dark", trim="steel_dark", trim_w=0.2)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("sealsdramon")
    mats = {"skin": ARM, "talon": STEEL, "claw": STEEL}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, talons=True, digitigrade=True, name="sealsdramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.4, 3.6, 54.0, 60.0, ARM, cut=1)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.2, -4.8, 0.9, 0.6, 57.0, 58.6, STEEL, cut=0)
    m.box(hd, -2.0, 57.4, -5.2, -0.4, 58.2, -5.0, solid(P, "lens", glow=True))
    spike(m, hd, (0, 60.0, -2.0), (0, 1, -0.2), 1.4, 6.0, STEEL, tip=0.8)
    for j in range(6):                                                                   # red blade-fin
        spike(m, bd, (0, 52.0 - j * 4.0, 4.0), (0, 0.6, 1), 1.0, 4.0 - j * 0.3, solid(P, "red"), tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # reversed combat knife
    m.box(a["arm_right"]["bone"], w[0] - 0.4, w[1] - 2.0, w[2] - 1.0, w[0] + 0.4, w[1] + 8.0, w[2] + 1.0, STEEL)
    tl = m.bone("tail", bd, (0, 32, 4))
    pts = [(0, 32.0, 4.0), (0, 22.0, 10.0), (0, 12.0, 16.0), (0, 6.0, 22.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 4 - i, ARM, extend=0.6)
    return m
