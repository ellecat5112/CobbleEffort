"""Tobucatmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a flying-squirrel cat: a fluffy grey-and-white body with gliding membranes stretched between its
legs, chequered racing-flag stripes on its back and tail, a yellow crest tuft, big ears and violet eyes, a long broad
grey tail with a yellow tip, and red claws. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fur, plane, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a fluffy grey flying-squirrel cat with gliding membranes, chequered racing stripes, a yellow crest and a long broad tail"
BASE = {"grey": (150, 146, 160), "grey_dark": (90, 86, 100), "white": (246, 246, 250), "white_dark": (200, 200, 210),
        "black": (30, 30, 34), "yellow": (250, 220, 70), "eye": (110, 70, 190), "pupil": (20, 10, 30),
        "red": (210, 50, 50)}
SHINY = {"grey": (200, 150, 110), "grey_dark": (140, 90, 50)}


def P(v):
    return pal(BASE, SHINY, v)


GREY = fur(P, "grey", "grey_dark", length=1.0)


def checkf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up" and abs(x) < 2.0:
        return tone(p["black"] if (int(x + 10) + int(z + 40)) % 2 else p["white"], face), None
    return GREY(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            c = eye(p, a - sx * 1.6, b - 13.6, 1.0, "eye")
            if c is not None:
                return c, None
        if b < 12.0:
            return tone(p["white"], face), None
    return GREY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tobucatmon")
    top = m.bone("tobucatmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0, 4.0, 7.0, 6.0, 12.0, checkf, cut=2)
    for sx in (-1, 1):                                                                 # gliding membranes
        x0, x1 = sorted((sx * 3.6, sx * 9.0))
        m.box(bd, x0, 8.0, -5.0, x1, 8.8, 5.0, GREY)
    hd = m.bone("head", bd, (0, 12, -6))
    ball(m, hd, (0, 13.4, -7.4), 3.8, headf, layers=4)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 16.0, -6.6), (sx * 0.5, 1, 0.3), 2.0, 4.0, GREY, tip=0.8)
    for j in range(4):
        spike(m, hd, ((j - 1.5) * 0.6, 17.0, -8.0), ((j - 1.5) * 0.3, 0.6, 1), 0.9, 4.0, solid(P, "yellow"), tip=0.8)
    for sx, nm, z in ((1, "leg_front_left", -4.0), (-1, "leg_front_right", -4.0), (1, "leg_back_left", 4.0),
                      (-1, "leg_back_right", 4.0)):
        lg = m.bone(nm, bd, (sx * 8.0, 8.0, z))
        rod(m, lg, (sx * 8.0, 8.4, z), (sx * 9.6, 6.0, z - 1.0), 2, fur(P, "white", "white_dark"), extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 9.6 + (j - 1) * 0.6, 5.4, z - 1.8), (0, -0.6, -1), 0.8, 1.4, solid(P, "red"), tip=0.8)
    tl = m.bone("tail", bd, (0, 10, 7))                                                # broad tail
    pts = [(0, 10.0, 7.0), (0, 14.0, 13.0), (0, 20.0, 15.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 3, checkf, extend=0.6, t2=2)
    ball(m, tl, (0, 21.0, 15.0), 1.6, solid(P, "yellow"), layers=1)
    return m
