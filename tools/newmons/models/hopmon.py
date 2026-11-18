"""Hopmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby
II blue teardrop blob with a tall yellow-tipped curling tuft, a yellow diamond on its brow, a yellow belly band, small
fins at its sides, big round eyes and a tiny fanged frown. Half a block tall.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a blue teardrop blob with a tall yellow-tipped tuft, a yellow brow diamond, side fins and a tiny fanged frown"
BASE = {"blue": (80, 130, 230), "blue_dark": (40, 80, 170), "yellow": (250, 220, 60), "eye": (20, 20, 24),
        "shine": (250, 250, 250), "tooth": (250, 250, 250), "mouth": (40, 40, 60)}
SHINY = {"blue": (230, 110, 140), "blue_dark": (170, 60, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 6.6)
            if d < 0.3:
                return tone(p["shine"], face), None
            if d < 0.9:
                return tone(p["eye"], face), None
        if abs(x) < 1.0 - abs(y - 10.0) * 0.6:
            return tone(p["yellow"], face), None
        if abs(y - 4.6) < 0.25 and abs(x) < 1.4:
            return tone(p["mouth"], face), None
    if y < 2.6:
        return tone(p["yellow"], face), None
    return skin(P, "blue", dark="blue_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hopmon")
    top = m.bone("hopmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 6.0, 0), 5.6, bodyf, layers=4)
    hd = m.bone("head", bd, (0, 11, 0))
    pts = [(0, 10.6, 0.4), (0.4, 14.0, 1.0), (1.4, 17.0, 1.6)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 2 - j, skin(P, "blue", dark="blue_dark") if j == 0 else solid(P, "yellow"), extend=0.3, t2=3 - j)
    for sx in (-1, 1):
        spike(m, bd, (sx * 5.0, 6.0, 0), (sx, 0.4, 0.3), 1.6, 3.0, skin(P, "blue", dark="blue_dark"), tip=0.8)
    return m
