"""Dorimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a round,
fluffy violet baby with two pointed cat ears, a white muzzle and chin, a big round amber eye on each side, little
white feet and a stubby tail. Baby II stage, half a block tall.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 0.7)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 6}
LOOK = "a round fluffy violet baby with pointed cat ears, a white muzzle, big amber eyes, little white feet and a stubby tail"
BASE = {"violet": (110, 100, 200), "violet_dark": (50, 44, 120), "white": (250, 250, 252), "white_dark": (200, 200, 214),
        "ear": (230, 160, 130), "eye": (220, 130, 40), "pupil": (20, 16, 16), "rim": (240, 230, 220)}
SHINY = {"violet": (130, 190, 120), "violet_dark": (60, 120, 50)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "violet", "violet_dark", length=1.0, density=2.8)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west"):
        for sx in (-1, 1):
            d = math.hypot(x - sx * 4.2, y - 10.4)
            if d < 1.9 and x * sx > 2.0:
                return tone(p["pupil"] if d < 0.7 else p["eye"] if d < 1.5 else p["rim"], face), None
    if face == "north" and y < 8.0 - abs(x) * 0.3:
        return tone(p["white"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dorimon")
    top = m.bone("dorimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 9.0, 0), 7.0, bodyf, layers=6, squash=1.1, ry=7.0)
    hd = m.bone("head", bd, (0, 15, 0))
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.4, 14.0, 1.0), (sx * 0.4, 1, 0.2), 3.0, 4.0, FUR, tip=1.0)
    m.round_box(bd, 0, 7.6, 1.6, 1.6, 6.0, 9.0, FUR, cut=1)                                # stubby tail
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 2.0, 0))
        m.round_box(lg, sx * 3.4, -1.0, 1.6, 2.0, 0.0, 3.0, fur(P, "white", "white_dark", length=0.6), cut=1)
    return m
