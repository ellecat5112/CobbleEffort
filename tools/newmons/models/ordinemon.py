"""Ordinemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fallen angel of ruin: two vast shaggy masses of black-violet feathers rearing up like twin
serpentine wings, each crowned with a great glowing gem eye (one green, one violet) and ending in hooked blades, a
small pale skeletal figure hanging between them, and black feathers drifting away. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, gem, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = ("two vast shaggy masses of black-violet feathers rearing like twin serpentine wings, each crowned with a glowing "
        "gem eye and ending in hooked blades, a pale skeletal figure hanging between")
BASE = {"feather": (60, 50, 90), "feather_dark": (20, 16, 34), "green": (90, 230, 120), "green_light": (220, 255, 220),
        "violet": (170, 110, 250), "violet_light": (240, 220, 255), "bone": (230, 228, 236), "blade": (90, 80, 160)}
SHINY = {"feather": (200, 200, 220), "feather_dark": (130, 130, 150), "blade": (220, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "feather", "feather_dark")


def build():
    m = Model("ordinemon")
    top = m.bone("ordinemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    for sx, gem_key in ((1, "violet"), (-1, "green")):                                    # twin feather serpents
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 4.0, 34.0, 0))
        chain = [(sx * 20.0, 4.0, 3.0), (sx * 22.0, 18.0, 5.0), (sx * 22.0, 34.0, 6.0), (sx * 18.0, 50.0, 4.0),
                 (sx * 12.0, 60.0, 2.0)]
        for j, (p0, p1) in enumerate(zip(chain, chain[1:])):
            rod(m, wb, p0, p1, 7 - j, FEATH, extend=0.8)
            for i in range(4):
                ang = 2 * math.pi * i / 4 + j
                spike(m, wb, p0, (math.cos(ang), 0.3, math.sin(ang)), 2.0, 6.0, FEATH, tip=0.8)
        h = chain[-1]
        ball(m, wb, (h[0], h[1] + 2.0, h[2] - 1.0), 3.4, FEATH, layers=3)
        ball(m, wb, (h[0], h[1] + 2.0, h[2] - 3.6), 1.6, gem(P, gem_key, gem_key + "_light"), layers=2)   # gem eye
        spike(m, wb, (h[0] - sx * 2.0, h[1] - 1.0, h[2] - 2.0), (-sx * 1, -0.8, -0.4), 1.8, 12.0,
              metal(P, "blade"), tip=0.8)                                                # hooked blade
        rod(m, wb, (sx * 4.0, 34.0, 0), chain[0], 4, FEATH, extend=0.6)
    sk = m.bone("figure", bd, (0, 36, 0))                                                # pale skeletal figure
    m.round_box(sk, 0, 0, 1.2, 1.0, 30.0, 38.0, solid(P, "bone"), cut=0)
    m.round_box(sk, 0, 0, 1.2, 1.2, 38.0, 40.6, solid(P, "bone"), cut=0)
    for sx in (-1, 1):
        rod(m, sk, (sx * 1.0, 37.0, 0), (sx * 3.0, 32.0, -1.0), 1, solid(P, "bone"), extend=0.1)
        rod(m, sk, (sx * 0.6, 30.0, 0), (sx * 1.0, 24.0, 0), 1, solid(P, "bone"), extend=0.1)
    return m
