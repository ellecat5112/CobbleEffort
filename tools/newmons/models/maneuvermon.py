"""Maneuvermon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
flying-fox fighter jet: a sleek white jet-plane beast with a blue-and-orange striped fox head at the nose, a teal
canopy, long swept orange-tipped wings, tailfins, and little clawed legs tucked under. 25 blocks long.

Front is -z, y is up. 24 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, gem, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a sleek white jet-plane beast with a blue-and-orange fox head at the nose, a teal canopy and long swept orange-tipped wings"
BASE = {"white": (240, 242, 248), "white_dark": (170, 176, 196), "blue": (60, 100, 200), "orange": (240, 130, 40),
        "teal": (60, 200, 200), "teal_light": (200, 250, 250), "yellow": (240, 210, 60), "red": (220, 40, 40),
        "eye": (240, 200, 40), "black": (30, 30, 34)}
SHINY = {"white": (60, 60, 76), "white_dark": (24, 24, 34)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "white", "white_dark", trim="blue", trim_w=0.2)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 16.0:
        return tone(p["orange"], face), None
    if abs(abs(x) - 10.0) < 0.6:
        return tone(p["blue"], face), None
    return HULL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("maneuvermon")
    top = m.bone("maneuvermon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(8):
        r = 3.6 * math.sin(math.pi * (0.25 + 0.7 * (i + 0.5) / 8)) + 0.6
        slab_z(m, bd, 0, 12.0, -12.0 + i * 3.4, -8.6 + i * 3.4, r, r * 0.8, HULL)
    m.round_box(bd, 0, -4.0, 2.0, 3.0, 14.4, 16.6, gem(P, "teal", "teal_light", glow=False), cut=1)       # canopy
    hd = m.bone("head", bd, (0, 12, -13))
    m.round_box(hd, 0, -15.0, 2.2, 2.6, 10.6, 14.0, armour(P, "blue", "blue"), cut=1)                      # fox head nose
    spike(m, hd, (0, 12.0, -17.6), (0, -0.1, -1), 1.4, 3.0, solid(P, "orange"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.1, sx * 2.4), 12.6, -16.4, max(sx * 2.1, sx * 2.4), 13.4, -15.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.4, 14.0, -13.0), (sx * 0.4, 1, 0.6), 1.0, 2.6, solid(P, "orange"), tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.4, 12.0, -2.0))
        for j in range(4):
            x0, x1 = sorted((side * 2.4, side * (24.0 - j * 4.0)))
            m.box(wb, x0, 11.6, -6.0 + j * 2.4, x1, 12.6, -3.6 + j * 2.4, wingf, rotation=(0, side * -30, side * 6),
                  pivot=(side * 2.4, 12.0, -2.0))
        x0, x1 = sorted((side * 1.4, side * 6.0))
        m.box(wb, x0, 13.0, 12.0, x1, 13.8, 15.0, wingf, rotation=(0, side * -25, side * -40), pivot=(side * 1.4, 13.0, 12.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 1.6, 9.0, 2.0))
        rod(m, lg, (sx * 1.6, 9.0, 2.0), (sx * 2.0, 4.0, 3.0), 1, HULL, extend=0.3, t2=1)
        for j in range(3):
            spike(m, lg, (sx * 2.0 + (j - 1) * 0.6, 3.6, 2.6), (0, -1, -0.4), 0.8, 2.0, solid(P, "yellow"), tip=0.8)
    return m
