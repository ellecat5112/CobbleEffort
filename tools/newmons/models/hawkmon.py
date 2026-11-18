"""Hawkmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little red hawk: a round red bird with a white face and chest ruff, a yellow beak, blue eyes, a headband with goggles
and a single orange crest feather, big red wings tipped black and fluffy yellow legs with grey talons. Child stage.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, fur, leather, metal, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a round red hawk with a white face and ruff, a yellow beak, goggles on a headband, big black-tipped wings and yellow legs"
BASE = {"red": (220, 40, 40), "red_dark": (140, 14, 18), "white": (246, 246, 250), "white_dark": (190, 192, 206),
        "beak": (250, 200, 40), "eye": (60, 120, 220), "black": (30, 28, 32), "yellow": (250, 210, 50),
        "yellow_dark": (200, 150, 20), "grey": (150, 150, 160), "band": (60, 60, 70), "orange": (250, 140, 40)}
SHINY = {"red": (60, 140, 220), "red_dark": (20, 70, 150)}


def P(v):
    return pal(BASE, SHINY, v)


RED = feathers(P, "red", "red_dark", size=(1.0, 1.6))


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 3.6 and y < 15.0:
        return fur(P, "white", "white_dark", length=0.8)(x, y, z, face, variant, box=box, **k)
    return RED(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hawkmon")
    top = m.bone("hawkmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 11.0, 0), 5.4, bodyf, layers=5)
    hd = m.bone("head", bd, (0, 16, -1))
    m.round_box(hd, 0, -1.0, 4.0, 3.6, 14.6, 22.0, fur(P, "white", "white_dark", length=0.8), cut=2)
    spike(m, hd, (0, 17.0, -4.6), (0, -0.6, -1), 2.0, 3.0, solid(P, "beak"), tip=0.8)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.8, -4.6, 0.8, 0.3, 18.0, 19.6, solid(P, "eye"), cut=0)
    m.round_box(hd, 0, -0.6, 4.2, 3.8, 19.6, 21.0, leather(P, "band", "black"), cut=1)          # headband
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.6, -4.4, 1.2, 0.4, 19.8, 21.2, metal(P, "grey", dark="black"), cut=0)
    spike(m, hd, (0, 21.6, 0), (0.2, 1, 0.4), 1.4, 5.0, solid(P, "orange"), tip=0.8)          # crest feather
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 13.0, 0))
        feather_wing(m, wb, (side * 5.0, 13.0, 0), 11.0, 7.0, 2, feathers(P, "red", "red_dark", tip="black"),
                     side=side, sweep=5, droop=-10.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 6.0, 0))
        m.round_box(lg, sx * 2.4, 0, 1.8, 1.8, 2.0, 7.0, fur(P, "yellow", "yellow_dark"), cut=1)
        for j in range(3):
            spike(m, lg, (sx * 2.4 + (j - 1) * 1.0, 1.0, -1.4), (0, -0.3, -1), 0.8, 2.0, solid(P, "grey"), tip=0.8)
    return m
