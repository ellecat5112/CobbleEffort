"""Turbomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a racing beast built for speed: a sleek blue swept-back body and long pointed snout with gold eyes,
blue fins tipped orange along its back, white fur at its chest, and four chunky jet-engine legs ringed blue with an
orange zigzag band and white claws, flame-streaked tail fins behind. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import fur, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "a sleek blue swept-back racing beast with a pointed snout, orange-tipped fins and four jet-engine legs with orange zigzag bands"
BASE = {"blue": (40, 100, 200), "blue_dark": (16, 44, 110), "orange": (250, 130, 40), "white": (246, 240, 230),
        "white_dark": (200, 190, 170), "navy": (24, 30, 70), "eye": (250, 210, 50), "claw": (250, 250, 250)}
SHINY = {"blue": (200, 50, 60), "blue_dark": (110, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = skin(P, "blue", dark="blue_dark")


def enginef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None:
        t = (z - box.lo[2]) / max(box.size[2], 1e-6)
        zz = 0.5 + 0.12 * math.sin((x + y) * 1.6)
        if abs(t - zz) < 0.1:
            return tone(p["orange"], face), None
        if t < 0.3 or t > 0.8:
            return tone(p["navy"], face), None
    return metal(P, "blue", dark="blue_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("turbomon")
    top = m.bone("turbomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(6):
        z0 = -10.0 + i * 3.4
        r = 4.0 - abs(i - 1.5) * 0.4
        slab_z(m, bd, 0, 11.0, z0, z0 + 3.6, r * 1.1, r, BLUE)
    hd = m.bone("head", bd, (0, 11, -10))
    spike(m, hd, (0, 11.0, -10.0), (0, -0.1, -1), 4.4, 9.0, BLUE, tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 2.6), 12.0, -14.0, max(sx * 1.2, sx * 2.6), 12.8, -12.0, solid(P, "eye", glow=True))
    ball(m, bd, (0, 9.0, -8.0), 3.0, fur(P, "white", "white_dark"), layers=2)
    for j in range(5):                                                                 # back fins
        spike(m, bd, (0, 14.0, -6.0 + j * 3.4), (0, 0.8, 1), 1.6, 6.0, BLUE, tip=0.8)
        spike(m, bd, (0, 17.0, -2.0 + j * 3.4), (0, 0.4, 1), 0.9, 2.0, solid(P, "orange"), tip=0.8)
    for sx, nm, z in ((1, "leg_front_left", -6.0), (-1, "leg_front_right", -6.0), (1, "leg_back_left", 6.0),
                      (-1, "leg_back_right", 6.0)):
        lg = m.bone(nm, bd, (sx * 4.6, 9.0, z))
        m.box(lg, sx * 6.0 - 2.4, 2.0, z - 4.0, sx * 6.0 + 2.4, 7.0, z + 4.0, enginef)
        for j in range(3):
            spike(m, lg, (sx * 6.0 + (j - 1) * 1.4, 2.0, z - 4.0), (0, -0.4, -1), 0.9, 2.0, solid(P, "claw"), tip=0.8)
    for sy in (-1, 1):                                                                 # tail fins
        spike(m, bd, (0, 11.0 + sy * 1.4, 10.0), (0, sy * 0.4, 1), 1.6, 7.0, solid(P, "orange"), tip=0.8)
    return m
