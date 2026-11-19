"""Sagomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a wandering gunner-monk: a lean demon-man with white hair and a steel mask over his face, a ragged
blue-and-black mantle, baggy navy trousers with a beaded rope belt, steel greaves ending in clawed feet, and a giant
six-barrelled revolver cylinder carried over his shoulder on a long crescent-bladed staff. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean gunner-monk with white hair and a steel mask, a ragged blue mantle, a beaded belt and a giant revolver-cylinder staff"
BASE = {"skin": (150, 110, 80), "skin_dark": (90, 60, 40), "navy": (40, 50, 90), "navy_dark": (14, 18, 40),
        "blue": (90, 120, 190), "blue_dark": (40, 60, 120), "white": (240, 240, 246), "white_dark": (180, 180, 196),
        "steel": (180, 184, 196), "steel_dark": (80, 84, 96), "black": (30, 28, 32), "bead": (190, 150, 90),
        "brass": (210, 170, 70), "claw": (240, 240, 236)}
SHINY = {"navy": (110, 30, 40), "navy_dark": (50, 10, 14), "blue": (200, 70, 80), "blue_dark": (130, 30, 40)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def mantlef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["black"] if face == "north" else p["blue"], face), None


def cylf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south"):
        for j in range(6):
            ang = 2 * math.pi * j / 6
            if math.hypot(x - (-14.0 + 3.6 * math.cos(ang)), y - (62.0 + 3.6 * math.sin(ang))) < 1.2:
                return tone(p["brass"] if math.hypot(x - (-14.0 + 3.6 * math.cos(ang)), y - (62.0 + 3.6 * math.sin(ang))) > 0.6
                            else p["black"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("sagomon")
    mats = {"skin": skin(P, "skin", dark="skin_dark"), "pelvis": fabric(P, "navy", "navy_dark", axis="y"),
            "thigh": fabric(P, "navy", "navy_dark", axis="y"), "shin": STEEL, "calf": STEEL, "talon": solid(P, "claw"),
            "foot": STEEL}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, talons=True, name="sagomon")
    bd = a["body"]
    for j in range(8):                                                                   # beaded rope belt
        ang = 2 * math.pi * j / 8
        m.round_box(bd, 4.4 * math.cos(ang), 3.4 * math.sin(ang), 0.8, 0.8, 31.6, 33.0, solid(P, "bead"), cut=0)
    cape(m, bd, 53.0, 14.0, 30.0, mantlef, z=3.6, flare=2.2, panels=6, seed=12)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, -2.4, 2.4, 0.8, 54.4, 58.6, STEEL, cut=0)                            # steel mask
    for j in range(7):                                                                   # white hair
        spike(m, hd, ((j - 3) * 0.8, 60.0, 0.6), ((j - 3) * 0.3, 0.6, 0.8), 1.2, 4.0, strands(P, "white", "white_dark"),
              tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # staff over the shoulder
    ab = a["arm_right"]["bone"]
    rod(m, ab, (w[0] + 2.0, w[1] - 6.0, w[2] + 4.0), (-14.0, 62.0, 2.0), 1, STEEL, extend=0.2)
    rod(m, ab, (-14.0, 62.0, 4.0), (-14.0, 62.0, -6.0), 9, cylf, extend=0.2)               # giant cylinder
    pts = [(w[0] + 2.0, w[1] - 6.0, w[2] + 4.0), (w[0] + 6.0, w[1] - 14.0, w[2] + 8.0), (w[0] + 2.0, w[1] - 18.0, w[2] + 10.0)]
    for p0, p1 in zip(pts, pts[1:]):                                                      # crescent blade
        rod(m, ab, p0, p1, 1, STEEL, extend=0.2, t2=3)
    return m
