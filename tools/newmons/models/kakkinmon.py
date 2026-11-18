"""Kakkinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby II orange ball wearing a big green armour shell helmet rimmed in bronze with a red gem on top and a leather
strap, so only its grinning fanged face and a little black peak show beneath. Half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "an orange ball under a big green armour shell helmet with a bronze rim and a red gem, grinning with fangs"
BASE = {"orange": (250, 150, 40), "orange_dark": (190, 90, 14), "green": (60, 120, 60), "green_dark": (20, 60, 20),
        "green_light": (130, 190, 120), "bronze": (170, 110, 50), "bronze_dark": (100, 60, 24), "red": (220, 40, 40),
        "red_light": (255, 160, 140), "eye": (24, 24, 30), "tooth": (250, 250, 246), "black": (30, 30, 34)}
SHINY = {"green": (150, 80, 160), "green_dark": (80, 30, 90), "green_light": (220, 160, 230)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(y - 5.4) < 0.5 and abs(x) < 3.0:
            return tone(p["tooth"] if (x + 4.0) % 1.2 < 0.6 else p["black"], face), None
        for sx in (-1, 1):
            if abs(x - sx * 1.8) < 0.7 and abs(y - 7.6) < 0.4:
                return tone(p["eye"], face), None
    return skin(P, "orange", dark="orange_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kakkinmon")
    top = m.bone("kakkinmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 6.0, 0), 4.6, bodyf, layers=4)
    hd = m.bone("head", bd, (0, 9, 0))
    SH = armour(P, "green", "green_dark", light="green_light")
    for j, (r, y0, y1) in enumerate(((6.4, 8.0, 10.0), (5.6, 10.0, 12.6), (4.2, 12.6, 14.4))):
        m.round_box(hd, 0, 0.6, r, r, y0, y1, SH, cut=max(1, int(r * 0.4)))
    m.round_box(hd, 0, 0.6, 6.8, 6.8, 7.6, 8.6, metal(P, "bronze", dark="bronze_dark"), cut=2)        # bronze rim
    m.round_box(hd, 0, 0.6, 1.2, 1.2, 14.2, 15.6, gem(P, "red", "red_light"), cut=0)
    m.round_box(hd, 0, 5.6, 2.4, 1.2, 6.4, 7.6, solid(P, "black"), cut=0)
    m.round_box(hd, 4.8, 0.6, 0.6, 1.6, 5.0, 8.0, leather(P, "bronze", "bronze_dark"), cut=0)
    return m
