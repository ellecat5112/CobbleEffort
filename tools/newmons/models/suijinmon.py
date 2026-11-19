"""Suijinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the water god machine: a squat red-and-gold armoured robot with a cluster of silver water-cannon
barrels on its shoulders, a round helmeted head with a gold crest, heavy silver piston limbs with clawed hands, a
coiled red tail, and big clawed silver feet. 35 blocks.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 5}
LOOK = "a squat red-and-gold armoured water god robot with shoulder clusters of silver water cannons, silver piston limbs and a coiled tail"
BASE = {"red": (200, 60, 60), "red_dark": (120, 24, 24), "gold": (236, 196, 80), "gold_dark": (150, 110, 30),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 120), "eye": (90, 220, 250), "black": (30, 30, 34)}
SHINY = {"red": (60, 110, 200), "red_dark": (20, 50, 130)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", trim="gold", trim_w=0.3)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("suijinmon")
    top = m.bone("suijinmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 30.0, 0), 11.0, RED, layers=6, ry=10.0)                                  # squat red body
    hd = m.bone("head", bd, (0, 40, -2))
    ball(m, hd, (0, 44.0, -3.0), 4.6, RED, layers=3)
    m.box(hd, -2.4, 44.0, -7.7, 2.4, 45.0, -7.4, solid(P, "eye", glow=True))
    spike(m, hd, (0, 48.0, -3.0), (0, 1, -0.2), 1.6, 5.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for sx in (-1, 1):                                                                   # water-cannon clusters
        for j in range(3):
            c = (sx * (8.0 + j * 2.6), 44.0 + (j % 2) * 3.0, 2.0 - j * 2.0)
            rod(m, bd, (c[0], c[1], c[2] + 4.0), (c[0], c[1] + 2.0, c[2] - 8.0), 2, STEEL, extend=0.3)
            m.round_box(bd, c[0], c[2] - 8.4, 1.0, 0.4, c[1] + 1.0, c[1] + 3.0, solid(P, "black"), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 10.0, 32.0, 0))
        rod(m, ab, (sx * 10.0, 32.0, 0), (sx * 15.0, 22.0, -3.0), 3, STEEL, extend=0.4)
        ball(m, ab, (sx * 15.0, 21.0, -3.0), 3.0, RED, layers=2)
        for f in range(3):
            spike(m, ab, (sx * 15.0 + (f - 1) * 1.4, 18.0, -4.0), (0, -1, -0.4), 1.0, 4.0, STEEL, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 18.0, 0))
        rod(m, lg, (sx * 5.0, 20.0, 0), (sx * 6.0, 6.0, -1.0), 3, STEEL, extend=0.4)
        m.round_box(lg, sx * 6.0, -2.0, 3.6, 5.0, 0.0, 6.0, STEEL, cut=1)
        for f in range(3):
            spike(m, lg, (sx * 6.0 + (f - 1) * 2.0, 1.0, -7.0), (0, -0.2, -1), 1.2, 3.0, STEEL, tip=0.8)
    tl = m.bone("tail", bd, (0, 24, 10))
    pts = [(0, 24.0, 10.0), (4.0, 20.0, 18.0), (8.0, 26.0, 22.0), (6.0, 32.0, 20.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - i, RED, extend=0.4)
    return m
