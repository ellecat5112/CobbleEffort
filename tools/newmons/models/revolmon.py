"""Revolmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little gunslinger: a shadowy black face with glowing yellow eyes under a huge tan cowboy hat, a red
bandana streaming from its neck, brown gloves and boots with spurs, a blue shirt with a bullet bandolier, a giant
silver revolver in one hand and a smaller one in the other. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, leather, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a little gunslinger with a shadowy face and glowing eyes under a huge tan cowboy hat, a red bandana and a giant silver revolver"
BASE = {"tan": (210, 160, 90), "tan_dark": (150, 100, 40), "black": (24, 22, 28), "eye": (250, 220, 60),
        "red": (210, 40, 40), "red_dark": (130, 14, 14), "brown": (140, 90, 50), "brown_dark": (80, 46, 20),
        "blue": (50, 90, 170), "blue_dark": (20, 44, 110), "steel": (210, 214, 226), "steel_dark": (110, 114, 130),
        "gold": (230, 190, 60)}
SHINY = {"tan": (60, 56, 64), "tan_dark": (24, 22, 28), "red": (60, 140, 220), "red_dark": (20, 70, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.6) < 0.6 and abs(y - 26.0) < 0.8:
                return p["eye"], p["eye"]
    return tone(p["black"], face), None


STEEL = metal(P, "steel", dark="steel_dark")
LEATHER = leather(P, "brown", "brown_dark")


def revolver(m, bone, grip, s):
    gx, gy, gz = grip
    m.box(bone, gx - 0.8 * s, gy - 3.0 * s, gz - 1.0 * s, gx + 0.8 * s, gy, gz + 1.0 * s, solid(P, "brown"))     # grip
    m.box(bone, gx - 1.0 * s, gy, gz - 3.0 * s, gx + 1.0 * s, gy + 2.4 * s, gz + 1.4 * s, STEEL)                  # frame
    rod(m, bone, (gx, gy + 1.6 * s, gz - 3.0 * s), (gx, gy + 1.6 * s, gz - 11.0 * s), max(1, round(1.4 * s)), STEEL,
        extend=0.2)
    m.round_box(bone, gx, gz - 1.2 * s, 1.6 * s, 1.4 * s, gy + 0.2 * s, gy + 2.4 * s, STEEL, cut=0)               # cylinder


def build():
    m = Model("revolmon")
    top = m.bone("revolmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 4.0, 3.4, 10.0, 20.0, fabric(P, "blue", "blue_dark", axis="y"), cut=1)
    m.box(bd, -4.2, 14.0, -3.8, 4.2, 15.2, -3.4, LEATHER, rotation=(0, 0, 30), pivot=(0, 15, -3.6))   # bandolier
    for j in range(5):
        m.box(bd, -2.6 + j * 1.3, 13.0 + j * 0.75, -4.2, -2.0 + j * 1.3, 14.6 + j * 0.75, -3.8, solid(P, "gold"))
    hd = m.bone("head", bd, (0, 20, 0))
    ball(m, hd, (0, 25.0, -0.2), 4.0, facef, layers=3)
    m.round_box(hd, 0, 0, 3.6, 3.0, 20.0, 22.0, fabric(P, "red", "red_dark", axis="x"), cut=1)      # bandana
    for j in range(3):
        rod(m, hd, (2.6, 21.0, 2.0), (7.0 + j, 24.0 + j * 2.0, 6.0), 1, solid(P, "red"), extend=0.2, t2=2)
    m.round_box(hd, 0, 0, 9.0, 9.0, 28.0, 29.4, leather(P, "tan", "tan_dark"), cut=3)          # huge cowboy hat
    m.round_box(hd, 0, 0, 4.4, 4.4, 29.0, 34.0, leather(P, "tan", "tan_dark"), cut=1)
    m.round_box(hd, 0, 0, 4.6, 4.6, 29.2, 30.4, solid(P, "brown_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 7.0, sx * 9.0), 29.0, -3.0, max(sx * 7.0, sx * 9.0), 31.0, 3.0, leather(P, "tan", "tan_dark"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 18.0, 0))
        rod(m, ab, (sx * 4.0, 18.0, 0), (sx * 7.0, 13.0, -2.0), 2, fabric(P, "blue", "blue_dark", axis="x"), extend=0.3)
        ball(m, ab, (sx * 7.4, 12.0, -2.6), 1.8, LEATHER, layers=2)
    revolver(m, "arm_right", (-7.4, 12.0, -3.0), 1.6)                                      # giant revolver
    revolver(m, "arm_left", (7.4, 12.0, -3.0), 0.9)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 9.0, 0))
        m.round_box(lg, sx * 2.0, 0, 1.6, 1.6, 4.0, 10.0, fabric(P, "blue", "blue_dark", axis="y"), cut=0)
        m.round_box(lg, sx * 2.2, -1.0, 2.2, 3.4, 0.0, 6.0, LEATHER, cut=1)
        spike(m, lg, (sx * 2.2, 1.0, 2.4), (0, 0, 1), 0.8, 1.6, solid(P, "gold"), tip=0.8)
    return m
