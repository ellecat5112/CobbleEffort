"""Yolkmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little egg yolk with dot eyes and a cat mouth, peeking out from under a cracked shell cap patterned
with green rings, sitting in a puddle of egg white. 0.35 blocks.

Front is -z, y is up. Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 2.0)
KIND = "biped"
K = 4
LOOK = "a little egg yolk with dot eyes and a cat mouth under a cracked green-ringed shell cap, sitting in egg white"
BASE = {"yolk": (250, 200, 50), "yolk_dark": (220, 150, 20), "white": (250, 250, 246), "shell": (240, 240, 230),
        "ring": (60, 150, 90), "eye": (30, 24, 20)}
SHINY = {"yolk": (250, 140, 160), "yolk_dark": (210, 90, 120), "ring": (90, 110, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def yolkf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 1.6, b - 5.6) < 0.6:
                return p["eye"], None
        if abs(b - 4.2) < 0.25 and abs(a) < 1.0:
            return p["eye"], None
    return skin(P, "yolk", dark="yolk_dark")(x, y, z, face, variant, box=box, **k)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = math.hypot(x - 2.0, z - 1.0)
    if face != "down" and abs(d % 2.4 - 1.2) < 0.35 and d < 4.0:
        return tone(p["ring"], face), None
    return tone(p["shell"], face), None


def build():
    m = Model("yolkmon")
    top = m.bone("yolkmon", None, (0, 0, 0))
    m.round_box(top, 0, 0, 9.0, 8.0, 0.0, 1.0, solid(P, "white"), cut=3)                   # egg white puddle
    bd = m.bone("body", top, (0, 1, 0))
    ball(m, bd, (0, 4.6, 0), 4.0, yolkf, layers=4, squash=0.8)
    ball(m, bd, (0, 9.0, 0.6), 4.8, shellf, layers=3, squash=0.7)                         # shell cap
    for j in range(8):
        ang = j * 2 * math.pi / 8
        m.box(bd, 4.4 * math.cos(ang) - 0.6, 7.0 - (j % 2) * 0.8, 0.6 + 4.4 * math.sin(ang) - 0.6,
              4.4 * math.cos(ang) + 0.6, 8.0, 0.6 + 4.4 * math.sin(ang) + 0.6, shellf)
    return m
