"""Runnermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a lightning-fast beast: a lean white body zigzagged with black-and-green bolt stripes, a white
mane, a yellow-and-black lightning crest on its head, big black armoured paws and boots banded green with silver
claws, and a long striped tail ending in a green lightning bolt. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a lean white beast zigzagged with black-and-green bolt stripes, a lightning crest, black armoured green-banded paws and a bolt tail"
BASE = {"white": (240, 242, 246), "white_dark": (180, 184, 196), "black": (30, 30, 36), "black_dark": (10, 10, 12),
        "green": (80, 230, 100), "yellow": (250, 230, 50), "steel": (210, 214, 226), "steel_dark": (110, 114, 126),
        "eye": (230, 50, 50)}
SHINY = {"green": (240, 80, 180), "white": (240, 220, 160), "white_dark": (190, 160, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    zz = (z * 0.6 + abs(math.sin(y * 1.2)) * 1.4) % 5.0
    if zz < 0.6:
        return tone(p["black"], face), None
    if zz < 0.9:
        return tone(p["green"], face), p["green"]
    return fur(P, "white", "white_dark", length=1.2)(x, y, z, face, variant, box=box, **k)


def pawf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if 5.0 < y < 6.4:
        return tone(p["green"], face), p["green"]
    return armour(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("runnermon")
    mats = {"skin": furf, "head": furf, "leg_lower": pawf, "paw": pawf, "claw": metal(P, "steel", dark="steel_dark")}
    a = quadruped(m, mats, "runnermon", length=26.0, body_y=18.0, body_rx=5.4, body_ry=5.4, neck=((0, 22, -14),
                  (0, 25, -18)), head_len=9.0, head_w=3.6, head_h=4.0, teeth=4, tail=((0, 20, 13), (0, 26, 18),
                  (0, 32, 20)), tail_r=(1.6, 1.4, 1.2))
    hd = a["head"]
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.5, sx * 3.8))
        m.box(hd, x0, 26.0, -21.0, x1, 26.8, -19.6, solid(P, "eye", glow=True))
    m.box(hd, -0.4, 28.0, -20.0, 0.4, 33.0, -18.0, solid(P, "yellow"), rotation=(0, 0, 15), pivot=(0, 28.0, -19.0))
    m.box(hd, -0.4, 31.0, -19.0, 0.4, 36.0, -17.0, solid(P, "yellow"), rotation=(0, 0, -20), pivot=(0, 31.0, -18.0))
    for j in range(5):                                                                   # white mane
        spike(m, a["neck"], ((j % 2 * 2 - 1) * 1.6, 25.0, -14.0 + j * 1.2), ((j % 2 * 2 - 1) * 0.6, 1, 0.5), 1.4, 4.0,
              fur(P, "white", "white_dark"), tip=0.8)
    m.box("tail", -0.4, 32.0, 19.0, 0.4, 37.0, 21.0, solid(P, "green", glow=True), rotation=(0, 0, 20), pivot=(0, 32, 20))
    m.box("tail", -0.4, 35.0, 18.0, 0.4, 40.0, 20.0, solid(P, "green", glow=True), rotation=(0, 0, -25), pivot=(0, 35, 19))
    return m
