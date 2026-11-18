"""Lalamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
singing seed: a little round lime-green body under a big pink bell-flower head with two dot eyes and an O-shaped
singing mouth, two yellow sprout leaves on top and little leaf-like arms. Child stage, 1 block tall.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, local, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 6}
LOOK = "a little lime-green body under a big pink bell-flower head with dot eyes, an O-shaped singing mouth and two yellow sprout leaves"
BASE = {"lime": (170, 220, 90), "lime_dark": (100, 160, 40), "pink": (240, 170, 190), "pink_dark": (200, 110, 140),
        "yellow": (240, 220, 110), "yellow_dark": (190, 160, 50), "eye": (30, 24, 30)}
SHINY = {"pink": (180, 200, 250), "pink_dark": (110, 130, 210), "lime": (240, 200, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.8, y - 15.0) < 0.6:
                return tone(p["eye"], face), None
        if abs(math.hypot(x, y - 13.0) - 0.7) < 0.3:
            return tone(p["eye"], face), None
    return skin(P, "pink", dark="pink_dark")(x, y, z, face, variant, box=box, **k)


def leaf_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    return a * a / 0.25 + b * b / 0.25 < 1.0


def build():
    m = Model("lalamon")
    top = m.bone("lalamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 5.0, 0), 4.0, skin(P, "lime", dark="lime_dark"), layers=3)
    hd = m.bone("head", bd, (0, 9, 0))
    m.round_box(hd, 0, 0, 4.4, 4.0, 10.0, 18.0, headf, cut=2)                          # bell-flower head
    for i in range(6):                                                               # petal lip
        ang = 2 * math.pi * i / 6
        spike(m, hd, (4.0 * math.cos(ang), 10.6, 3.6 * math.sin(ang)), (math.cos(ang), -0.6, math.sin(ang)), 1.6, 2.2,
              skin(P, "pink", dark="pink_dark"), tip=0.8)
    rod(m, hd, (0, 18.0, 0), (0, 20.0, 0), 1, solid(P, "yellow_dark"), extend=0, t2=1)
    for sx in (-1, 1):                                                               # sprout leaves
        m.box(hd, min(0, sx * 6.0), 19.6, -1.2, max(0, sx * 6.0), 19.6, 1.2, cutout(leaf_in, skin(P, "yellow", dark="yellow_dark")),
              rotation=(0, 0, sx * 15), pivot=(0, 19.6, 0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # little leaf arms
        ab = m.bone(nm, bd, (sx * 3.6, 6.0, 0))
        spike(m, ab, (sx * 3.4, 6.0, 0), (sx, 0.4, -0.2), 1.4, 2.6, skin(P, "lime", dark="lime_dark"), tip=0.8)
    return m
