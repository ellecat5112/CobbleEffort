"""Proto Gizmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the prototype Gizumon: a violet metal dome of a body with one glowing yellow lens on a jointed
arm, four long bladed spider legs of purple and black on cabled joints, and a fringe of green ribbed hose tentacles
hanging beneath. 1 block.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 2.6)
KIND = "floater"
K = 3
LOOK = "a violet metal dome with one glowing yellow lens, four long bladed spider legs and a fringe of green hose tentacles"
BASE = {"violet": (110, 60, 170), "violet_dark": (50, 20, 90), "black": (30, 26, 36), "green": (70, 140, 70),
        "green_dark": (24, 80, 30), "lens": (250, 210, 40), "lens_core": (230, 60, 40), "steel": (180, 184, 196)}
SHINY = {"violet": (190, 40, 50), "violet_dark": (100, 14, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def hosef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green_dark"] if (y % 1.2) < 0.4 else p["green"], face), None


def build():
    m = Model("protogizmon")
    top = m.bone("protogizmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 22.0, 0), 6.0, metal(P, "violet", dark="violet_dark"), layers=5, ry=5.0)
    m.round_box(bd, 0, 0, 5.0, 5.0, 16.0, 18.0, metal(P, "black"), cut=1)
    rod(m, bd, (2.0, 20.0, -5.0), (3.0, 18.0, -8.0), 1, metal(P, "steel"), extend=0.2)
    ball(m, bd, (3.0, 18.0, -8.6), 1.4, solid(P, "lens", glow=True), layers=2)
    m.box(bd, 2.4, 17.4, -10.1, 3.6, 18.6, -9.9, solid(P, "lens_core", glow=True))
    for i in range(10):                                                                  # hose tentacles
        ang = 2 * math.pi * i / 10
        x0, z0 = 3.6 * math.cos(ang), 3.6 * math.sin(ang)
        rod(m, bd, (x0, 16.0, z0), (x0 * 1.1, 8.0 - (i % 3), z0 * 1.1), 1, hosef, extend=0.2)
    for sx in (-1, 1):                                                                   # bladed spider legs
        for sz in (-1, 1):
            nm = f"leg_{'front' if sz < 0 else 'back'}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, bd, (sx * 5.0, 22.0, sz * 3.0))
            knee = (sx * 13.0, 28.0, sz * 7.0)
            rod(m, lg, (sx * 5.0, 22.0, sz * 3.0), knee, 1, metal(P, "steel"), extend=0.3)
            m.round_box(lg, knee[0], knee[2], 1.4, 1.4, knee[1] - 1.4, knee[1] + 1.4, metal(P, "black"), cut=0)
            spike(m, lg, knee, (sx * 0.3, -1, sz * 0.2), 2.0, 26.0, metal(P, "violet", dark="violet_dark"), tip=0.8)
    return m
