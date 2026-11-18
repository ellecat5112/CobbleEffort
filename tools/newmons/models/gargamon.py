"""Gargamon (Gaagamon on wikimon) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art
on wikimon.net): the little crow: a violet-blue crow with a red eye, a grey beak, a white crest feather, a ragged white
cloth wrapped round its chest and dark wings fringed in grey, standing on orange talons. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import fabric, feathers, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a violet-blue crow with a red eye, a grey beak, a white crest feather, a ragged white chest cloth and dark wings"
BASE = {"violet": (70, 70, 160), "violet_dark": (30, 30, 90), "grey": (150, 150, 160), "white": (240, 240, 236),
        "white_dark": (180, 180, 170), "eye": (210, 30, 40), "talon": (240, 160, 60), "black": (30, 28, 34)}
SHINY = {"violet": (40, 40, 44), "violet_dark": (14, 14, 18)}


def P(v):
    return pal(BASE, SHINY, v)


FEATHER = feathers(P, "violet", "violet_dark", size=(1.0, 1.6))


def build():
    m = Model("gargamon")
    top = m.bone("gargamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 12.0, 0), 5.6, FEATHER, layers=5, ry=6.4)
    m.round_box(bd, 0, -0.6, 5.0, 5.0, 8.0, 14.0, fabric(P, "white", "white_dark"), cut=2)      # ragged cloth
    for j in range(5):
        spike(m, bd, ((j - 2) * 2.0, 8.0, -4.6), (0, -1, -0.2), 1.6, 2.6, fabric(P, "white", "white_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 18, -1))
    m.round_box(hd, 0, -1.0, 3.6, 3.4, 16.0, 23.0, FEATHER, cut=2)
    spike(m, hd, (0, 19.0, -4.4), (0, -0.4, -1), 2.0, 4.0, solid(P, "grey"), tip=0.8)          # beak
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.8, -4.2, 0.8, 0.3, 20.0, 21.6, solid(P, "eye"), cut=0)
    spike(m, hd, (0.6, 22.6, -1.0), (0.3, 1, 0.6), 1.2, 5.0, solid(P, "white"), tip=0.8)       # crest feather
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 15.0, 0))
        feather_wing(m, wb, (side * 5.0, 15.0, 0), 8.0, 5.0, 2, FEATHER, side=side, sweep=10, droop=-6.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 6.0, 0))
        rod(m, lg, (sx * 2.0, 7.0, 0), (sx * 2.0, 1.0, 0), 1, solid(P, "talon"), extend=0.2, t2=1)
        for j in range(3):
            spike(m, lg, (sx * 2.0, 0.6, 0), ((j - 1) * 0.6, -0.1, -1), 0.8, 2.6, solid(P, "talon"), tip=0.8)
    return m
