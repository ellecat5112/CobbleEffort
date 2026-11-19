"""Sheepmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of friendship: a round pink woolly sheep with a dark grey face and legs, big
curling red-and-white striped ram horns, little hooves, and two grey smiley-faced cannon barrels strapped to its back.
15 blocks.

Front is -z, y is up. 28 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a round pink woolly sheep with a dark grey face, curling red-and-white striped ram horns and two smiley cannon barrels on its back"
BASE = {"pink": (246, 200, 220), "pink_dark": (220, 150, 180), "grey": (80, 80, 86), "grey_dark": (40, 40, 44),
        "red": (210, 40, 50), "white": (250, 250, 250), "steel": (190, 194, 206), "steel_dark": (100, 104, 118),
        "yellow": (250, 230, 120), "eye": (250, 220, 60), "black": (24, 24, 28)}
SHINY = {"pink": (240, 240, 246), "pink_dark": (190, 190, 206)}


def P(v):
    return pal(BASE, SHINY, v)


WOOL = fur(P, "pink", "pink_dark", length=1.0, density=1.2)


def hornf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y + z) % 2.0 < 1.0 else p["white"], face), None


def build():
    m = Model("sheepmon")
    top = m.bone("sheepmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for c, r in (((0, 14.0, 2.0), 8.0), ((-4.0, 15.0, 6.0), 5.0), ((4.0, 15.0, 6.0), 5.0), ((0, 17.0, -2.0), 5.0)):
        ball(m, bd, c, r, WOOL, layers=5)
    hd = m.bone("head", bd, (0, 14, -7))
    m.round_box(hd, 0, -9.0, 3.0, 2.8, 10.0, 16.0, skin(P, "grey", dark="grey_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 13.6, -11.9, max(sx * 1.0, sx * 2.4), 14.6, -11.7, solid(P, "eye"))
        pts = [(sx * 2.6, 15.0, -8.0), (sx * 6.0, 18.0, -7.0), (sx * 8.0, 15.0, -6.0), (sx * 7.0, 12.0, -6.0),
               (sx * 5.0, 13.0, -7.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                  # curling ram horns
            rod(m, hd, p0, p1, 2, hornf, extend=0.3)
    ball(m, hd, (0, 16.0, -7.0), 2.4, WOOL, layers=2)
    for sx in (-1, 1):                                                                   # smiley cannons
        rod(m, bd, (sx * 3.4, 22.0, 6.0), (sx * 3.4, 22.0, -4.0), 4, metal(P, "steel", dark="steel_dark"), extend=0.2)
        m.round_box(bd, sx * 3.4, -4.4, 1.6, 0.4, 20.4, 23.6, solid(P, "yellow"), cut=0)
        m.box(bd, sx * 3.4 - 0.8, 22.2, -4.9, sx * 3.4 + 0.8, 22.6, -4.7, solid(P, "black"))
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        zz = -3.0 if "front" in nm else 6.0
        lg = m.bone(nm, top, (sx * 4.0, 8.0, zz))
        ball(m, lg, (sx * 4.0, 6.0, zz), 2.6, WOOL, layers=2)
        m.round_box(lg, sx * 4.0, zz, 1.4, 1.4, 0.8, 5.0, skin(P, "grey", dark="grey_dark"), cut=0)
        m.round_box(lg, sx * 4.0, zz, 1.6, 1.8, 0.0, 1.2, solid(P, "black"), cut=0)
    return m
