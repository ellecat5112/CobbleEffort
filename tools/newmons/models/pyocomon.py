"""Pyocomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a pale-pink onion bulb with big green eyes and a little smile, a fringe of root nubs below, and a
deep-blue flower of six ragged petals on top with yellow-and-red curling stamens. 0.5 blocks.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 3
LOOK = "a pale-pink onion bulb with big green eyes, root nubs and a deep-blue six-petal flower with curling yellow stamens"
BASE = {"pink": (250, 220, 230), "pink_dark": (220, 170, 190), "eye": (60, 170, 90), "pupil": (20, 30, 20),
        "white": (255, 255, 255), "blue": (40, 80, 180), "blue_dark": (20, 40, 110), "yellow": (250, 210, 50),
        "red": (220, 60, 40), "mouth": (180, 60, 80)}
SHINY = {"blue": (200, 50, 120), "blue_dark": (120, 20, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def bulbf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.6, (y - 5.2) * 0.8)
            if d < 0.45:
                return tone(p["pupil"], face), None
            if d < 0.9:
                return tone(p["eye"], face), None
        if abs(y - 3.6 - 0.15 * x * x) < 0.15 and abs(x) < 1.0:
            return tone(p["mouth"], face), None
    return skin(P, "pink", dark="pink_dark", var=0.02)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pyocomon")
    top = m.bone("pyocomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 4.6, 0), 4.0, bulbf, layers=4, ry=3.8)
    spike(m, bd, (0, 8.0, 0), (0, 1, 0), 2.0, 2.0, bulbf, tip=0.8)
    for i in range(6):
        ang = 2 * math.pi * i / 6
        spike(m, bd, (2.4 * math.cos(ang), 1.2, 2.4 * math.sin(ang)), (0.3 * math.cos(ang), -1, 0.3 * math.sin(ang)),
              1.0, 1.4, bulbf, tip=0.8)
    fl = m.bone("flower", bd, (0, 10, 0))
    for i in range(6):                                                                   # six ragged blue petals
        ang = 2 * math.pi * i / 6
        p0 = (0.8 * math.cos(ang), 10.0, 0.8 * math.sin(ang))
        x0, x1 = sorted((p0[0], p0[0] + 5.0 * math.cos(ang)))
        spike(m, fl, p0, (math.cos(ang), -0.2, math.sin(ang)), 2.2, 6.0, skin(P, "blue", dark="blue_dark", var=0.03),
              tip=0.8)
    for j in range(5):                                                                   # curling stamens
        ang = 2 * math.pi * j / 5
        pts = [(0, 10.0, 0), (1.4 * math.cos(ang), 13.0, 1.4 * math.sin(ang)), (2.4 * math.cos(ang), 14.6, 2.4 * math.sin(ang))]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, fl, p0, p1, 1, solid(P, "yellow"), extend=0.2)
        m.box(fl, pts[-1][0] - 0.5, 14.6, pts[-1][2] - 0.5, pts[-1][0] + 0.5, 15.6, pts[-1][2] + 0.5,
              solid(P, "red" if j % 2 else "yellow"))
    return m
