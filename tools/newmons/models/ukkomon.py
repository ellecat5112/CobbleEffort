"""Ukkomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little white ancient fairy shaped like a plump ghost: big green eyes, a tiny open mouth, a violet
orb on its chest, three stubby horn-points tipped red and two little arms with black-clawed hands. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, gem, plane, skin, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a little white ghost-shaped fairy with big green eyes, a violet chest orb and red-tipped horn points"
BASE = {"white": (250, 250, 252), "white_dark": (200, 200, 214), "eye": (110, 200, 70), "pupil": (20, 30, 10),
        "red": (220, 50, 50), "orb": (180, 140, 240), "orb_light": (240, 220, 255), "black": (30, 30, 34),
        "mouth": (220, 120, 140)}
SHINY = {"white": (250, 230, 200), "white_dark": (210, 180, 140), "orb": (240, 140, 120), "orb_light": (255, 220, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            c = eye(p, a - sx * 2.4, b - 13.4, 1.4, "eye")
            if c is not None:
                return c, None
        if math.hypot(a, b - 10.6) < 0.7:
            return p["mouth"], None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ukkomon")
    top = m.bone("ukkomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 12.0, 0), 6.0, bodyf, layers=5, squash=0.9)
    spike(m, bd, (0, 6.4, 0), (0, -1, 0), 4.0, 5.0, bodyf, tip=0.8)                    # tapering ghost tail
    ball(m, bd, (0, 8.6, -4.8), 1.4, gem(P, "orb", "orb_light"), layers=2)
    for d in ((-1, 0.6), (1, 0.6), (0.3, 1)):                                         # horn points
        base_pt = (d[0] * 4.0, 15.0 + d[1] * 1.6, 0)
        spike(m, bd, base_pt, (d[0], d[1] + 0.4, 0), 1.8, 4.6, skin(P, "white", dark="white_dark"), tip=0.8)
        tip = (base_pt[0] + d[0] * 3.4, base_pt[1] + (d[1] + 0.4) * 3.4, 0)
        ball(m, bd, tip, 0.9, solid(P, "red"), layers=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 10.0, 0))
        rod(m, ab, (sx * 5.0, 10.0, 0), (sx * 9.0, 9.0, -1.0), 2, skin(P, "white", dark="white_dark"), extend=0.4)
        for f in range(3):
            spike(m, ab, (sx * 9.4, 9.0, -1.0), (sx, (f - 1) * 0.6, -0.3), 0.8, 1.6, solid(P, "black"), tip=0.8)
    return m
