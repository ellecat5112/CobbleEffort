"""Thunderbirmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Armor Digimon of friendship: a great navy-blue thunderbird with lightning bolts
marked on its feathers, a ruff of white crest feathers, a golden beak, golden lightning-shaped tail plumes and wing
tips, and talons wreathed in sparks. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import eye, feathers, metal, plane, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a great navy thunderbird with lightning-marked feathers, a white crest ruff, a golden beak and golden lightning tail plumes"
BASE = {"navy": (40, 60, 170), "navy_dark": (16, 24, 90), "gold": (250, 200, 50), "gold_dark": (190, 130, 20),
        "white": (240, 242, 250), "white_dark": (180, 184, 200), "bolt": (255, 220, 60), "eye": (230, 40, 40),
        "pupil": (20, 10, 10), "talon": (60, 60, 70)}
SHINY = {"navy": (40, 140, 90), "navy_dark": (16, 70, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def featherf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (abs(x) * 0.7 + y * 0.5) % 6.0
    if face in ("up", "north", "south") and 1.0 < t < 1.8 and (abs(x) * 1.3 % 3.0) < 1.6:
        return tone(p["bolt"], face), None
    if abs(x) > 18.0:
        return tone(p["gold"], face), None
    return feathers(P, "navy", "navy_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 10.4, y - 25.6, 0.9, "eye", slit=True)
        if c is not None:
            return c, None
    return feathers(P, "navy", "navy_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("thunderbirmon")
    top = m.bone("thunderbirmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 18.0, 0), 5.6, feathers(P, "navy", "navy_dark"), layers=5, ry=7.0)
    hd = m.bone("head", bd, (0, 24, -6))
    ball(m, hd, (0, 25.0, -8.0), 3.4, headf, layers=3)
    spike(m, hd, (0, 24.6, -11.0), (0, -0.3, -1), 2.2, 4.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for j in range(9):                                                                 # white crest ruff
        ang = (j - 4) * 0.4
        spike(m, hd, (math.sin(ang) * 3.0, 26.0, -6.0), (math.sin(ang) * 0.8, 0.6, 1), 1.4, 6.0,
              feathers(P, "white", "white_dark"), tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 4.0, 21.0, 0))
        feather_wing(m, wb, (sx * 4.0, 21.0, 0), 24.0, 12.0, 3, featherf, side=sx, sweep=25, droop=-4.0)
    tl = m.bone("tail", bd, (0, 16, 6))                                                 # lightning tail plumes
    for j in range(4):
        x = (j - 1.5) * 2.4
        for s in range(3):
            y0 = 14.0 - s * 4.6
            m.box(tl, x - 0.8 + (s % 2) * 1.2, y0 - 5.0, 6.0 + s * 1.6, x + 0.8 + (s % 2) * 1.2, y0, 7.0 + s * 1.6,
                  solid(P, "gold"), rotation=(0, 0, 18 if s % 2 else -18), pivot=(x, y0, 6.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.4, 13.0, 0))
        rod(m, lg, (sx * 2.4, 13.0, 0), (sx * 2.6, 8.0, -1.0), 1, solid(P, "gold"), extend=0.3)
        for j in range(3):
            spike(m, lg, (sx * 2.6, 8.0, -1.0), ((j - 1) * 0.4, -0.6, -1), 0.8, 2.4, solid(P, "talon"), tip=0.8)
    return m
