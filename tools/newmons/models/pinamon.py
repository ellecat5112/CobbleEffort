"""Pinamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a fluffy orange owl chick with a white face, huge round brown eyes, a little hooked beak, two long
feather-tufts with pink fluffy tips, and small dark wings. 0.5 blocks tall.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a fluffy orange owl chick with a white face, huge round brown eyes, a little hooked beak and long pink-tipped feather tufts"
BASE = {"orange": (230, 130, 60), "orange_dark": (170, 80, 30), "white": (250, 246, 240), "brown": (110, 70, 40),
        "black": (20, 16, 16), "beak": (90, 80, 70), "pink": (240, 150, 170), "wing": (70, 60, 60)}
SHINY = {"orange": (150, 150, 200), "orange_dark": (90, 90, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("pinamon")
    top = m.bone("pinamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 6.0, 0), 5.0, feathers(P, "orange", "orange_dark"), layers=5, ry=4.6)
    ball(m, bd, (0, 6.0, -2.6), 3.6, solid(P, "white"), layers=3, ry=3.2, squash=0.5)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.6, 6.4, -4.2), 1.4, solid(P, "brown"), layers=2, squash=0.4)
        m.box(bd, sx * 1.6 - 0.5, 6.0, -4.85, sx * 1.6 + 0.5, 7.0, -4.75, solid(P, "black"))
        pts = [(sx * 1.6, 10.0, 0), (sx * 4.0, 13.0, 0.4), (sx * 5.6, 14.6, 0.6)]
        for p0, p1 in zip(pts, pts[1:]):                                                 # feather tufts
            rod(m, bd, p0, p1, 1, solid(P, "orange"), extend=0.1)
        spike(m, bd, pts[-1], (sx * 0.5, 0.6, 0), 1.2, 1.6, solid(P, "pink"), tip=0.8)
        x0, x1 = sorted((sx * 4.0, sx * 7.0))
        m.box(bd, x0, 3.0, 1.0, x1, 7.0, 1.4, solid(P, "wing"), rotation=(0, 0, sx * 20), pivot=(sx * 4.0, 5.0, 1.2))
    spike(m, bd, (0, 5.0, -4.6), (0, -0.6, -1), 0.9, 1.6, solid(P, "beak"), tip=0.8)
    return m
