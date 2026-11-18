"""Kuramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby I
pale lavender star-shaped blob with one huge orange eye in its middle and little dark spikes between its points. A
third of a block tall.

Front is -z, y is up. 14 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a pale lavender star-shaped blob with one huge orange eye"
BASE = {"lav": (210, 210, 240), "lav_dark": (140, 140, 190), "lav_light": (245, 245, 255), "orange": (240, 140, 40),
        "pupil": (24, 20, 20), "white": (255, 255, 255), "dark": (60, 60, 80)}
SHINY = {"lav": (220, 250, 210), "lav_dark": (140, 200, 130), "orange": (90, 160, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x, y - 6.0)
        if math.hypot(x + 0.6, y - 6.8) < 0.5:
            return tone(p["white"], face), None
        if d < 0.9:
            return tone(p["pupil"], face), None
        if d < 2.0:
            return tone(p["orange"], face), None
        if d < 2.3:
            return tone(p["pupil"], face), None
    return skin(P, "lav", dark="lav_dark", light="lav_light")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kuramon")
    top = m.bone("kuramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 6.0, 0), 4.4, bodyf, layers=4)
    for i in range(5):                                                               # star points
        ang = math.radians(90 + i * 72)
        spike(m, bd, (3.6 * math.cos(ang), 6.0 + 3.6 * math.sin(ang), 0), (math.cos(ang), math.sin(ang), 0), 2.4, 3.6,
              skin(P, "lav", dark="lav_dark"), tip=0.8)
        a2 = ang + math.radians(36)
        spike(m, bd, (4.0 * math.cos(a2), 6.0 + 4.0 * math.sin(a2), 0.6), (math.cos(a2), math.sin(a2), 0.3), 0.8, 1.0,
              solid(P, "dark"), tip=0.8)
    return m
