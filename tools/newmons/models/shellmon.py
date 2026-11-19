"""Shellmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a hermit crab-slug: a squat pink body with blue spots and stubby squelching legs, a gaping drooling
mouth, one blue eye, a wild mop of green-and-yellow tendril hair, living in a huge spiked blue-grey shell. 15 blocks.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, skin, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a squat pink spotted slug-crab with a gaping drooling mouth, one blue eye and a mop of green tendril hair in a huge spiked blue shell"
BASE = {"pink": (240, 110, 170), "pink_dark": (180, 50, 110), "spot": (120, 200, 240), "shell": (150, 160, 200),
        "shell_dark": (80, 90, 130), "green": (150, 220, 60), "green_dark": (80, 140, 20), "eye": (60, 120, 220),
        "black": (30, 20, 30), "mouth": (120, 20, 50), "white": (255, 255, 255)}
SHINY = {"pink": (250, 200, 90), "pink_dark": (200, 140, 30), "shell": (170, 120, 110), "shell_dark": (100, 60, 50)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if math.sin(x * 1.6) * math.sin(y * 1.3 + z * 0.7) > 0.88:
        return tone(p["spot"], face), None
    return skin(P, "pink", dark="pink_dark", var=0.04)(x, y, z, face, variant, box=box, **k)


SHELL = armour(P, "shell", "shell_dark")


def build():
    m = Model("shellmon")
    top = m.bone("shellmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 16.0, 8.0), 11.0, SHELL, layers=6, ry=11.0)                              # spiked shell
    for i in range(12):
        ang = 2 * math.pi * i / 12
        for yy in (12.0, 20.0):
            spike(m, bd, (10.0 * math.cos(ang), yy, 8.0 + 10.0 * math.sin(ang)), (math.cos(ang), 0.4, math.sin(ang)),
                  2.0, 5.0, SHELL, tip=0.8)
    hd = m.bone("head", bd, (0, 12, -4))
    ball(m, hd, (0, 12.0, -6.0), 6.4, bodyf, layers=5, ry=6.0)
    m.box(hd, -4.0, 6.0, -12.6, 4.0, 11.0, -10.0, solid(P, "mouth"))                         # gaping mouth
    for j in range(4):
        spike(m, hd, (-3.0 + j * 2.0, 11.0, -12.0), (0, -1, 0), 0.9, 2.0, bodyf, tip=0.8)
    m.round_box(hd, -1.6, -11.4, 1.4, 0.8, 14.0, 17.0, solid(P, "white"), cut=0)
    m.box(hd, -2.0, 14.6, -12.3, -1.0, 16.0, -12.1, solid(P, "eye"))
    for j in range(10):                                                                  # mop of tendril hair
        ang = math.radians(-100 + j * 22)
        spike(m, hd, (4.0 * math.sin(ang), 17.0, -6.0 + math.cos(ang)), (math.sin(ang), 0.8, -0.2), 1.2, 5.0,
              strands(P, "green", "green_dark"), tip=0.8)
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        zz = -8.0 if "front" in nm else -2.0
        lg = m.bone(nm, top, (sx * 6.0, 6.0, zz))
        rod(m, lg, (sx * 5.0, 7.0, zz), (sx * 10.0, 1.0, zz - 2.0), 3, bodyf, extend=0.6)
        ball(m, lg, (sx * 10.6, 1.4, zz - 2.4), 1.6, bodyf, layers=1)
    return m
