"""Queen Chessmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the black queen of the chessboard: a tall knight-queen in gunmetal-black plate trimmed
gold, a crowned helm with a pink visor and a long silver plume, flared pauldrons, a skirt of long steel blade-tassets,
a great magenta cape, and a tall staff with a black hammer head, a golden heart-knot and a dangling red heart. 35
blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, gem, metal, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall knight-queen in gunmetal plate trimmed gold with a crowned helm, a steel blade skirt, a magenta cape and a hammer staff"
BASE = {"black": (60, 62, 72), "black_dark": (20, 20, 26), "gold": (230, 190, 70), "gold_dark": (150, 100, 20),
        "pink": (220, 60, 140), "pink_dark": (130, 20, 80), "steel": (210, 214, 226), "steel_dark": (110, 114, 126),
        "visor": (240, 120, 200), "red": (210, 30, 40), "silver": (220, 220, 230), "silver_dark": (150, 150, 166)}
SHINY = {"black": (230, 230, 240), "black_dark": (150, 150, 166), "pink": (60, 120, 220), "pink_dark": (20, 60, 150)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "black", "black_dark", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["pink_dark"] if face == "north" else p["pink"], face), None


def build():
    m = Model("queenchessmon")
    mats = {"skin": PLATE, "neck": metal(P, "black", dark="black_dark"), "knee": GOLD, "foot": GOLD}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, name="queenchessmon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # flared pauldrons
        m.round_box(bd, sx * 7.6, 0, 3.2, 3.4, 47.0, 52.0, PLATE, cut=1)
        spike(m, bd, (sx * 9.6, 51.0, 0), (sx * 0.8, 1, 0), 1.6, 4.0, GOLD, tip=0.8)
    for i in range(10):                                                                  # steel blade tassets
        ang = math.radians(-110 + i * 24)
        if -0.3 < math.sin(ang) < 0.3 and math.cos(ang) > 0:
            continue
        cx, cz = 4.8 * math.cos(ang), 3.6 * math.sin(ang)
        m.box(bd, cx - 0.8, 14.0, cz - 0.3, cx + 0.8, 32.0, cz + 0.3, STEEL,
              rotation=(math.sin(ang) * 10, 0, -math.cos(ang) * 10), pivot=(cx, 32.0, cz))
    cape(m, bd, 52.0, 16.0, 44.0, capef, z=4.0, flare=1.8, panels=7, seed=4)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.0, PLATE, cut=1)
    m.box(hd, -1.8, 57.0, -3.3, 1.8, 57.8, -3.1, solid(P, "visor", glow=True))
    for j in range(5):                                                                   # crown
        spike(m, hd, (-2.0 + j, 60.0, -1.6), (0, 1, 0), 0.9, 2.0 + (j == 2) * 1.6, GOLD, tip=0.8)
    for j in range(4):                                                                   # silver plume
        rod(m, hd, (0, 60.0, 1.0), (j - 1.5, 54.0 - j * 4.0, 6.0 + j), 1, strands(P, "silver", "silver_dark"),
            extend=0.2, t2=2)
    w = a["arm_right"]["wrist"]                                                          # hammer staff
    rod(m, a["arm_right"]["bone"], (w[0], 2.0, w[2] - 2.0), (w[0], 70.0, w[2] - 2.0), 1, STEEL, extend=0.2)
    m.box(a["arm_right"]["bone"], w[0] - 4.0, 68.0, w[2] - 3.4, w[0] + 4.0, 71.0, w[2] - 0.6, metal(P, "black"))
    m.round_box(a["arm_right"]["bone"], w[0], w[2] - 2.0, 1.6, 1.6, 58.0, 61.0, GOLD, cut=0)     # heart knot
    m.box(a["arm_right"]["bone"], w[0] - 1.0, 52.0, w[2] - 2.6, w[0] + 1.0, 54.0, w[2] - 1.4, gem(P, "red", "pink"))
    return m
