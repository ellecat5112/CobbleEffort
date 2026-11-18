"""Rhamphomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a violet rhamphorhynchus: a lean purple-scaled pterosaur with a long toothy beak, a pink-magenta
crest and eye-mask, great pale membrane wings on long finger bones, grasping clawed feet, and a long thin tail ending
in a chained crystal-ice mace. 15 blocks.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import gem, metal, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a lean violet pterosaur with a long toothy beak, a magenta crest, pale membrane wings and a tail ending in a chained ice mace"
BASE = {"violet": (110, 90, 200), "violet_dark": (50, 40, 120), "membrane": (200, 210, 240), "membrane_dark": (150, 160, 200),
        "magenta": (230, 60, 170), "tooth": (250, 250, 240), "claw": (40, 36, 40), "ice": (170, 220, 250),
        "steel": (180, 184, 196), "mouth": (150, 40, 70)}
SHINY = {"violet": (60, 150, 110), "violet_dark": (20, 80, 50), "magenta": (250, 160, 40)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "violet", "violet_dark", size=1.2)


def build():
    m = Model("rhamphomon")
    top = m.bone("rhamphomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 22.0, 2.0), 4.0, HIDE, layers=4, ry=4.6, squash=1.3)
    nk = m.bone("neck", bd, (0, 26, -2))
    rod(m, nk, (0, 25.0, -2.0), (0, 29.0, -6.0), 2, HIDE, extend=0.4)
    hd = m.bone("head", nk, (0, 29, -6))
    m.round_box(hd, 0, -7.0, 1.8, 2.4, 28.0, 32.0, HIDE, cut=1)
    spike(m, hd, (0, 29.6, -9.0), (0, -0.1, -1), 1.6, 9.0, HIDE, tip=0.8)                   # long beak
    for j in range(5):
        for sx in (-1, 1):
            spike(m, hd, (sx * 0.6, 29.0, -10.0 - j * 1.4), (sx * 0.2, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    m.round_box(hd, 0, -7.6, 1.9, 1.0, 30.4, 31.6, solid(P, "magenta"), cut=0)              # eye-mask
    for j in range(5):                                                                   # magenta crest
        spike(m, hd, (0, 32.0, -6.0 + j * 0.8), (0, 1, 0.4 + j * 0.2), 0.9, 3.0 + j * 0.4, strands(P, "magenta", "violet_dark"),
              tip=0.8)
    for sx in (-1, 1):                                                                   # membrane wings
        bat_wing(m, bd, (sx * 3.0, 24.0, 1.0), 32.0, 14.0, 4, HIDE, skin(P, "membrane", dark="membrane_dark"), side=sx,
                 sweep=20)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.0, 19.0, 3.0))
        rod(m, lg, (sx * 2.0, 19.0, 3.0), (sx * 2.4, 13.0, 2.0), 1, HIDE, extend=0.2, t2=2)
        for f in range(3):
            spike(m, lg, (sx * 2.4 + (f - 1) * 0.7, 12.6, 1.6), ((f - 1) * 0.3, -1, -0.6), 0.8, 2.4, solid(P, "claw"),
                  tip=0.8)
    tl = m.bone("tail", bd, (0, 21, 7))                                                  # tail + chained ice mace
    pts = [(0, 21.0, 7.0), (0, 16.0, 13.0), (2.0, 10.0, 16.0), (4.0, 5.0, 14.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, HIDE, extend=0.2, t2=1)
    rod(m, tl, pts[-1], (4.0, 3.0, 10.0), 1, metal(P, "steel"), extend=0.1, t2=1)
    ball(m, tl, (4.0, 3.0, 8.6), 2.2, gem(P, "ice", "membrane", glow=False), layers=2)
    for j in range(4):
        ang = 2 * math.pi * j / 4
        spike(m, tl, (4.0 + 2.0 * math.cos(ang), 3.0 + 2.0 * math.sin(ang), 8.6), (math.cos(ang), math.sin(ang), 0),
              0.9, 1.6, gem(P, "ice", "membrane", glow=False), tip=0.8)
    return m
