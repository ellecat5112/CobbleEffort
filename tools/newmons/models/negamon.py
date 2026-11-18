"""Negamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a mysterious dark-blue blob with one huge yellow eye, a long thin feeler arching from its crown and
a skirt of tentacles dotted with red suckers trailing away into wisps of dark mist. 0.5 blocks tall.

Front is -z, y is up. 20 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a dark-blue blob with one huge yellow eye, a long feeler and a skirt of red-dotted tentacles trailing into mist"
BASE = {"blue": (60, 66, 110), "blue_dark": (24, 26, 56), "red": (210, 50, 60), "white": (250, 250, 250),
        "eye": (250, 210, 40), "pupil": (16, 16, 20), "mist": (90, 70, 130, 150)}
SHINY = {"blue": (120, 60, 110), "blue_dark": (60, 20, 60), "eye": (120, 230, 120)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "blue", dark="blue_dark")


def tentf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and math.sin(y * 3.0) * math.sin(x * 3.0 + z * 3.0) > 0.7:
        return tone(p["red"], face), None
    return BODY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("negamon")
    top = m.bone("negamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 13.0, 0), 4.6, BODY, layers=4, ry=4.4)
    ball(m, bd, (0, 13.6, -3.6), 2.6, solid(P, "white"), layers=3, squash=0.5)              # huge eye
    m.round_box(bd, 0, -4.9, 1.8, 0.3, 11.8, 15.4, solid(P, "eye"), cut=0)
    m.box(bd, -0.7, 12.9, -5.3, 0.7, 14.3, -5.2, solid(P, "pupil"))
    pts = [(0, 17.0, 0), (1.0, 20.0, 1.0), (4.0, 21.0, 2.0), (6.0, 19.0, 2.6)]
    for p0, p1 in zip(pts, pts[1:]):                                                     # thin feeler
        rod(m, bd, p0, p1, 1, solid(P, "blue_dark"), extend=0.1)
    tb = m.bone("tentacles", bd, (0, 10, 0))
    for i in range(8):                                                                   # tentacle skirt
        ang = 2 * math.pi * i / 8
        p0 = (3.0 * math.cos(ang), 10.0, 3.0 * math.sin(ang))
        p1 = (5.0 * math.cos(ang), 5.0, 5.0 * math.sin(ang))
        p2 = (4.0 * math.cos(ang + 0.4), 1.0, 4.0 * math.sin(ang + 0.4))
        rod(m, tb, p0, p1, 2, tentf, extend=0.3)
        rod(m, tb, p1, p2, 1, solid(P, "mist"), extend=0.2)
    return m
