"""Parasimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the parasite from the dark area: a long-legged spider of pink jointed limbs around a green body
with a gaping fanged mouth, a cluster of red eyes and a trailing green tendril it uses to take over its hosts. 35
blocks wide.

Front is -z, y is up. 30 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a long-legged spider of pink jointed limbs around a green body with a gaping fanged mouth, red eyes and a trailing tendril"
BASE = {"pink": (220, 120, 190), "pink_dark": (150, 60, 130), "green": (90, 170, 80), "green_dark": (40, 100, 30),
        "red": (230, 40, 40), "mouth": (160, 30, 70), "tooth": (250, 250, 240)}
SHINY = {"pink": (130, 170, 230), "pink_dark": (60, 100, 170), "green": (200, 160, 70), "green_dark": (140, 100, 30)}


def P(v):
    return pal(BASE, SHINY, v)


LEG = skin(P, "pink", dark="pink_dark")


def build():
    m = Model("parasimon")
    top = m.bone("parasimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 16.0, 0), 5.0, skin(P, "green", dark="green_dark"), layers=4, ry=4.0)
    m.round_box(bd, 0, -4.6, 2.6, 0.6, 13.6, 16.6, solid(P, "mouth"), cut=0)
    for j in range(5):
        spike(m, bd, (-2.0 + j * 1.0, 16.6, -5.0), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
    for i in range(5):
        ang = math.radians(-50 + i * 25)
        ball(m, bd, (3.0 * math.sin(ang), 19.0 + (i % 2) * 0.8, -3.8), 0.6, solid(P, "red", glow=True), layers=1)
    for i in range(8):                                                                   # long jointed legs
        ang = math.radians(20 + (i % 4) * 30) * (1 if i < 4 else -1)
        sx = 1 if i < 4 else -1
        lb = m.bone("leg_%d" % i, bd, (sx * 3.0, 16.0, 0))
        a2 = math.radians(-60 + (i % 4) * 40)
        knee = (sx * 14.0 * math.cos(a2 * 0.3), 28.0, 10.0 * math.sin(a2))
        foot = (sx * 22.0 * math.cos(a2 * 0.3), 0.0, 16.0 * math.sin(a2))
        rod(m, lb, (sx * 3.0, 16.0, 0), knee, 2, LEG, extend=0.4)
        ball(m, lb, knee, 1.4, LEG, layers=2)
        rod(m, lb, knee, foot, 2, LEG, extend=0.4)
    pts = [(2.0, 13.0, 4.0), (5.0, 9.0, 8.0), (8.0, 8.0, 12.0)]
    for p0, p1 in zip(pts, pts[1:]):                                                     # green tendril
        rod(m, bd, p0, p1, 1, skin(P, "green", dark="green_dark"), extend=0.2)
    return m
