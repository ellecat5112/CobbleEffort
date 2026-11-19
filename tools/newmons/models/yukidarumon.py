"""Yukidarumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a living snowman shaped like a big friendly bear: a round snow-white head with little round ears,
dot eyes and a black nose, a chunky snowball body with two red buttons, big rounded snow arms and stumpy legs, a swirl
of icy wind round its feet. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a living snowman shaped like a big friendly bear with round ears, dot eyes, two red buttons and a swirl of icy wind"
BASE = {"snow": (246, 250, 255), "snow_dark": (180, 204, 230), "red": (210, 40, 40), "black": (24, 24, 30),
        "wind": (150, 210, 250, 160)}
SHINY = {"snow": (250, 230, 240), "snow_dark": (220, 170, 200), "red": (60, 120, 220)}


def P(v):
    return pal(BASE, SHINY, v)


SNOW = skin(P, "snow", dark="snow_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.0, b - 28.0) < 0.6:
                return p["black"], None
        if math.hypot(a, b - 26.4) < 0.6:
            return p["black"], None
    return SNOW(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yukidarumon")
    top = m.bone("yukidarumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 14.0, 0), 8.0, SNOW, layers=5, ry=8.6)
    for j in range(2):
        ball(m, bd, (0, 17.0 - j * 3.4, -7.6), 0.9, solid(P, "red"), layers=1)
    hd = m.bone("head", bd, (0, 22, 0))
    ball(m, hd, (0, 27.4, -0.4), 5.0, headf, layers=4)
    for sx in (-1, 1):
        ball(m, hd, (sx * 3.8, 32.0, 0), 1.6, SNOW, layers=2, squash=0.5)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 18.0, 0))
        rod(m, ab, (sx * 7.0, 18.0, 0), (sx * 11.0, 20.0 if sx > 0 else 12.0, -2.0), 3, SNOW, extend=0.6)
        ball(m, ab, (sx * 11.6, 20.6 if sx > 0 else 11.0, -2.4), 3.0, SNOW, layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 7.0, 0))
        m.round_box(lg, sx * 4.4, -0.4, 3.0, 3.4, 0.0, 7.0, SNOW, cut=1)
    wd = m.bone("wind", top, (0, 2, 0))
    for i in range(14):
        ang = i * 2 * math.pi / 14
        r = 11.0 + (i % 3)
        m.box(wd, r * math.cos(ang) - 1.4, 1.0 + (i % 4) * 1.2, r * math.sin(ang) - 1.4, r * math.cos(ang) + 1.4,
              2.0 + (i % 4) * 1.2, r * math.sin(ang) + 1.4, solid(P, "wind", glow=True))
    return m
