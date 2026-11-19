"""Sanzomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the travelling priestess: a tall monk in a high gold-and-black embroidered cap, a red veil over the
lower face, long fair hair, a long gold-patterned cream robe with flowing white-and-black sleeves and sashes, prayer
beads, a great prayer-bead rosary arcing over her head and a long unrolled sutra scroll streaming from one hand.
Built covered: a full robe. 25 blocks.

Front is -z, y is up. 70 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a tall travelling priestess in a high gold cap, a red veil, a long gold-patterned robe with flowing sleeves, a great rosary and a sutra scroll"
BASE = {"cream": (236, 220, 170), "cream_dark": (170, 150, 90), "gold": (220, 180, 70), "gold_dark": (140, 100, 20),
        "white": (246, 246, 250), "white_dark": (190, 190, 206), "black": (30, 28, 32), "red": (190, 30, 40),
        "skin": (246, 220, 200), "hair": (240, 220, 160), "hair_dark": (190, 160, 90), "bead": (200, 60, 50),
        "bead_dark": (40, 34, 30), "paper": (240, 230, 200), "ink": (60, 50, 40)}
SHINY = {"cream": (170, 200, 230), "cream_dark": (100, 130, 170), "red": (60, 90, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def robef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and abs((x * 1.2 + y) % 4.0 - 2.0) < 0.3:
        return tone(p["gold"], face), None
    return fabric(P, "cream", "cream_dark", axis="y", period=3.0)(x, y, z, face, variant, box=box, **k)


SLEEVE = fabric(P, "white", "white_dark", axis="y", period=3.0)


def scrollf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and (abs(y % 2.0 - 1.0) < 0.15 and (x * 3) % 2 < 1):
        return tone(p["ink"], face), None
    return tone(p["paper"], face), None


def sashf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["black"] if face == "north" else p["white"], face), None


def build():
    m = Model("sanzomon")
    mats = {"skin": robef, "neck": skin(P, "skin"), "hand": skin(P, "skin"), "finger": skin(P, "skin"),
            "forearm": SLEEVE, "upper_arm": SLEEVE}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.75, leg_bulk=0.8, name="sanzomon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    for i in range(8):                                                                   # long robe
        r = 4.4 + i * 0.8
        m.round_box(bd, 0, 0.4, r, r * 0.85, 32.0 - (i + 1) * 4.0, 32.0 - i * 4.0 + 0.2, robef, cut=max(1, round(r * 0.3)))
    cape(m, bd, 52.0, 12.0, 46.0, sashf, z=3.6, flare=1.2, panels=5, seed=3)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, skin(P, "skin"), cut=1)
    m.round_box(hd, 0, -2.4, 2.4, 0.6, 54.0, 56.6, solid(P, "red"), cut=0)                  # red veil
    m.round_box(hd, 0, 0, 2.6, 2.8, 59.6, 68.0, fabric(P, "gold", "black", axis="y", period=1.6), cut=1)   # tall cap
    m.box(hd, -2.6, 42.0, 0.6, 2.6, 59.0, 3.0, strands(P, "hair", "hair_dark"))
    for j in range(28):                                                                  # great rosary arc
        ang = math.pi * (j / 27)
        c = (16.0 * math.cos(ang), 60.0 + 10.0 * math.sin(ang), 2.0)
        ball(m, hd, c, 0.9, solid(P, "bead" if j % 4 else "bead_dark"), layers=1)
    w = a["arm_left"]["wrist"]                                                           # unrolled sutra scroll
    m.box(a["arm_left"]["bone"], w[0] + 1.0, w[1] - 30.0, w[2] - 2.0, w[0] + 1.6, w[1] + 2.0, w[2] + 6.0, scrollf,
          rotation=(0, 0, 20), pivot=(w[0] + 1.0, w[1], w[2]))
    rod(m, a["arm_left"]["bone"], (w[0] + 1.0, w[1] + 1.0, w[2] - 3.0), (w[0] + 1.0, w[1] + 1.0, w[2] + 7.0), 2,
        solid(P, "red"), extend=0.2)
    return m
