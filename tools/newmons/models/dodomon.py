"""Dodomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a round,
fluffy purple baby blob with two pointed cat ears, a white zigzag-edged belly like a toothy grin, and big round brown
eyes. Baby I stage, a third of a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 0.5)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 4}
LOOK = "a round fluffy purple blob with pointed cat ears, a white zigzag belly and big round brown eyes"
BASE = {"purple": (120, 110, 200), "purple_dark": (60, 50, 130), "white": (250, 250, 252), "ear": (230, 160, 130),
        "eye": (180, 100, 40), "pupil": (20, 16, 16), "rim": (240, 230, 220)}
SHINY = {"purple": (210, 130, 170), "purple_dark": (140, 60, 100)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "purple", "purple_dark", length=1.0, density=2.8)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 3.0, y - 8.6)
            if d < 0.7:
                return tone(p["pupil"], face), None
            if d < 1.6:
                return tone(p["eye"], face), None
            if d < 1.9:
                return tone(p["rim"], face), None
        if y < 6.0 - abs((x * 0.8) % 2.0 - 1.0) * 1.2:
            return tone(p["white"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dodomon")
    top = m.bone("dodomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 0, 0))
    ball(m, bd, (0, 7.0, 0), 7.0, bodyf, layers=6, squash=0.9, ry=6.4)
    hd = m.bone("head", bd, (0, 12, 0))
    for sx in (-1, 1):                                                       # pointed cat ears
        spike(m, hd, (sx * 3.6, 11.6, 0.4), (sx * 0.4, 1, 0), 3.0, 4.0, FUR, tip=1.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        m.bone(nm, top, (sx * 3.0, 1.0, 0))
    return m
