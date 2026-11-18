"""Regalecusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the oarfish warrior-king: a serpentine body of deep crimson banded with dark stripes and
edged by a long crackling fin of blue lightning, a silver-armoured humanoid torso with a ragged red sash, a golden
oarfish-skull helm trailing long red streamer-fins, a coiled whip in one hand and a long lightning-blade spear in the
other. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "an oarfish warrior-king: a crimson banded serpent body with a lightning fin, a silver-armoured torso, a golden skull helm and a lightning spear"
BASE = {"crimson": (130, 40, 60), "crimson_dark": (60, 14, 24), "stripe": (40, 20, 30), "silver": (210, 214, 226),
        "silver_dark": (110, 114, 130), "gold": (236, 196, 70), "gold_dark": (150, 110, 20), "red": (210, 40, 40),
        "red_dark": (120, 14, 14), "bolt": (160, 220, 255), "eye": (250, 220, 60), "black": (30, 28, 32)}
SHINY = {"crimson": (40, 100, 140), "crimson_dark": (14, 44, 70), "red": (60, 160, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def serpf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (z * 0.5 + y * 0.3) % 4.0 < 0.9:
        return tone(p["stripe"], face), None
    return armour(P, "crimson", "crimson_dark")(x, y, z, face, variant, box=box, **k)


ARM = armour(P, "silver", "silver_dark", trim="gold", trim_w=0.2)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("regalecusmon")
    mats = {"skin": ARM, "pelvis": serpf, "neck": metal(P, "black")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=0.8, name="regalecusmon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    tb = m.bone("tail", bd, (0, 30, 0))                                                  # serpentine body
    pts = [(0, 32.0, 0), (0, 22.0, 4.0), (4.0, 12.0, 10.0), (0, 6.0, 18.0), (-6.0, 6.0, 24.0), (-8.0, 12.0, 30.0),
           (-4.0, 22.0, 34.0), (2.0, 30.0, 32.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, max(3, 9 - i), serpf, extend=0.8)
        for j in range(2):                                                               # lightning fin
            q = (p0[0] + (p1[0] - p0[0]) * j / 2, p0[1] + (p1[1] - p0[1]) * j / 2 + 4.0, p0[2] + (p1[2] - p0[2]) * j / 2)
            spike(m, tb, q, (0, 1, 0.3), 1.2, 4.0, solid(P, "bolt", glow=True), tip=0.8)
    m.round_box(bd, 0, 0, 5.2, 4.0, 30.0, 34.0, fabric(P, "red", "red_dark", axis="y"), cut=1)   # ragged sash
    rod(m, bd, (3.0, 32.0, -3.0), (6.0, 22.0, -5.0), 2, fabric(P, "red", "red_dark", axis="y"), extend=0.2, t2=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.8, 4.0, 54.0, 60.0, GOLD, cut=1)                             # golden skull helm
    m.round_box(hd, 0, -5.4, 1.6, 1.4, 54.0, 57.0, GOLD, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.7, sx * 2.9), 57.0, -4.0, max(sx * 2.7, sx * 2.9), 58.0, -2.6, solid(P, "eye", glow=True))
    for j in range(4):                                                                   # red streamer-fins
        pts2 = [(0, 60.0, -2.0 + j), ((j - 1.5) * 2.0, 66.0, 4.0 + j * 2.0), ((j - 1.5) * 4.0, 62.0, 12.0 + j * 2.0)]
        for p0, p1 in zip(pts2, pts2[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.2, t2=2)
    w = a["arm_right"]["wrist"]                                                          # lightning-blade spear
    ab = a["arm_right"]["bone"]
    rod(m, ab, (w[0], w[1] + 10.0, w[2] - 1.0), (w[0], w[1] - 6.0, w[2] - 1.0), 1, metal(P, "black"), extend=0.2)
    m.box(ab, w[0] - 0.4, w[1] - 28.0, w[2] - 2.6, w[0] + 0.4, w[1] - 6.0, w[2] + 0.6, solid(P, "bolt", glow=True))
    w = a["arm_left"]["wrist"]                                                           # coiled whip
    for i in range(10):
        ang = i * 0.9
        p0 = (w[0] + 1.6 * math.cos(ang), w[1] - 2.0 - i * 0.6, w[2] + 1.6 * math.sin(ang))
        p1 = (w[0] + 1.6 * math.cos(ang + 0.9), w[1] - 2.6 - i * 0.6, w[2] + 1.6 * math.sin(ang + 0.9))
        rod(m, a["arm_left"]["bone"], p0, p1, 1, solid(P, "black"), extend=0.2)
    return m
