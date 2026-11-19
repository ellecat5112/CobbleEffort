"""Sharkmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a cyborg shark warship: a sleek navy-and-violet armoured shark with a green glass eye, a jagged steel-
toothed maw, a tall swept dorsal fin and blade-fins, engine pipes along its back, a serrated keel of blue fins beneath,
and two little shark-headed torpedoes streaking ahead. 25 blocks.

Front is -z, y is up. 36 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a sleek navy-and-violet cyborg shark warship with a green glass eye, a steel-toothed maw, blade fins and two shark-headed torpedoes"
BASE = {"navy": (40, 40, 90), "navy_dark": (14, 14, 40), "violet": (90, 70, 160), "blue": (60, 100, 200),
        "blue_dark": (24, 50, 130), "steel": (210, 214, 226), "steel_dark": (110, 114, 130), "green": (90, 240, 160),
        "white": (240, 250, 250), "mouth": (130, 30, 40)}
SHINY = {"navy": (130, 40, 50), "navy_dark": (60, 14, 20), "violet": (200, 90, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "navy", "navy_dark", trim="violet", trim_w=0.25)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("sharkmon")
    top = m.bone("sharkmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    for i in range(8):                                                                   # hull slices
        t = (i + 0.5) / 8
        r = 6.0 * math.sin(math.pi * (0.25 + 0.7 * t)) + 1.0
        slab_z(m, bd, 0, 16.0, -14.0 + i * 4.0, -14.0 + (i + 1) * 4.0 + 0.2, r * 0.9, r, HULL)
    hd = m.bone("head", bd, (0, 16, -14))
    m.round_box(hd, 0, -19.0, 4.0, 5.0, 13.0, 20.0, HULL, cut=1)
    spike(m, hd, (0, 17.0, -24.0), (0, -0.1, -1), 3.0, 6.0, HULL, tip=0.8)
    m.box(hd, -3.6, 12.6, -24.0, 3.6, 14.6, -15.0, solid(P, "mouth"))
    for j in range(6):
        for sx in (-1, 1):
            spike(m, hd, (sx * 3.4, 14.6, -23.0 + j * 1.4), (0, -1, 0), 0.9, 1.6, STEEL, tip=0.8)
            spike(m, hd, (sx * 3.2, 12.6, -23.0 + j * 1.4), (0, 1, 0), 0.9, 1.2, STEEL, tip=0.8)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.6, -18.0, 1.0, 1.6, 17.6, 19.6, gem(P, "green", "white"), cut=0)
    spike(m, bd, (0, 22.0, -2.0), (0, 1, 0.8), 3.0, 18.0, HULL, tip=0.8)                    # tall swept dorsal fin
    for sx in (-1, 1):
        spike(m, bd, (sx * 5.0, 14.0, -4.0), (sx * 1, -0.2, 0.6), 2.0, 9.0, armour(P, "blue", "blue_dark"), tip=0.8)
        rod(m, bd, (sx * 2.6, 21.0, 2.0), (sx * 2.6, 21.0, 14.0), 1, STEEL, extend=0.2, t2=2)   # engine pipes
    for j in range(6):                                                                   # serrated keel fins
        spike(m, bd, (0, 10.0, -10.0 + j * 4.0), (0, -1, 0.4), 1.4, 4.0, armour(P, "blue", "blue_dark"), tip=0.8)
    spike(m, bd, (0, 16.0, 18.0), (0, 0.7, 1), 2.4, 10.0, HULL, tip=0.8)                    # tail fin
    spike(m, bd, (0, 16.0, 18.0), (0, -0.6, 1), 2.0, 7.0, HULL, tip=0.8)
    for j, (dx, dy) in enumerate(((-6.0, 6.0), (-10.0, 2.0))):                             # shark torpedoes
        c = (dx, dy, -30.0 - j * 4.0)
        rod(m, bd, (c[0], c[1], c[2] + 6.0), c, 2, STEEL, extend=0.2)
        spike(m, bd, c, (0, 0, -1), 1.4, 2.0, solid(P, "navy"), tip=0.8)
    return m
