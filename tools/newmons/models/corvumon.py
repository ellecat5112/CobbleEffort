"""Corvumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ghostly raven. A dark indigo raven with a ragged white mane round its head and shoulders, a
grey hooked beak, red eyes, enormous pale silvery wings with ragged feather tips spread wide, and grey taloned feet.
15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage (floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "floater"
K = 3
LOOK = ("a dark indigo raven with a ragged white mane, a hooked grey beak, red eyes and enormous pale silvery ragged "
        "wings spread wide")
BASE = {"indigo": (50, 50, 110), "indigo_dark": (20, 20, 50), "white": (240, 242, 250), "white_dark": (180, 186, 204),
        "beak": (130, 134, 150), "beak_dark": (70, 72, 86), "eye": (230, 40, 40), "talon": (90, 92, 104)}
SHINY = {"indigo": (110, 30, 50), "indigo_dark": (50, 10, 20), "white": (240, 220, 160), "white_dark": (190, 160, 100)}


def P(v):
    return pal(BASE, SHINY, v)


DARK = feathers(P, "indigo", "indigo_dark", size=(1.0, 1.8))
PALE = feathers(P, "white", "white_dark", size=(1.6, 3.2), flow=(0, 1))


def build():
    m = Model("corvumon")
    top = m.bone("corvumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    ball(m, bd, (0, 20.0, 1.0), 5.6, DARK, layers=5, squash=1.3)
    hd = m.bone("head", bd, (0, 27, -1))
    m.round_box(hd, 0, -1.0, 3.2, 3.4, 26.0, 32.0, DARK, cut=1)
    spike(m, hd, (0, 28.6, -4.4), (0, -0.4, -1), 2.4, 4.0, metal(P, "beak", dark="beak_dark"), tip=0.4)
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.1, sx * 3.4), 29.6, -2.6, max(sx * 3.1, sx * 3.4), 30.4, -1.6, solid(P, "eye", glow=True))
    for i in range(14):                                                     # ragged white mane
        ang = math.radians(i * 360 / 14)
        spike(m, hd, (3.6 * math.cos(ang), 27.0 + 2.0 * math.sin(ang), 1.0 + 1.0 * math.sin(ang)),
              (math.cos(ang), 0.2 + 0.4 * math.sin(ang), 0.6), 1.8, 4.0, PALE, tip=0.5)
    wb = m.bone("wings", bd, (0, 24, 2))                                    # enormous pale wings
    for sx in (-1, 1):
        for j, ang in enumerate((55, 30, 8, -15)):
            x0, x1 = sorted((sx * 3.0, sx * (24.0 - j * 2.0)))
            m.box(wb, x0, 22.0, 2.0 + j * 0.5, x1, 28.0, 2.0 + j * 0.5, PALE, rotation=(0, sx * 10, sx * ang),
                  pivot=(sx * 3.0, 25.0, 2.0 + j * 0.5))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                     # taloned feet
        lg = m.bone(nm, top, (sx * 2.0, 15.0, 1.0))
        rod(m, lg, (sx * 2.0, 15.0, 1.0), (sx * 2.4, 9.0, 0.0), 2, solid(P, "talon"), extend=0.3)
        for d in ((-0.5, -1, -1), (0, -1, -1), (0.5, -1, -1)):
            spike(m, lg, (sx * 2.4, 9.0, 0.0), d, 0.8, 3.0, solid(P, "talon"))
    tl = m.bone("tail", bd, (0, 16, 5))
    for j in range(5):
        spike(m, tl, (0, 16.0, 5.0), ((j - 2) * 0.3, -1, 0.5), 1.6, 9.0, PALE, tip=0.5)
    return m
