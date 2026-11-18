"""Kudamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the pipe
fox: a slender white fox with a long tapering snout, narrow golden eyes, pointed black-tipped ears, violet swirling
markings, a grey metal collar, red claws, and a long violet-patterned tail coiled round a brass-capped bamboo bullet
pipe. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "quadruped"
K = 4
LOOK = "a slender white fox with violet swirl markings, black-tipped ears, a metal collar and a long tail coiled round a brass bullet pipe"
BASE = {"white": (240, 240, 250), "white_dark": (170, 170, 196), "violet": (130, 100, 200), "black": (24, 24, 30),
        "eye": (230, 180, 60), "red": (210, 40, 60), "steel": (150, 154, 166), "steel_dark": (80, 84, 96),
        "brass": (210, 170, 80), "brass_dark": (140, 100, 30), "bamboo": (240, 230, 200)}
SHINY = {"white": (250, 230, 170), "white_dark": (200, 170, 100), "violet": (200, 80, 80)}


def P(v):
    return pal(BASE, SHINY, v)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(math.sin(z * 0.7 + y * 0.5)) > 0.9 and y > 8.0:
        return tone(p["violet"], face), None
    return fur(P, "white", "white_dark", length=0.8)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kudamon")
    top = m.bone("kudamon", None, (0, 0, 0))
    pp = m.bone("pipe", top, (0, 3, 2))                                              # bamboo bullet pipe
    rod(m, pp, (-6.0, 3.0, 4.0), (6.0, 3.0, 2.0), 3, metal(P, "bamboo", dark="white_dark"), extend=0)
    m.round_box(pp, 7.0, 2.0, 1.2, 3.0, 0.0, 6.0, metal(P, "brass", dark="brass_dark"), cut=1)
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.6, 2.8, 3.4, 6.0, 15.0, coatf, cut=1)
    m.round_box(bd, 0, 0.0, 2.8, 2.8, 14.4, 16.0, metal(P, "steel", dark="steel_dark"), cut=1)      # collar
    hd = m.bone("head", bd, (0, 16, -1))
    m.round_box(hd, 0, -1.0, 2.4, 2.8, 16.0, 21.0, coatf, cut=1)
    spike(m, hd, (0, 17.6, -3.6), (0, -0.2, -1), 1.8, 4.0, skin(P, "white", dark="white_dark"), tip=0.8)
    m.box(hd, -0.5, 17.0, -7.7, 0.5, 17.8, -7.4, solid(P, "black"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.0), 19.0, -3.9, max(sx * 1.0, sx * 2.0), 19.6, -3.7, solid(P, "eye"))
        spike(m, hd, (sx * 1.6, 20.6, -0.4), (sx * 0.4, 1, 0.3), 1.4, 4.0, coatf, tip=0.8)
        spike(m, hd, (sx * 2.3, 23.6, 0.6), (sx * 0.4, 1, 0.3), 0.8, 1.6, solid(P, "black"), tip=0.8)
    for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                       (-1, 1, "leg_back_right")):
        lg = m.bone(nm, bd, (sx * 1.8, 7.0, sz * 2.0))
        rod(m, lg, (sx * 1.8, 7.0, sz * 2.0), (sx * 2.2, 3.4, sz * 2.0 - 1.0), 1, coatf, extend=0.3, t2=1)
        spike(m, lg, (sx * 2.2, 3.4, sz * 2.0 - 1.4), (0, -0.4, -1), 0.8, 1.6, solid(P, "red"), tip=0.8)
    tb = m.bone("tail", bd, (0, 8, 3))
    pts = [(0, 8.0, 3.4), (-3.0, 6.0, 8.0), (-6.0, 4.0, 6.0), (-5.0, 5.0, 1.0), (0, 6.0, -1.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, coatf, extend=0.6)
    return m
