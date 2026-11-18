"""Pusumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round fluffy grey fur-ball, darker behind, with big teary blue eyes, a pale muzzle with a golden
pacifier in its mouth, and a yellow lightning-bolt horn on top. 0.35 blocks.

Front is -z, y is up. 14 units tall; Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "a round fluffy grey fur-ball with big blue eyes, a golden pacifier and a yellow lightning-bolt horn"
BASE = {"grey": (200, 202, 210), "grey_dark": (60, 60, 66), "white": (250, 250, 252), "eye": (120, 190, 220),
        "pupil": (20, 30, 40), "yellow": (250, 210, 50), "gold": (220, 200, 120), "gold_dark": (150, 130, 60)}
SHINY = {"grey": (240, 210, 150), "grey_dark": (120, 80, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 5.6)
            if math.hypot(x - sx * 1.8 + 0.3, y - 6.0) < 0.3:
                return tone(p["white"], face), None
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.1:
                return tone(p["eye"], face), None
        if abs(x) < 2.0 and y < 4.6:
            return tone(p["white"], face), None
    if z > 1.0:
        return fur(P, "grey_dark", "grey_dark", length=1.0)(x, y, z, face, variant, box=box, **k)
    return fur(P, "grey", "grey_dark", length=1.0, density=1.4)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pusumon")
    top = m.bone("pusumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 5.0, 0.4), 5.0, furf, layers=4, ry=4.4)
    ball(m, bd, (0, 3.4, -4.6), 1.0, metal(P, "gold", dark="gold_dark"), layers=2)          # pacifier
    m.box(bd, -0.4, 9.0, -0.6, 0.4, 12.0, 0.4, solid(P, "yellow"), rotation=(0, 0, 25), pivot=(0, 9.0, 0))
    m.box(bd, -0.4, 11.0, -0.6, 0.4, 14.0, 0.4, solid(P, "yellow"), rotation=(0, 0, -30), pivot=(0, 11.0, 0))
    return m
