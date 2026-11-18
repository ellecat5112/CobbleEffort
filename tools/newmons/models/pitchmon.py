"""Pitchmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a pale-blue tadpole-like blob with two long ears, a big red eye on one side, a little beak, small
spines along its back and a curling tail. 0.35 blocks tall.

Front is -z, y is up. 16 units tall; Baby I stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a pale-blue tadpole-like blob with two long ears, a big red eye, a little beak, small back spines and a curling tail"
BASE = {"blue": (200, 230, 250), "blue_dark": (130, 180, 220), "eye": (200, 40, 40), "white": (250, 250, 255),
        "black": (24, 24, 30)}
SHINY = {"blue": (250, 220, 230), "blue_dark": (220, 160, 180)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "blue", dark="blue_dark", var=0.02)


def build():
    m = Model("pitchmon")
    top = m.bone("pitchmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 6.0, 0), 4.6, BODY, layers=4, ry=4.2)
    for sx in (-1, 1):
        ball(m, bd, (sx * 2.0, 7.0, -3.8), 1.2, solid(P, "white"), layers=2, squash=0.5)
        m.box(bd, sx * 2.0 - 0.5, 6.6, -4.45, sx * 2.0 + 0.5, 7.6, -4.35, solid(P, "eye"))
        spike(m, bd, (sx * 1.6, 9.6, 0.4), (sx * 0.3, 1, 0.2), 1.6, 6.0, BODY, tip=0.8)
    spike(m, bd, (0, 5.0, -4.4), (0, -0.4, -1), 1.0, 1.6, solid(P, "black"), tip=0.8)
    for j in range(3):
        spike(m, bd, (0, 8.0 - j * 1.6, 3.6 + j * 0.4), (0, 0.4, 1), 0.8, 1.4, BODY, tip=0.8)
    pts = [(0, 3.0, 3.0), (1.0, 1.0, 6.0), (2.6, 1.6, 8.0), (3.0, 3.4, 8.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, BODY, extend=0.2, t2=2)
    return m
