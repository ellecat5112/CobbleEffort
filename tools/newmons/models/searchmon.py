"""Searchmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of knowledge: a white-and-blue robot beetle with a round radar dish on its back
marked with a blue spiral, long swept antennae, a camera-lens eye on its flank, red eyes and six jointed blue-tipped
legs. 15 blocks.

Front is -z, y is up. 30 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a white-and-blue robot beetle with a round spiral radar dish on its back, long swept antennae, red eyes and six jointed legs"
BASE = {"white": (236, 238, 246), "white_dark": (160, 166, 186), "blue": (40, 70, 170), "blue_dark": (14, 30, 100),
        "eye": (230, 40, 50), "lens": (40, 40, 50), "steel": (200, 204, 216)}
SHINY = {"blue": (200, 140, 30), "blue_dark": (120, 70, 10)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "white", "white_dark", trim="blue", trim_w=0.25)


def dishf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up":
        r = math.hypot(x, z - 4.0)
        a = math.atan2(z - 4.0, x)
        if abs(((r - a * 0.8) % 2.6) - 1.3) < 0.4:
            return tone(p["blue"], face), None
    return metal(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("searchmon")
    top = m.bone("searchmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 12.0, 4.0), 8.0, SHELL, layers=5, ry=5.4, squash=1.1)
    m.round_box(bd, 0, 4.0, 11.0, 11.0, 20.0, 21.6, dishf, cut=4)                          # radar dish
    rod(m, bd, (0, 16.0, 4.0), (0, 20.0, 4.0), 2, metal(P, "steel"), extend=0.2)
    hd = m.bone("head", bd, (0, 10, -4))
    ball(m, hd, (0, 10.0, -5.0), 4.0, SHELL, layers=3)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.6), 10.6, -9.1, max(sx * 1.0, sx * 2.6), 11.6, -8.9, solid(P, "eye", glow=True))
        pts = [(sx * 1.2, 13.0, -7.0), (sx * 6.0, 18.0, -2.0), (sx * 16.0, 20.0, 6.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                  # swept antennae
            rod(m, hd, p0, p1, 1, solid(P, "white"), extend=0.2, t2=2)
    ball(m, bd, (8.0, 12.0, 0.0), 1.6, solid(P, "lens"), layers=2)                          # camera lens
    for sx in (-1, 1):
        for j, zz in enumerate((-2.0, 4.0, 10.0)):
            nm = f"leg_{('front', 'mid', 'back')[j]}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 6.0, 9.0, zz))
            rod(m, lg, (sx * 6.0, 9.0, zz), (sx * 11.0, 10.0, zz - 1.0), 2, SHELL, extend=0.4)
            rod(m, lg, (sx * 11.0, 10.0, zz - 1.0), (sx * 13.0, 1.0, zz - 2.0), 1, armour(P, "blue", "blue_dark"),
                extend=0.4, t2=2)
            spike(m, lg, (sx * 13.0, 1.0, zz - 2.0), (sx * 0.4, -0.2, -1), 1.0, 2.4, solid(P, "blue"), tip=0.8)
    return m
