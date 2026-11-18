"""Gurimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby
II round white blob with a crown of red-tipped spikes and a red cone horn, big yellow eyes, a little cat mouth and
blushing cheeks: Gammamon's baby form. Half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a round white blob with a crown of red-tipped spikes, a red cone horn, big yellow eyes and blushing cheeks"
BASE = {"white": (250, 248, 244), "white_dark": (200, 196, 190), "red": (220, 60, 70), "eye": (250, 210, 40),
        "pupil": (20, 18, 16), "cheek": (250, 170, 180), "black": (30, 28, 32)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "red": (240, 150, 40)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = skin(P, "white", dark="white_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.4, y - 7.6)
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.5:
                return tone(p["eye"], face), None
            if math.hypot(x - sx * 4.0, y - 5.6) < 0.8:
                return tone(p["cheek"], face), None
        if abs(y - 5.4) < 0.25 and abs(x) < 0.9:
            return tone(p["black"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gurimon")
    top = m.bone("gurimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 6.5, 0), 6.0, bodyf, layers=5, ry=6.0)
    hd = m.bone("head", bd, (0, 12, 0))
    for j in range(7):                                                                   # crown of spikes
        ang = math.radians(-150 + j * 50)
        spike(m, hd, (5.0 * math.sin(ang), 9.0 + 3.0 * math.cos(ang) * 0.4, 2.0 + 3.0 * math.cos(ang)),
              (math.sin(ang), 0.6, 0.6 + 0.4 * math.cos(ang)), 2.0, 3.6, WHITE, tip=None)
        spike(m, hd, (5.0 * math.sin(ang) + math.sin(ang) * 2.4, 11.0, 4.0 + math.cos(ang) * 2.0),
              (math.sin(ang), 0.6, 0.6), 1.0, 1.4, solid(P, "red"))
    spike(m, hd, (0, 12.4, -1.0), (0, 1, -0.2), 1.8, 3.0, solid(P, "red"), tip=0.8)
    return m
