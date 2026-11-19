"""Sunmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little orange-red sun ball with a happy smile, black eyes, five stubby sun-ray spikes round it and a
yellow flame flickering on top. 0.5 blocks.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = "a little orange-red sun ball with a happy smile, black eyes, stubby sun-ray spikes and a yellow flame on top"
BASE = {"orange": (240, 90, 40), "orange_dark": (180, 40, 14), "orange_light": (255, 160, 110), "black": (24, 20, 20),
        "white": (255, 255, 255), "flame": (255, 210, 60)}
SHINY = {"orange": (90, 140, 240), "orange_dark": (30, 70, 180), "orange_light": (160, 200, 255), "flame": (180, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "orange", dark="orange_dark", light="orange_light", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 6.6) < 0.7:
                return tone(p["white"] if math.hypot(x - sx * 1.6 + 0.2, y - 6.9) < 0.25 else p["black"], face), None
        if abs(y - 4.4 - 0.12 * x * x) < 0.18 and abs(x) < 1.8:
            return tone(p["black"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("sunmon")
    top = m.bone("sunmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 6.0, 0), 4.4, bodyf, layers=4)
    for j in range(5):
        ang = math.radians(-18 + j * 72 - 90)
        spike(m, bd, (4.0 * math.cos(ang), 6.0 + 4.0 * math.sin(ang), 0), (math.cos(ang), math.sin(ang), 0), 1.6, 2.6,
              SKIN, tip=0.8)
    spike(m, bd, (0, 10.0, 0), (0.3, 1, 0), 1.6, 7.0, solid(P, "flame", glow=True), tip=0.8)
    return m
