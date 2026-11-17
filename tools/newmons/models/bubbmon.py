"""Bubbmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a bubbly slime baby. A pale lime-green jelly puddle that rises to a rounded head with two black
eyes and a little round mouth, glossy highlights, and soap bubbles clinging to its head and floating above it.
Baby I.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import mix, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 0.5)
KIND = "floater"
K = 4
LOOK = "a pale lime-green jelly puddle rising to a rounded head with black eyes, a round mouth and floating bubbles"
BASE = {"lime": (210, 236, 160, 230), "lime_dark": (150, 190, 100), "white": (252, 255, 240), "eye": (20, 20, 20),
        "mouth": (230, 210, 120), "bubble": (220, 245, 200, 150), "bubble_light": (255, 255, 255, 200)}
SHINY = {"lime": (200, 210, 250, 230), "lime_dark": (130, 140, 210), "bubble": (220, 220, 255, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def jellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.2, y - 10.0) < 0.9:
                return tone(p["eye"], face), None
        d = math.hypot(x + 0.8, y - 7.4)
        if d < 1.2:
            return tone(p["mouth"] if d > 0.5 else p["lime_dark"], face), None
    if math.hypot(x + 2.6, y - 12.6) < 1.0 or face == "up" and (x + z) % 5 < 0.8:
        return tone(p["white"], face), None
    return tone(p["lime"][:3], face), None


def bubblef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["bubble_light"] if face in ("up", "north") and (x + y) % 2 < 0.5 else p["bubble"]
    return c, None


def build():
    m = Model("bubbmon")
    top = m.bone("bubbmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for r, y0, y1, cz in ((9.0, 0.0, 1.4, 0.6), (7.4, 1.4, 3.0, 0.3), (6.0, 3.0, 10.0, 0.0), (5.4, 10.0, 12.6, 0.0),
                          (4.2, 12.6, 14.0, 0.0), (2.6, 14.0, 14.8, 0.0)):
        m.round_box(bd, 0, cz, r, r * 0.86, y0, y1, jellyf, cut=max(1, round(r * 0.35)))
    for sx in (-1, 1):                                                       # ragged puddle lobes
        m.round_box(bd, sx * 8.4, 2.0, 2.4, 2.0, 0.0, 1.2, jellyf, cut=1)
    hd = m.bone("head", bd, (0, 12, 0))
    for c, r in (((4.6, 14.0, 0.0), 1.8), ((-4.4, 15.6, 1.0), 1.6), ((1.4, 17.0, -0.6), 1.4), ((5.4, 17.6, 1.0), 1.0),
                 ((-1.6, 19.0, 1.0), 1.8)):
        ball(m, hd, c, r, bubblef, layers=3)
    return m
