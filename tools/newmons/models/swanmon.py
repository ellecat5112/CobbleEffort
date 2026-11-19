"""Swanmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of purity: a white swan with a long curving neck, a golden beak and a green eye, a
golden breastplate, great wings of white feathers tipped grey raised in a ring, and silver-and-gold armoured legs.
15 blocks.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a white swan with a long curving neck, a golden beak, a golden breastplate, great raised white wings and armoured legs"
BASE = {"white": (248, 248, 252), "white_dark": (180, 184, 200), "grey": (150, 154, 170), "gold": (240, 200, 80),
        "gold_dark": (170, 120, 30), "silver": (210, 214, 226), "eye": (90, 200, 120), "black": (30, 28, 30)}
SHINY = {"white": (60, 56, 70), "white_dark": (24, 22, 30), "grey": (130, 120, 160)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "white", "white_dark", tip="grey")


def build():
    m = Model("swanmon")
    top = m.bone("swanmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 18.0, 1.0), 5.0, FEATH, layers=4, ry=6.4)
    m.round_box(bd, 0, -4.0, 3.0, 1.0, 16.0, 22.0, armour(P, "gold", "gold_dark"), cut=0)   # golden breastplate
    nk = m.bone("neck", bd, (0, 23, -2))
    pts = [(0, 23.0, -2.0), (0, 28.0, 1.0), (0, 34.0, 0.0), (0, 36.0, -3.0)]                # curving neck
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, nk, p0, p1, 2, FEATH, extend=0.4)
    hd = m.bone("head", nk, (0, 36, -3))
    ball(m, hd, (0, 36.0, -4.0), 1.8, FEATH, layers=2)
    spike(m, hd, (0, 35.6, -5.6), (0, -0.4, -1), 1.0, 3.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 1.9), 36.4, -4.6, max(sx * 1.6, sx * 1.9), 37.0, -4.0, solid(P, "eye"))
        feather_wing(m, bd, (sx * 4.0, 22.0, 3.0), 20.0, 12.0, 6, FEATH, side=sx, sweep=10, droop=-16.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.0, 13.0, 1.0))
        rod(m, lg, (sx * 2.0, 13.0, 1.0), (sx * 2.4, 4.0, 0), 2, metal(P, "silver"), extend=0.3)
        m.round_box(lg, sx * 2.4, -0.6, 1.6, 2.2, 0.0, 4.0, metal(P, "gold", dark="gold_dark"), cut=0)
    return m
