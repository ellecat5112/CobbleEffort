"""Hover Espimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the hover spy: a blue robot riding a round hovering saucer with an orange band, a helmeted head with a visor and blue
ear-pods, a red chest light, two big blue arms with black claw hands and a pair of smoking back cannons. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, gem, metal, riveted, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a blue robot riding a hovering saucer with an orange band, a visored helmet, a red chest light and back cannons"
BASE = {"blue": (40, 110, 200), "blue_dark": (14, 50, 120), "blue_light": (120, 190, 250), "orange": (240, 140, 30),
        "steel": (180, 186, 200), "steel_dark": (80, 86, 100), "black": (30, 28, 34), "red": (220, 40, 40),
        "red_light": (255, 160, 140), "visor": (200, 210, 230), "smoke": (70, 66, 64, 160)}
SHINY = {"blue": (230, 190, 50), "blue_dark": (170, 120, 10), "blue_light": (255, 240, 150)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", light="blue_light", trim="steel", trim_w=0.3, rivets=True)


def build():
    m = Model("hoverespimon")
    top = m.bone("hoverespimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for j, r in enumerate((14.0, 12.0, 9.0)):                                            # hovering saucer
        m.round_box(bd, 0, 0, r, r * 0.8, 2.0 + j * 2.0, 4.0 + j * 2.0, ARM if j != 1 else metal(P, "orange", dark="steel_dark"),
                    cut=max(1, int(r * 0.3)))
    m.round_box(bd, 0, 0, 5.0, 4.0, 8.0, 22.0, ARM, cut=2)
    m.round_box(bd, 0, -4.0, 1.6, 0.4, 14.0, 17.0, gem(P, "red", "red_light"), cut=0)
    hd = m.bone("head", bd, (0, 22, 0))
    m.round_box(hd, 0, 0, 3.6, 3.4, 22.0, 29.0, metal(P, "steel", dark="steel_dark"), cut=1)
    m.round_box(hd, 0, -3.4, 3.0, 0.4, 24.0, 26.4, solid(P, "visor"), cut=0)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.8, 0, 1.4, 1.6, 27.0, 31.0, ARM, cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 19.0, 0))
        rod(m, ab, (sx * 5.0, 19.0, 0), (sx * 12.0, 14.0, -4.0), 3, ARM, extend=0.6)
        for j in range(3):
            spike(m, ab, (sx * 12.0 + (j - 1) * 1.0, 13.0, -5.6), (sx * 0.3, -0.4, -1), 0.9, 3.0, solid(P, "black"), tip=0.8)
    for sx in (-1, 1):                                                                     # back cannons + smoke
        rod(m, bd, (sx * 3.0, 20.0, 4.0), (sx * 8.0, 26.0, 14.0), 3, ARM, extend=0)
        m.round_box(bd, sx * 8.6, 15.0, 1.6, 1.6, 26.0, 28.0, metal(P, "orange", dark="steel_dark"), cut=0)
    m.round_box(bd, -8.0, -6.0, 3.0, 3.0, 4.0, 10.0, solid(P, "smoke"), cut=1)
    return m
