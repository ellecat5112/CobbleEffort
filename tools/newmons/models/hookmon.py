"""Hookmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
pirate captain: a stout pirate in a navy coat with gold buttons and red cuffs, a big tricorne hat with a skull and
crossbones, a dark face with one glowing eye, a golden hook on one arm, a silver bell-mouthed gauntlet on the other,
striped red-and-white trousers and black boots. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a stout pirate captain in a navy coat with gold buttons, a big tricorne hat with a skull, a golden hook, a "
        "silver bell-mouthed gauntlet and striped trousers")
BASE = {"navy": (40, 36, 80), "navy_dark": (14, 12, 40), "gold": (240, 200, 60), "gold_dark": (160, 120, 20),
        "red": (200, 40, 40), "white": (246, 246, 246), "black": (30, 28, 32), "black_dark": (12, 12, 14),
        "face": (40, 36, 46), "eye": (250, 220, 60), "steel": (210, 214, 224), "steel_dark": (110, 114, 126)}
SHINY = {"navy": (130, 30, 40), "navy_dark": (70, 10, 14)}


def P(v):
    return pal(BASE, SHINY, v)


COAT0 = fabric(P, "navy", "navy_dark", axis="y")


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and any(abs(x - sx * 2.0) < 0.5 and (y % 3.0) < 1.0 for sx in (-1, 1)):
        return tone(p["gold"], face), None
    return COAT0(x, y, z, face, variant, box=box, **k)


def pantsf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y % 2.0) < 1.0 else p["white"], face), None


def hatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, y - 41.0) < 1.6:
        return tone(p["white"], face), None
    return COAT0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hookmon")
    top = m.bone("hookmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 18.0, 34.0, coatf, cut=2)
    m.round_box(bd, 0, 0, 5.4, 4.4, 12.0, 19.0, pantsf, cut=1)
    m.round_box(bd, 0, 0, 6.2, 5.2, 19.0, 21.0, leather(P, "black", "black_dark", stitch="gold"), cut=2)
    hd = m.bone("head", bd, (0, 34, 0))
    m.round_box(hd, 0, 0, 3.6, 3.6, 33.6, 40.0, skin(P, "face", dark="black"), cut=1)
    m.box(hd, 0.6, 36.4, -3.8, 2.2, 37.6, -3.6, solid(P, "eye", glow=True))
    m.round_box(hd, 0, 0, 8.0, 6.0, 39.4, 41.0, hatf, cut=3)                              # tricorne brim
    m.round_box(hd, 0, 0, 5.0, 4.4, 40.6, 46.0, hatf, cut=2)
    m.round_box(hd, 0, 0, 5.2, 4.6, 41.0, 42.0, metal(P, "gold", dark="gold_dark"), cut=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 31.0, 0))
        rod(m, ab, (sx * 6.0, 31.0, 0), (sx * 9.0, 24.0, -2.0), 3, COAT0, extend=0.6)
        m.round_box(ab, sx * 9.4, -2.4, 2.0, 2.0, 21.0, 24.0, solid(P, "red"), cut=1)
    al = "arm_left"                                                                         # silver bell gauntlet
    m.round_box(al, 10.0, -5.0, 2.6, 2.6, 18.0, 22.0, metal(P, "steel", dark="steel_dark"), cut=1)
    m.round_box(al, 10.0, -9.0, 3.6, 2.0, 16.6, 23.4, metal(P, "steel", dark="steel_dark"), cut=1)
    ar = "arm_right"                                                                        # golden hook
    pts = [(-9.4, 21.0, -2.4), (-10.0, 16.0, -3.0), (-12.6, 14.0, -3.0), (-14.0, 16.0, -3.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, ar, p0, p1, 1, metal(P, "gold", dark="gold_dark"), extend=0.2, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 14.0, 0))
        rod(m, lg, (sx * 3.0, 14.0, 0), (sx * 3.4, 4.0, 0), 4, pantsf, extend=0.4)
        m.round_box(lg, sx * 3.6, -1.2, 2.8, 3.6, 0.0, 6.0, leather(P, "black", "black_dark"), cut=1)
    return m
