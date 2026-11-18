"""Gigimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby
II round red blob, Guilmon's baby form: two tall pointed red ears tipped black, big yellow eyes, a black mark on its
cheek, a toothy grin and a pale belly. Half a block tall.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a round red blob with tall black-tipped ears, big yellow eyes, a black cheek mark and a toothy grin"
BASE = {"red": (240, 90, 80), "red_dark": (180, 40, 40), "belly": (250, 230, 220), "black": (30, 26, 30),
        "eye": (250, 210, 40), "pupil": (20, 16, 10), "white": (250, 250, 250)}
SHINY = {"red": (90, 90, 100), "red_dark": (40, 40, 50)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.2, y - 9.6)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.3:
                return tone(p["eye"], face), None
        if 2.6 < x < 4.4 and 7.0 < y < 8.2 and (x - 2.6) * 0.6 > (8.2 - y) * 0.4:
            return tone(p["black"], face), None
        if abs(y - 6.0 - 0.15 * x * x) < 0.3 and abs(x) < 2.4:
            return tone(p["black"], face), None
        if y < 4.0:
            return tone(p["belly"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gigimon")
    top = m.bone("gigimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 7.0, 0), 6.0, bodyf, layers=5)
    hd = m.bone("head", bd, (0, 12, 0))
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 11.6, 0.4), (sx * 0.4, 1, 0.2), 2.6, 5.0, RED, tip=None)
        spike(m, hd, (sx * 4.9, 16.4, 1.4), (sx * 0.4, 1, 0.2), 1.4, 2.0, solid(P, "black"))
    return m
