"""Skull Satamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a red skeletal demon: a gaunt red-and-black bone body with a horned skull, ragged black
bat wings, violet-banded steel greaves and gauntlets, and a long red bone staff topped with a golden orb and ending in
a hooked claw. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a gaunt red skeletal demon with a horned skull, ragged black bat wings, violet-banded steel greaves and a golden-orb bone staff"
BASE = {"red": (190, 40, 40), "red_dark": (100, 14, 14), "black": (30, 28, 32), "black_dark": (10, 10, 12),
        "violet": (120, 80, 190), "steel": (190, 194, 206), "steel_dark": (90, 94, 108), "gold": (250, 210, 60),
        "eye": (250, 220, 60), "bone": (230, 220, 200)}
SHINY = {"red": (60, 60, 70), "red_dark": (20, 20, 26)}


def P(v):
    return pal(BASE, SHINY, v)


def bonef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 36.0 < y < 50.0 and abs((y % 2.4) - 1.2) < 0.4 and abs(x) > 0.8:
        return tone(p["black"], face), None
    return skin(P, "red", dark="red_dark")(x, y, z, face, variant, box=box, **k)


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y % 4.0) < 1.0:
        return tone(p["violet"], face), None
    return metal(P, "steel", dark="steel_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("skullsatamon")
    mats = {"skin": bonef, "forearm": bandf, "shin": bandf, "calf": bandf, "foot": bandf, "talon": metal(P, "steel"),
            "claw": metal(P, "steel")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, talons=True, claws=True, name="skullsatamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.0, solid(P, "bone"), cut=1)                  # horned skull
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 57.0, -3.5, max(sx * 0.6, sx * 2.0), 58.2, -3.3, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 60.0, -0.4), (sx * 0.6, 1, 0.2), 1.4, 6.0, solid(P, "black"), tip=0.8)
        bat_wing(m, bd, (sx * 3.0, 50.0, 3.0), 24.0, 14.0, 4, metal(P, "black"), skin(P, "black", dark="black_dark"),
                 side=sx, sweep=20)
    w = a["arm_right"]["wrist"]                                                          # golden-orb bone staff
    ab = a["arm_right"]["bone"]
    rod(m, ab, (w[0], 4.0, w[2] - 2.0), (w[0], 66.0, w[2] - 2.0), 1, solid(P, "red"), extend=0.2)
    ball(m, ab, (w[0], 68.0, w[2] - 2.0), 2.0, metal(P, "gold"), layers=2)
    for sx in (-1, 1):
        spike(m, ab, (w[0], 66.0, w[2] - 2.0), (sx * 0.6, 0.8, 0), 1.0, 4.0, solid(P, "red"), tip=0.8)
    pts = [(w[0], 4.0, w[2] - 2.0), (w[0] + 2.0, 2.0, w[2] - 4.0), (w[0] + 1.0, 3.0, w[2] - 6.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, ab, p0, p1, 1, solid(P, "red"), extend=0.1, t2=1)
    return m
