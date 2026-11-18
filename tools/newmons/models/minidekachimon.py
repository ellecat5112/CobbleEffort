"""Minidekachimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a glossy red little dragon with a huge round head that is mostly a wide jagged grin,
one big blue eye bulging on top, small pale-blue tipped paws and feet, and a long curling tail. 1 block tall.

Front is -z, y is up. 20 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 1.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a glossy red little dragon with a huge head that is mostly a wide jagged grin, one big blue eye on top and a curling tail"
BASE = {"red": (220, 30, 40), "red_dark": (130, 10, 20), "red_light": (250, 120, 120), "mouth": (240, 90, 120),
        "mouth_dark": (120, 20, 40), "tooth": (250, 250, 246), "white": (250, 250, 250), "eye": (60, 120, 220),
        "pupil": (10, 10, 20), "tip": (190, 210, 230)}
SHINY = {"red": (60, 170, 90), "red_dark": (20, 90, 40), "red_light": (150, 230, 170)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark", light="red_light")


def build():
    m = Model("minidekachimon")
    top = m.bone("minidekachimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 5.0, 0.6), 2.6, RED, layers=3, ry=2.8)
    hd = m.bone("head", bd, (0, 8, 0))
    ball(m, hd, (0, 12.6, -0.4), 5.4, RED, layers=5, ry=4.6, squash=0.9)
    m.round_box(hd, 0, -4.4, 3.8, 0.8, 9.0, 13.4, solid(P, "mouth"), cut=1)              # wide jagged grin
    for j in range(5):
        spike(m, hd, (-3.0 + j * 1.5, 13.4, -5.0), (0, -1, 0), 1.2, 1.6, solid(P, "tooth"), tip=0.8)
        spike(m, hd, (-2.4 + j * 1.2, 9.0, -5.0), (0, 1, 0), 1.0, 1.2, solid(P, "tooth"), tip=0.8)
    ball(m, hd, (2.6, 17.4, -1.0), 2.2, solid(P, "white"), layers=3)                     # one big eye on top
    m.box(hd, 1.8, 16.8, -3.25, 3.4, 18.4, -3.1, solid(P, "eye"))
    m.box(hd, 2.3, 17.2, -3.3, 2.9, 18.0, -3.25, solid(P, "pupil"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.4, 7.0, -0.6))
        rod(m, ab, (sx * 2.4, 7.0, -0.6), (sx * 5.0, 9.0, -1.4), 1, RED, extend=0.3, t2=1)
        ball(m, ab, (sx * 5.4, 9.4, -1.6), 0.9, solid(P, "tip"), layers=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 3.0, 0.6))
        rod(m, lg, (sx * 1.6, 3.6, 0.6), (sx * 2.0, 0.8, 0.0), 2, RED, extend=0.3)
        m.round_box(lg, sx * 2.0, -0.6, 1.0, 1.4, 0.0, 1.0, solid(P, "tip"), cut=0)
    tb = m.bone("tail", bd, (0, 4, 3))
    pts = [(0, 4.0, 3.0), (2.0, 3.0, 7.0), (5.0, 4.0, 9.0), (8.0, 6.0, 8.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, RED, extend=0.3, t2=1)
    return m
