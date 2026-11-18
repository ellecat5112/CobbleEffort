"""Piyomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a pink bird with fluffy feathers tipped blue, a big red beak, round blue eyes, a curled feather crest
striped pink and blue, wing-arms with red claws, a ring on one leg and yellow taloned feet with red claws. 1 block tall.

Front is -z, y is up. 28 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a pink bird with blue-tipped fluffy feathers, a big red beak, round blue eyes, a curled striped crest and yellow red-clawed feet"
BASE = {"pink": (240, 150, 190), "pink_dark": (190, 90, 140), "blue": (60, 90, 200), "red": (220, 50, 40),
        "yellow": (250, 210, 60), "eye": (60, 120, 220), "white": (250, 250, 250), "steel": (200, 204, 216)}
SHINY = {"pink": (240, 220, 120), "pink_dark": (190, 160, 60), "blue": (200, 70, 60)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "pink", "pink_dark", tip="blue")


def crestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["blue"] if (y + z) % 2.0 < 0.8 else p["pink"], face), None


def build():
    m = Model("piyomon")
    top = m.bone("piyomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 12.0, 0.4), 5.0, FEATH, layers=5, ry=6.0)
    hd = m.bone("head", bd, (0, 17, 0))
    ball(m, hd, (0, 19.6, -0.4), 4.0, FEATH, layers=4, ry=3.6)
    m.round_box(hd, 0, -5.4, 1.8, 2.0, 17.6, 20.0, solid(P, "red"), cut=1)                 # big red beak
    spike(m, hd, (0, 18.6, -7.2), (0, -1, -0.4), 1.2, 1.6, solid(P, "red"), tip=0.8)
    for sx in (-1, 1):
        ball(m, hd, (sx * 2.0, 20.8, -3.2), 1.0, solid(P, "white"), layers=2, squash=0.5)
        m.box(hd, sx * 2.0 - 0.4, 20.4, -3.75, sx * 2.0 + 0.4, 21.2, -3.65, solid(P, "eye"))
    pts = [(0, 23.0, 0), (0.4, 26.0, 1.0), (1.6, 27.4, 0.6), (2.2, 26.4, -0.4)]
    for p0, p1 in zip(pts, pts[1:]):                                                     # curled crest
        rod(m, hd, p0, p1, 1, crestf, extend=0.2, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.4, 14.0, 0))
        x0, x1 = sorted((sx * 4.0, sx * 8.0))
        m.box(ab, x0, 9.0, -1.0, x1, 15.0, 1.0, FEATH, rotation=(0, 0, sx * 15), pivot=(sx * 4.0, 14.0, 0))
        for f in range(3):
            spike(m, ab, (sx * 7.4, 9.0, -0.6 + f * 0.6), (sx * 0.2, -1, -0.4), 0.8, 2.4, solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 7.0, 0))
        rod(m, lg, (sx * 2.0, 7.0, 0), (sx * 2.4, 2.0, 0), 1, solid(P, "yellow"), extend=0.2, t2=2)
        if sx > 0:
            m.round_box(lg, 2.2, 0, 1.2, 1.2, 3.6, 4.4, metal(P, "steel"), cut=0)
        for f in range(3):
            spike(m, lg, (sx * 2.4 + (f - 1) * 0.8, 0.8, -0.6), ((f - 1) * 0.3, -0.4, -1), 0.8, 2.6, solid(P, "red"),
                  tip=0.8)
    return m
