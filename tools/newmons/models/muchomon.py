"""Muchomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a plump red bird with a yellow belly flamed red, a big green-and-yellow hooked beak, round yellow
eyes, a shaggy crest, wings ending in grey claws, and stout grey taloned feet. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a plump red bird with a yellow belly flamed red, a big green-and-yellow hooked beak, round yellow eyes and grey talons"
BASE = {"red": (220, 50, 40), "red_dark": (140, 20, 14), "yellow": (250, 220, 60), "green": (90, 170, 60),
        "beak_y": (240, 200, 40), "grey": (110, 110, 124), "eye": (240, 220, 40), "pupil": (20, 20, 20)}
SHINY = {"red": (60, 140, 220), "red_dark": (20, 70, 150)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "red", "red_dark")


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(y - 10.0 - 1.6 * abs(math.sin(x * 0.9))) % 3.0 < 0.6:
        return tone(p["red"], face), None
    return tone(p["yellow"], face), None


def build():
    m = Model("muchomon")
    top = m.bone("muchomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 13.0, 0.6), 7.0, FEATH, layers=6, ry=8.0, squash=0.9)
    ball(m, bd, (0, 11.0, -3.4), 5.0, bellyf, layers=4, ry=6.0, squash=0.5)
    hd = m.bone("head", bd, (0, 20, -1))
    ball(m, hd, (0, 22.0, -1.6), 4.0, FEATH, layers=4, ry=3.6)
    m.round_box(hd, 0, -6.6, 2.2, 2.4, 21.6, 24.0, solid(P, "beak_y"), cut=1)            # hooked beak
    m.round_box(hd, 0, -6.0, 2.0, 2.0, 19.6, 21.6, solid(P, "green"), cut=1)
    spike(m, hd, (0, 22.4, -9.0), (0, -1, -0.3), 1.4, 2.4, solid(P, "beak_y"), tip=0.8)
    for sx in (-1, 1):
        ball(m, hd, (sx * 2.8, 23.6, -3.6), 1.0, solid(P, "eye"), layers=2)
        m.box(hd, sx * 2.8 - 0.3, 23.4, -4.65, sx * 2.8 + 0.3, 24.0, -4.6, solid(P, "pupil"))
        wb = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 6.0, 15.0, 0))
        x0, x1 = sorted((sx * 6.0, sx * 11.0))
        m.box(wb, x0, 8.0, -1.0, x1, 16.0, 1.0, FEATH, rotation=(0, 0, sx * 20), pivot=(sx * 6.0, 15.0, 0))
        for f in range(2):
            spike(m, wb, (sx * 10.0, 8.0, -0.4 + f), (sx * 0.4, -1, -0.3), 1.0, 2.6, solid(P, "grey"), tip=0.8)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 3.0, 6.0, 0))
        rod(m, lg, (sx * 3.0, 6.0, 0), (sx * 3.2, 1.0, -0.6), 2, solid(P, "grey"), extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 3.2 + (f - 1) * 1.0, 0.6, -1.0), (0, -0.3, -1), 1.0, 2.6, solid(P, "grey"), tip=0.8)
    for i in range(5):                                                                   # shaggy crest
        spike(m, hd, ((i - 2) * 0.8, 25.0, 0.0), ((i - 2) * 0.3, 1, 0.6), 1.2, 3.0, FEATH, tip=0.8)
    return m
