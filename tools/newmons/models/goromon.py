"""Goromon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby II pebble: a grey rounded rock with one big yellow eye set in a dark hollow, a jagged dark mouth beneath it and
little stones tumbling around it. Half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a grey rounded rock with one big yellow eye in a dark hollow and a jagged dark mouth"
BASE = {"rock": (150, 150, 156), "rock_dark": (90, 90, 96), "rock_light": (200, 200, 206), "hollow": (20, 18, 22),
        "eye": (250, 210, 40), "pupil": (20, 18, 22)}
SHINY = {"rock": (200, 150, 110), "rock_dark": (140, 90, 60), "rock_light": (240, 200, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ROCK = skin(P, "rock", dark="rock_dark", light="rock_light")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 9.0)
        if d < 0.9:
            return tone(p["pupil"], face), None
        if d < 2.4:
            return tone(p["eye"], face), None
        if abs(x) < 4.4 and 5.0 < y < 7.6 - 0.8 * abs(((x + 4.4) % 2.2) - 1.1):
            return tone(p["hollow"], face), None
        if d < 3.4:
            return tone(p["hollow"], face), None
    return ROCK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("goromon")
    top = m.bone("goromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    ball(m, bd, (0, 7.5, 0), 7.0, facef, layers=5, ry=7.5)
    for c in ((-8.0, 1.0, -2.0), (8.4, 3.0, -1.0), (7.0, 0.6, -5.0)):
        m.round_box(bd, c[0], c[2], 1.0, 1.0, c[1], c[1] + 1.6, ROCK, cut=0)
    m.bone("head", bd, (0, 12, 0))
    return m
