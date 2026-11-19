"""Vipmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little vine serpent: a violet snake-dragon with a horned head and a forked tongue, its body
wrapped round a bunch of glossy purple grapes, green vine leaves sprouting from its back and a pink-bellied coiled
tail. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, gem, skin, solid
from _route import pal, tone

HEIGHT = 23
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "floater"
K = 3
LOOK = "a violet vine serpent coiled round a bunch of glossy purple grapes, with green vine leaves and a horned head"
BASE = {"violet": (150, 70, 190), "violet_dark": (80, 30, 120), "grape": (120, 40, 110), "grape_light": (220, 150, 220),
        "leaf": (70, 170, 70), "leaf_dark": (30, 100, 30), "belly": (240, 170, 190), "tongue": (220, 60, 80),
        "eye": (250, 220, 60), "pupil": (20, 10, 20), "white": (255, 255, 255), "horn": (40, 34, 46)}
SHINY = {"violet": (60, 150, 110), "violet_dark": (20, 90, 60), "grape": (60, 140, 60), "grape_light": (180, 240, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 6.0, y - 19.6, 0.8, "eye", slit=True)
        if c is not None:
            return c, None
    return skin(P, "violet", dark="violet_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vipmon")
    top = m.bone("vipmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i, (x, y, z) in enumerate(((0, 12, 0), (-2, 10, 1), (2, 10, 1), (0, 8, 0), (-1.4, 6.4, 1), (1.4, 6.4, 1),
                                   (0, 4.6, 0.6), (-3, 12.4, -0.6), (3, 12.4, -0.6))):
        ball(m, bd, (x, y, z), 2.0, gem(P, "grape", "grape_light", glow=False), layers=2)
    for i in range(12):                                                                # body coiled round the grapes
        ang = i * 0.6
        r = 4.4
        p0 = (r * math.cos(ang), 4.0 + i * 1.1, r * math.sin(ang))
        p1 = (r * math.cos(ang + 0.6), 4.0 + (i + 1) * 1.1, r * math.sin(ang + 0.6))
        rod(m, bd, p0, p1, 2, skin(P, "violet", dark="violet_dark"), extend=0.4)
    hd = m.bone("head", bd, (0, 18, -3))
    m.round_box(hd, 0, -4.0, 2.0, 3.0, 17.4, 21.0, headf, cut=1)
    spike(m, hd, (0, 18.0, -7.0), (0, -0.2, -1), 0.8, 3.0, solid(P, "tongue"), tip=0.8)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.4, 21.0, -3.0), (sx * 0.3, 1, 0.6), 1.0, 3.4, solid(P, "horn"), tip=0.8)
    for j in range(4):                                                                 # vine leaves
        ang = (j - 1.5) * 0.7
        spike(m, bd, (math.sin(ang) * 2.0, 15.0, 2.0), (math.sin(ang), 0.8, 0.6), 2.2, 5.0, skin(P, "leaf", dark="leaf_dark"),
              tip=0.8)
    tl = m.bone("tail", bd, (3, 4, 2))
    for i in range(8):
        ang = i * 0.8
        r = 3.0 - i * 0.25
        p0 = (5.0 + r * math.cos(ang), 3.0 + r * math.sin(ang) * 0.4, 3.0 + r * math.sin(ang))
        p1 = (5.0 + (r - 0.25) * math.cos(ang + 0.8), 3.0 + (r - 0.25) * math.sin(ang + 0.8) * 0.4,
              3.0 + (r - 0.25) * math.sin(ang + 0.8))
        rod(m, tl, p0, p1, 1, skin(P, "belly", dark="violet"), extend=0.2)
    return m
