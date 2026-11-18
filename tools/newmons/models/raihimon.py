"""Raihimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the warrior of the sun spirit: a broad knight in crimson plate patterned with golden suns, a
spiky crowned black helm, gold-and-black banded limbs with golden claws, a great fan of golden blade-wings behind it,
two steel cannons on its shoulders, and a long golden staff topped with a trident claw. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a broad crimson knight patterned with golden suns, a spiky black helm, a fan of golden blade-wings and a trident staff"
BASE = {"red": (170, 30, 30), "red_dark": (90, 10, 10), "gold": (236, 190, 60), "gold_dark": (150, 100, 20),
        "black": (36, 32, 36), "black_dark": (12, 10, 12), "steel": (200, 204, 216), "steel_dark": (100, 104, 120),
        "eye": (250, 200, 40)}
SHINY = {"red": (40, 60, 150), "red_dark": (14, 24, 80)}


def P(v):
    return pal(BASE, SHINY, v)


def sunplate(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south"):
        cx, cy = round(x / 6.0) * 6.0, round(y / 6.0) * 6.0
        d = math.hypot(x - cx, y - cy)
        if d < 1.2 or (d < 2.2 and abs(math.sin(math.atan2(y - cy, x - cx) * 4)) > 0.8):
            return tone(p["gold"], face), None
    return armour(P, "red", "red_dark", trim="gold", trim_w=0.25)(x, y, z, face, variant, box=box, **k)


def bandf(x, y, z, face, variant, box=None, **k):
    if (y % 3.0) < 1.0:
        return metal(P, "gold", dark="gold_dark")(x, y, z, face, variant, box=box, **k)
    return armour(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)


GOLD = metal(P, "gold", dark="gold_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("raihimon")
    mats = {"skin": sunplate, "forearm": bandf, "shin": bandf, "calf": bandf, "hand": bandf, "finger": GOLD,
            "claw": GOLD, "talon": GOLD, "foot": bandf}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.1, claws=True, talons=True, digitigrade=True,
                 name="raihimon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.6, 0, 3.6, 3.8, 46.0, 52.0, sunplate, cut=1)
        rod(m, bd, (sx * 8.0, 52.0, 2.0), (sx * 9.0, 60.0, 0.0), 2, STEEL, extend=0.4)         # shoulder cannons
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.0, 60.0, armour(P, "black", "black_dark"), cut=1)
    m.box(hd, -1.8, 57.0, -3.5, 1.8, 57.8, -3.3, solid(P, "eye", glow=True))
    for j in range(9):                                                                   # spiky crown
        ang = math.radians(-70 + j * 17.5)
        spike(m, hd, (2.6 * math.sin(ang), 60.0, -1.0 + 1.6 * abs(math.sin(ang))), (math.sin(ang) * 0.5, 1, 0.3),
              1.0, 4.0 + (j % 2) * 2.0, GOLD, tip=0.8)
    wb = m.bone("wings", bd, (0, 50, 4))                                                 # golden blade-wings
    for sx in (-1, 1):
        for j in range(6):
            ang = math.radians(10 + j * 14)
            spike(m, wb, (sx * 3.0, 50.0, 4.0), (sx * math.cos(ang), math.sin(ang), 0.5), 1.6, 18.0 + j * 2.0, GOLD,
                  tip=0.8)
    w = a["arm_left"]["wrist"]                                                           # trident staff
    ab = a["arm_left"]["bone"]
    rod(m, ab, (w[0], 4.0, w[2] - 2.0), (w[0], 68.0, w[2] - 2.0), 1, bandf, extend=0.2)
    for f in (-1, 0, 1):
        spike(m, ab, (w[0] + f * 1.6, 68.0, w[2] - 2.0), (f * 0.3, 1, 0), 1.0, 5.0, STEEL, tip=0.8)
    m.box(ab, w[0] - 2.4, 67.0, w[2] - 2.6, w[0] + 2.4, 68.4, w[2] - 1.4, STEEL)
    return m
