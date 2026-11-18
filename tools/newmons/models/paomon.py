"""Paomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a soft white bun of a creature with a cracked-open top, two dot eyes, a little smile and two floppy
pink ears. 0.35 blocks tall.

Front is -z, y is up. 14 units tall; Baby I stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a soft white bun with a cracked top, dot eyes, a little smile and floppy pink ears"
BASE = {"white": (248, 246, 242), "white_dark": (200, 196, 190), "pink": (240, 110, 150), "black": (24, 24, 26)}
SHINY = {"white": (250, 236, 200), "white_dark": (210, 190, 140), "pink": (120, 170, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("paomon")
    top = m.bone("paomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 6.0, skin(P, "white", dark="white_dark", var=0.02), layers=5, ry=4.6, squash=0.85)
    for j in range(4):                                                                   # cracked top
        m.box(bd, -2.0 + j * 1.0, 9.0 + (j % 2) * 0.4, -3.6, -1.4 + j * 1.0, 9.4 + (j % 2) * 0.4, -3.4, solid(P, "black"))
    for sx in (-1, 1):
        ball(m, bd, (sx * 2.4, 5.4, -4.9), 0.5, solid(P, "black"), layers=1)
        rod(m, bd, (sx * 5.4, 6.0, 0), (sx * 7.4, 2.6, -0.6), 2, solid(P, "pink"), extend=0.3, t2=3)
    m.box(bd, -0.8, 4.0, -5.2, 0.8, 4.3, -5.05, solid(P, "black"))
    return m
