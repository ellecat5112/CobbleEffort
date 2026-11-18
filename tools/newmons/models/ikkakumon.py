"""Ikkakumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
one-horned walrus beast: a great shaggy body of white fur, a single long dark horn rising from its brow, blue eyes in a
dark mask, a gaping red maw with two long ivory tusks, a white beard, wispy feelers by its ears and four short legs
with red claws. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.6)
KIND = "quadruped"
K = 3
LOOK = "a great shaggy white walrus beast with one long dark horn, blue eyes, a red maw with long ivory tusks and red claws"
BASE = {"white": (246, 246, 250), "white_dark": (170, 176, 200), "horn": (60, 50, 70), "horn_light": (130, 120, 140),
        "eye": (60, 140, 230), "mask": (60, 60, 80), "mouth": (200, 40, 50), "mouth_dark": (120, 14, 24),
        "tusk": (246, 236, 200), "claw": (220, 40, 40), "paw": (90, 70, 90)}
SHINY = {"white": (240, 220, 170), "white_dark": (190, 160, 110)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=2.0)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.6) < 0.8 and abs(y - 26.4) < 0.6:
                return tone(p["eye"], face), None
            if abs(x - sx * 2.6) < 1.8 and abs(y - 26.4) < 1.2:
                return tone(p["mask"], face), None
        if 17.0 < y < 23.6 and abs(x) < 3.6 - abs(y - 20.3) * 0.3:
            return tone(p["mouth_dark"] if abs(x) < 1.6 and y < 21.0 else p["mouth"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ikkakumon")
    top = m.bone("ikkakumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 13.0, 3.0), 11.0, FUR, layers=7, squash=1.0)
    hd = m.bone("head", bd, (0, 22, -6))
    m.round_box(hd, 0, -6.0, 6.0, 5.0, 16.0, 30.0, facef, cut=2)
    pts = [(0, 29.0, -7.0), (-2.0, 34.0, -10.0), (-4.0, 38.0, -14.0)]                          # single horn
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 2 - j, solid(P, "horn" if j else "horn_light"), extend=0.3, t2=2 - j)
    spike(m, hd, pts[-1], (-0.4, 0.8, -0.6), 1.0, 3.0, solid(P, "horn"), tip=0.8)
    for sx in (-1, 1):
        pts = [(sx * 1.8, 18.6, -11.4), (sx * 2.0, 14.0, -12.6), (sx * 1.6, 9.0, -12.0)]       # ivory tusks
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "tusk"), extend=0.3, t2=2)
        fp = [(sx * 5.6, 27.0, -4.0), (sx * 9.0, 28.0, -2.0), (sx * 12.0, 26.0, 0.0)]          # wispy feelers
        for p0, p1 in zip(fp, fp[1:]):
            rod(m, hd, p0, p1, 1, strands(P, "white", "white_dark"), extend=0.2, t2=1)
    for i in range(9):                                                                     # shaggy beard
        ang = math.radians(-80 + i * 20)
        spike(m, hd, (5.4 * math.sin(ang), 17.0, -6.0 - 4.0 * math.cos(ang)), (math.sin(ang) * 0.3, -1, -0.3), 2.4,
              5.0, FUR, tip=0.8)
    for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                       (-1, 1, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 6.0, 6.0, sz * 6.0))
        m.round_box(lg, sx * 7.0, sz * 6.0 - 1.0, 3.0, 3.6, 0.0, 6.0, FUR, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 7.0 + (j - 1) * 1.6, 0.8, sz * 6.0 - 4.4), (0, -0.2, -1), 1.0, 2.0, solid(P, "claw"),
                  tip=0.8)
    return m
