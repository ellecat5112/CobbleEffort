"""Fujamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little horned fish. A light-blue fish with dark blue stripes, a white belly, a single short horn on its snout and a
grey rounded head-crest, a red eye, a toothy open grin, flowing lavender fins and a long arched tail ringed with a
black band before its lavender fluke. Child stage, 1 block tall.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import local, scales, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = ("a light-blue striped fish with a white belly, a snout horn, a red eye, a toothy grin, flowing lavender fins and "
        "a long arched black-banded tail")
BASE = {"blue": (120, 210, 240), "blue_dark": (40, 110, 170), "stripe": (40, 80, 150), "white": (246, 250, 250),
        "grey": (150, 170, 190), "fin": (200, 180, 240), "fin_dark": (140, 110, 200), "eye": (210, 30, 40),
        "pupil": (16, 16, 20), "mouth": (110, 30, 50), "tooth": (250, 250, 250), "black": (34, 32, 38)}
SHINY = {"blue": (250, 200, 120), "blue_dark": (200, 130, 50), "stripe": (180, 80, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SCALE_S = scales(P, "blue", "blue_dark", size=1.0)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 6.4 or face == "down":
        return tone(p["white"], face), None
    if abs((z * 0.5 + y * 0.2) % 3.0 - 1.5) < 0.35 and face != "north":
        return tone(p["stripe"], face), None
    return SCALE_S(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 4.6 < y < 7.4 and abs(x) < 3.4:
        if (y > 6.8 or y < 5.2) and ((x + 4.0) % 1.0) < 0.5:
            return tone(p["tooth"], face), None
        return tone(p["mouth"], face), None
    if face in ("east", "west") and math.hypot(z + 5.0, y - 9.0) < 1.0:
        return tone(p["pupil"] if math.hypot(z + 5.0, y - 9.0) < 0.4 else p["eye"], face), None
    return bodyf(x, y, z, face, variant, box=box, **k)


def finf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["fin_dark"] if (u + v * 0.5) % 1.6 < 0.4 else p["fin"], face), None


def build():
    m = Model("fujamon")
    top = m.bone("fujamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 1.0, 4.4, 6.0, 3.0, 13.0, bodyf, cut=2)
    hd = m.bone("head", bd, (0, 8, -5))
    m.round_box(hd, 0, -6.0, 3.8, 3.0, 4.0, 12.0, headf, cut=2)
    m.round_box(hd, 0, -6.4, 2.6, 2.0, 10.0, 12.6, solid(P, "grey"), cut=1)           # grey head-crest
    spike(m, hd, (0, 11.6, -8.0), (0, 0.6, -1), 1.4, 2.6, solid(P, "grey"), tip=0.2)  # snout horn
    for j in range(5):                                                                  # flowing dorsal fins
        m.box(bd, -0.2, 12.0, -2.0 + j * 1.6, 0.2, 17.0 - j * 0.6, 0.0 + j * 1.6, finf,
              rotation=(-30, (j - 2) * 10, 0), pivot=(0, 12.0, -2.0 + j * 1.6))
    for sx in (-1, 1):                                                                  # pectoral fins
        x0, x1 = sorted((sx * 4.0, sx * 9.0))
        m.box(bd, x0, 3.0, -2.0, x1, 3.4, 4.0, finf, rotation=(0, sx * 20, sx * -25), pivot=(sx * 4.0, 3.4, 0))
    tb = m.bone("tail", bd, (0, 8, 6))
    pts = [(0, 8.0, 6.0), (0, 11.0, 11.0), (0, 14.0, 15.0), (0, 15.0, 20.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 2, bodyf if j != 1 else solid(P, "black"), extend=0.4, t2=max(1, 3 - j))
    for sy in (-1, 1):
        m.box(tb, -3.0, 15.0, 20.0, 3.0, 15.4, 25.0, finf, rotation=(0, sy * 25, 0), pivot=(0, 15.0, 20.0))
    return m
