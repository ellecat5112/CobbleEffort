"""Lucemon: Larva (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the core of the fallen angel: a small cream capsule-shaped body like a seed, a single glowing red eye set in a dark
band, a tail streaming blue-white light, and a fan of long golden feathers sweeping back over it. 35 blocks long (no
level on wikimon besides Ultimate).

Front is -z, y is up. 30 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, feathers, gem, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a small cream capsule-shaped body with one glowing red eye, a tail of blue-white light and a fan of long golden feathers"
BASE = {"cream": (240, 230, 210), "cream_dark": (180, 166, 140), "dark": (50, 40, 60), "red": (240, 40, 40),
        "red_light": (255, 180, 170), "gold": (230, 190, 90), "gold_dark": (150, 110, 30), "light": (170, 220, 255, 190),
        "light_core": (240, 250, 255, 220)}
SHINY = {"gold": (200, 200, 220), "gold_dark": (120, 120, 150), "red": (90, 200, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("lucemonlarva")
    top = m.bone("lucemonlarva", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(6):                                                               # capsule body
        r = 4.0 * math.sin(math.pi * (i + 0.5) / 6) + 0.8
        slab_z(m, bd, 0, 16.0, -6.0 + i * 2.4, -3.6 + i * 2.4, r, r, armour(P, "cream", "cream_dark"))
    m.round_box(bd, 0, -6.4, 4.2, 0.6, 14.6, 17.4, solid(P, "dark"), cut=0)
    m.round_box(bd, 0, -7.0, 1.2, 0.4, 15.0, 17.0, gem(P, "red", "red_light"), cut=0)
    tb = m.bone("tail", bd, (0, 14, 8))                                              # tail of light
    for j in range(4):
        m.round_box(tb, 0, 9.0 + j * 4.0, 1.6 - j * 0.3, 2.4, 13.0 - j * 3.0, 15.0 - j * 3.0,
                    solid(P, "light_core" if j < 2 else "light", glow=True), cut=0)
    FE = feathers(P, "gold", "gold_dark", size=(1.6, 3.0))
    for j in range(9):                                                               # fan of golden feathers
        ang = math.radians(-20 + j * 15)
        spike(m, bd, (0.4 * (j - 4), 18.0, 0.0), (math.sin(ang - 0.6) * 0.6, math.cos(ang - 0.6) * 0.8 + 0.4, 1), 2.4,
              14.0 + (4 - abs(j - 4)) * 1.6, FE, tip=0.8)
    return m
