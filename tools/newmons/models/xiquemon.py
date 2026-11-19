"""Xiquemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a magpie of sky and sea: a sleek navy-black bird with a teal scaled breast fastened with gold frog
buttons, a red neck tie, gold goggles over its eyes, a hooked pale beak, great wings of black and silver-white
feathers tipped teal, and long teal-scaled legs with black talons. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, metal, scales, solid
from _route import pal, tone

HEIGHT = 38
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a sleek navy-black magpie with a teal scaled breast, gold goggles, a red tie and great black-and-silver wings tipped teal"
BASE = {"navy": (30, 36, 70), "navy_dark": (10, 12, 26), "teal": (40, 150, 150), "teal_dark": (14, 80, 90),
        "white": (230, 234, 244), "white_dark": (160, 166, 190), "gold": (240, 196, 60), "red": (190, 30, 50),
        "beak": (230, 220, 200), "black": (20, 20, 24)}
SHINY = {"navy": (240, 240, 246), "navy_dark": (170, 170, 190), "teal": (200, 100, 150), "teal_dark": (130, 40, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 20.0:
        return tone(p["teal"], face), None
    if abs(x) > 10.0:
        return feathers(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)
    return feathers(P, "navy", "navy_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("xiquemon")
    top = m.bone("xiquemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 19.0, 0), 4.6, feathers(P, "navy", "navy_dark"), layers=4, ry=6.0)
    ball(m, bd, (0, 18.0, -2.6), 3.6, scales(P, "teal", "teal_dark", size=0.8), layers=3, squash=0.6)
    for j in range(3):
        m.box(bd, -1.4, 15.0 + j * 2.0, -6.4, 1.4, 15.6 + j * 2.0, -6.0, metal(P, "gold"))
    m.box(bd, -0.8, 13.0, -6.6, 0.8, 21.0, -6.2, solid(P, "red"))
    hd = m.bone("head", bd, (0, 25, -3))
    ball(m, hd, (0, 26.4, -3.6), 2.8, feathers(P, "navy", "navy_dark"), layers=3)
    spike(m, hd, (0, 26.0, -6.2), (0, -0.5, -1), 1.4, 3.6, metal(P, "beak"), tip=0.8)
    m.box(hd, -2.8, 27.0, -6.4, 2.8, 28.2, -5.8, metal(P, "gold"))
    for j in range(4):
        spike(m, hd, ((j - 1.5) * 0.5, 28.6, -2.0), ((j - 1.5) * 0.2, 1, 0.8), 0.9, 5.0, feathers(P, "navy", "black"),
              tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 22.0, 0))
        feather_wing(m, wb, (sx * 3.0, 22.0, 0), 26.0, 12.0, 3, wingf, side=sx, sweep=35, droop=-12.0)
        lg = m.bone("leg_" + ("left" if sx > 0 else "right"), bd, (sx * 1.8, 14.0, 0))
        rod(m, lg, (sx * 1.8, 14.0, 0), (sx * 2.4, 4.0, -1.0), 1, scales(P, "teal", "teal_dark"), extend=0.3)
        for t in range(3):
            spike(m, lg, (sx * 2.4, 4.0, -1.0), ((t - 1) * 0.5, -0.6, -1), 0.9, 3.0, solid(P, "black"), tip=0.8)
    for j in range(3):
        spike(m, bd, ((j - 1) * 1.0, 16.0, 4.0), ((j - 1) * 0.2, -0.4, 1), 1.2, 8.0, feathers(P, "navy", "black"), tip=0.8)
    return m
