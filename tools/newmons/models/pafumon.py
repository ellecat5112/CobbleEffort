"""Pafumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little fluffy white puff of a creature fading to pale blue below, with two big glossy black eyes,
a tiny smile, two long pointed ears tipped brown and a curling wisp on one side. 0.35 blocks tall.

Front is -z, y is up. 16 units tall; Baby I stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a little fluffy white puff fading to pale blue with big glossy black eyes, a tiny smile and long brown-tipped ears"
BASE = {"white": (246, 248, 252), "white_dark": (170, 200, 230), "brown": (150, 90, 50), "black": (16, 16, 22),
        "shine": (250, 250, 255)}
SHINY = {"white": (250, 230, 240), "white_dark": (230, 170, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("pafumon")
    top = m.bone("pafumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 5.0, fur(P, "white", "white_dark", length=1.4, flow=(0, 1)), layers=5, ry=4.4)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.8, 5.6, -4.0), 1.3, solid(P, "black"), layers=2)
        m.box(bd, sx * 1.8 - 0.6, 6.0, -5.35, sx * 1.8 - 0.1, 6.6, -5.25, solid(P, "shine"))
        spike(m, bd, (sx * 2.4, 8.6, 0), (sx * 0.5, 1, 0.2), 1.6, 6.0, solid(P, "white"), tip=0.8)
        spike(m, bd, (sx * 3.6, 12.2, 0.4), (sx * 0.5, 1, 0.2), 0.9, 2.6, solid(P, "brown"), tip=0.8)
    m.box(bd, -0.8, 3.6, -4.95, 0.8, 4.0, -4.8, solid(P, "black"))
    pts = [(-4.6, 6.0, 0), (-6.0, 7.4, 0), (-5.6, 9.0, 0), (-4.6, 8.4, 0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, solid(P, "white_dark"), extend=0.1)
    return m
