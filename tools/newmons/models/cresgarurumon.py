"""Cres Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the moonlit wolf knight. A lean wolf-headed knight in gold-and-black striped armour, a
long white mane streaming back, a tattered violet cape, gold blade fins on its arms and legs, a long spear in one
hand and a great curved crescent blade in the other, and a gold-clawed wolf tail. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean wolf-headed knight in gold-and-black striped armour with a long white mane, a tattered violet cape, "
        "a long spear and a great curved crescent blade")
BASE = {"gold": (230, 186, 70), "gold_dark": (150, 110, 20), "gold_light": (255, 236, 160), "black": (34, 32, 40),
        "white": (240, 240, 246), "white_dark": (180, 184, 200), "violet": (90, 70, 170), "violet_dark": (40, 26, 90),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "eye": (250, 60, 60), "under": (40, 40, 50)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 150), "gold_light": (255, 255, 255), "violet": (160, 30, 50),
         "violet_dark": (80, 10, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def stripedgold(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y * 0.8 + abs(x) * 0.5) % 3.2 < 0.6:
        return tone(p["black"], face), None
    return armour(P, "gold", "gold_dark", light="gold_light")(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("cresgarurumon")
    mats = {"skin": solid(P, "under"), "chest": stripedgold, "abs": stripedgold, "pelvis": stripedgold,
            "deltoid": stripedgold, "forearm": stripedgold, "hand": stripedgold, "finger": STEEL, "claw": STEEL,
            "thigh": stripedgold, "knee": stripedgold, "shin": stripedgold, "calf": stripedgold, "foot": stripedgold,
            "talon": STEEL}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="cresgarurumon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 3.0, 54.4, 61.0, stripedgold, cut=1)
    m.box(hd, -1.8, 54.6, -7.4, 1.8, 57.4, -3.0, stripedgold)                     # wolf muzzle
    m.box(hd, -2.0, 58.0, -3.9, 2.0, 58.6, -3.5, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 60.6, -0.4), (sx * 0.3, 1, 0.4), 1.6, 5.0, stripedgold, tip=0.3)
    for i in range(10):                                                           # long white mane
        ang = math.radians(-90 + i * 20)
        rod(m, hd, (2.4 * math.sin(ang), 60.0, 1.0), (5.0 * math.sin(ang), 46.0 + abs(math.cos(ang)) * 4, 10.0),
            2, strands(P, "white", "white_dark"), extend=0.3, t2=1)
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                 # gold blade fins
        ab = a[nm]
        p0 = ab.get("elbow", ab.get("knee"))
        sx = 1 if nm.endswith("left") else -1
        spike(m, ab["bone"], (p0[0] + sx * 1.6, p0[1], p0[2] + 1.0), (sx * 0.6, 0.6, 0.6), 1.6, 5.0, metal(P, "gold", dark="gold_dark"), tip=0.3)
    cb = m.bone("cap", bd, (0, 52, 3))
    cape(m, cb, 52.0, 18.0, 40.0, fabric(P, "violet", "violet_dark", axis="y"), z=4.2, flare=1.1, panels=8,
         sweep=(0, 6), seed=11)
    ar = a["arm_right"]                                                           # the long spear
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 14.0, h[2]), (h[0], h[1] + 26.0, h[2]), 1, solid(P, "black"), extend=0)
    spike(m, ar["bone"], (h[0], h[1] + 26.0, h[2]), (0, 1, 0), 2.0, 6.0, STEEL, tip=0.4)
    al = a["arm_left"]                                                            # the crescent blade
    h = al["hand"]
    pts = []
    for i in range(9):
        ang = math.radians(-70 + i * 17)
        pts.append((h[0] + 4.0, h[1] - 6.0 + 16.0 * math.sin(ang), h[2] - 2.0 - 10.0 * math.cos(ang)))
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, al["bone"], p0, p1, 1, STEEL, extend=0.4, t2=3)
    tl = m.bone("tail", bd, (0, 31, 3))
    pts = [(0, 31.0, 3.0), (1.0, 25.0, 9.0), (2.0, 19.0, 12.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, strands(P, "white", "white_dark"), extend=0.4)
    spike(m, tl, pts[-1], (0.2, -1, 0.4), 1.4, 3.0, metal(P, "gold", dark="gold_dark"))
    return m
