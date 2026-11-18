"""Oleamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a carnivorous lily: a tall dark stem-body bending forward, crowned with a great drooping dark-red lily
whose petals curl back over a hidden face, long trailing leaves edged with green fringe, and a ring of red lily
petals at its base like a skirt. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = "a tall carnivorous lily: a dark bending stem-body crowned by a great drooping dark-red lily, long fringed leaves and a skirt of red petals"
BASE = {"stem": (50, 46, 52), "stem_dark": (20, 18, 22), "petal": (120, 40, 50), "petal_dark": (60, 14, 20),
        "green": (70, 120, 60), "fringe": (110, 170, 90), "white": (230, 226, 210)}
SHINY = {"petal": (220, 220, 236), "petal_dark": (150, 150, 170), "stem": (60, 90, 60)}


def P(v):
    return pal(BASE, SHINY, v)


STEM = skin(P, "stem", dark="stem_dark")
PETAL = skin(P, "petal", dark="petal_dark")


def build():
    m = Model("oleamon")
    top = m.bone("oleamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(8):                                                                   # skirt of petals
        ang = 2 * math.pi * i / 8
        m.box(bd, -2.0, 0.0, 0, 2.0, 10.0, 0.4, PETAL, rotation=(-40, -math.degrees(ang), 0),
              pivot=(0, 10.0, 0))
    pts = [(0, 8.0, 0), (0, 22.0, 1.0), (0, 36.0, 0.0), (0, 46.0, -3.0), (0, 52.0, -7.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                     # bending stem-body
        rod(m, bd, p0, p1, 6 - j, STEM, extend=0.6)
    hd = m.bone("head", bd, pts[-1])
    h = pts[-1]
    ball(m, hd, (h[0], h[1] + 1.0, h[2]), 4.0, PETAL, layers=3)
    for i in range(6):                                                                   # great drooping lily petals
        ang = 360.0 * i / 6
        m.box(hd, h[0] - 3.4, h[1] - 16.0, h[2] - 0.4, h[0] + 3.4, h[1] + 2.0, h[2] + 0.4, PETAL,
              rotation=(28, ang, 0), pivot=(h[0], h[1] + 2.0, h[2]))
        m.box(hd, h[0] - 2.0, h[1] - 18.0, h[2] - 0.3, h[0] + 2.0, h[1] - 14.0, h[2] + 0.3, PETAL,
              rotation=(60, ang, 0), pivot=(h[0], h[1] + 2.0, h[2]))
    for j in range(3):                                                                   # stamens
        rod(m, hd, (h[0], h[1], h[2]), (h[0] + (j - 1) * 1.6, h[1] - 8.0, h[2] - 2.0), 1, solid(P, "white"), extend=0.1)
    for sx in (-1, 1):                                                                   # long fringed leaves
        lb = m.bone("arm_left" if sx > 0 else "arm_right", bd, (0, 32.0, 0))
        x0, x1 = sorted((0, sx * 16.0))
        m.box(lb, x0, 30.0, -0.2, x1, 34.0, 0.2, skin(P, "green", dark="stem_dark"), rotation=(0, 0, -sx * 30),
              pivot=(0, 32.0, 0))
        for j in range(5):
            spike(m, lb, (sx * (4.0 + j * 2.4), 31.0 - j * 1.4, 0), (sx * 0.2, -1, 0), 1.0, 3.0,
                  strands(P, "fringe", "green"), tip=0.8)
    return m
