"""Saberdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a giant bird of darkness: a body of smoky black-grey feathers that tear away into dark flame at
every edge, two great ragged wings raised high, a pale bony beak with jagged fangs and a red tongue, and hooked pale
talons. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a giant bird of smoky black-grey feathers tearing into dark flame, great ragged raised wings, a fanged bony beak and pale talons"
BASE = {"grey": (80, 80, 88), "grey_dark": (24, 24, 30), "bone": (230, 226, 190), "bone_dark": (170, 160, 120),
        "red": (200, 40, 40), "eye": (240, 60, 60)}
SHINY = {"grey": (110, 60, 140), "grey_dark": (40, 14, 60)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "grey", "grey_dark", tip="grey_dark", size=(1.4, 2.4))


def build():
    m = Model("saberdramon")
    top = m.bone("saberdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 18.0, 2.0), 6.0, FEATH, layers=5, ry=7.0, squash=1.2)
    for j in range(8):                                                                   # flame-torn feather edges
        ang = 2 * math.pi * j / 8
        spike(m, bd, (5.0 * math.cos(ang), 14.0, 2.0 + 6.0 * math.sin(ang)), (math.cos(ang) * 0.5, -1, math.sin(ang) * 0.5),
              1.6, 5.0, FEATH, tip=0.8)
    nk = m.bone("neck", bd, (0, 22, -4))
    rod(m, nk, (0, 22.0, -3.0), (0, 18.0, -9.0), 4, FEATH, extend=0.6)
    hd = m.bone("head", nk, (0, 16, -11))
    ball(m, hd, (0, 16.0, -11.0), 3.4, FEATH, layers=3)
    spike(m, hd, (0, 15.6, -14.0), (0, -0.4, -1), 2.4, 6.0, solid(P, "bone"), tip=0.8)      # bony beak
    jb = m.bone("jaw", hd, (0, 14, -13))
    spike(m, jb, (0, 13.6, -13.6), (0, -0.8, -0.8), 1.6, 4.0, solid(P, "bone"), tip=0.8)
    rod(m, hd, (0, 14.4, -14.0), (0.6, 11.0, -16.0), 1, solid(P, "red"), extend=0.2, t2=1)
    for j in range(3):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.0, 14.6, -14.6 - j * 1.2), (0, -1, 0), 0.8, 1.4, solid(P, "bone"), tip=0.8)
        spike(m, hd, ((j - 1) * 1.4, 18.6, -10.0), ((j - 1) * 0.3, 1, 0.6), 1.2, 4.0, FEATH, tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.8, sx * 3.1), 17.0, -13.0, max(sx * 2.8, sx * 3.1), 17.8, -11.8, solid(P, "eye", glow=True))
        feather_wing(m, bd, (sx * 4.0, 22.0, 3.0), 22.0, 12.0, 6, FEATH, side=sx, sweep=15, droop=-14.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.4, 12.0, -2.0))
        rod(m, lg, (sx * 2.4, 12.0, -2.0), (sx * 3.0, 6.0, -6.0), 2, solid(P, "bone_dark"), extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 3.0 + (f - 1) * 1.0, 5.6, -6.4), ((f - 1) * 0.3, -1, -0.8), 1.0, 4.0, solid(P, "bone"),
                  tip=0.8)
    return m
