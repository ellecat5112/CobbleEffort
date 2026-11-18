"""Mococomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a fluffy golden cloud of smoke with a round face, big blue eyes, a wide open fanged smile, two
orange spots on its brow, curling wisps for a crest and a tail, and two little clawed paws. 0.5 blocks tall.

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
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a fluffy golden cloud of smoke with big blue eyes, a wide fanged smile, curling wisps and little clawed paws"
BASE = {"gold": (250, 220, 70), "gold_dark": (220, 170, 30), "orange": (240, 150, 40), "eye": (60, 120, 220),
        "white": (250, 250, 250), "pupil": (10, 10, 20), "mouth": (230, 110, 40), "tooth": (250, 250, 246),
        "claw": (246, 246, 240)}
SHINY = {"gold": (200, 220, 250), "gold_dark": (140, 160, 220), "orange": (110, 140, 240)}


def P(v):
    return pal(BASE, SHINY, v)


CLOUD = skin(P, "gold", dark="gold_dark", var=0.03)


def build():
    m = Model("mococomon")
    top = m.bone("mococomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 8.0, 0), 6.0, CLOUD, layers=5, ry=5.0, squash=0.85)
    for ang in (30, 150, 210, 330):                                                       # puffs round the cloud
        a = math.radians(ang)
        ball(m, bd, (6.0 * math.cos(a), 7.0 + 2.0 * math.sin(a), 1.0), 2.4, CLOUD, layers=2)
    for sx in (-1, 1):
        ball(m, bd, (sx * 2.2, 9.6, -4.4), 1.3, solid(P, "white"), layers=2)
        m.box(bd, sx * 2.2 - 0.6, 9.0, -5.75, sx * 2.2 + 0.6, 10.4, -5.6, solid(P, "eye"))
        m.box(bd, sx * 2.0 - 0.6, 12.2, -4.2, sx * 2.0 + 0.6, 12.8, -4.0, solid(P, "orange"))
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 3.0, 4.0, -3.0))
        ball(m, ab, (sx * 3.4, 3.0, -4.0), 1.4, CLOUD, layers=2)
        for f in range(2):
            spike(m, ab, (sx * 3.4 + (f - 0.5) * 1.0, 2.0, -5.0), (0, -0.4, -1), 0.8, 1.2, solid(P, "claw"), tip=0.8)
    m.round_box(bd, 0, -4.6, 2.4, 0.6, 5.6, 8.0, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        spike(m, bd, (sx * 1.6, 8.0, -5.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    pts = [(0, 12.0, 0), (0.6, 15.0, 0.4), (2.0, 17.0, 0.6), (3.0, 16.0, 0.6)]
    for p0, p1 in zip(pts, pts[1:]):                                                      # curling wisp crest
        rod(m, bd, p0, p1, 1, CLOUD, extend=0.2, t2=2)
    pts = [(5.0, 7.0, 3.0), (8.0, 8.0, 4.0), (9.6, 10.0, 4.0), (8.6, 11.0, 4.0)]
    for p0, p1 in zip(pts, pts[1:]):                                                      # curling wisp tail
        rod(m, bd, p0, p1, 1, CLOUD, extend=0.2, t2=2)
    return m
