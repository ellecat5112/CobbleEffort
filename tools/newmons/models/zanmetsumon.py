"""Zanmetsumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a samurai lord riding a beast: a huge shaggy purple-black mammoth-like dragon with a gaping
shark-toothed maw in its chest, white tusks, gold-banded legs and a trunk-like tail curling up with a guard, and
astride it a blue-skinned samurai in black-and-gold armour with a horned kabuto, wielding katana in several hands, the
blades trailing blue spirit-fire. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a samurai in black-and-gold armour with many katana riding a shaggy purple-black beast with a shark-toothed maw in its chest"
BASE = {"purple": (80, 64, 96), "purple_dark": (30, 22, 40), "tooth": (250, 250, 244), "mouth": (40, 20, 30),
        "gold": (230, 186, 60), "gold_dark": (160, 110, 20), "black": (36, 34, 40), "black_dark": (12, 12, 14),
        "blue": (90, 140, 180), "blue_dark": (40, 80, 120), "steel": (220, 226, 240), "fire": (110, 170, 255, 180),
        "eye": (255, 220, 80)}
SHINY = {"purple": (150, 110, 70), "purple_dark": (80, 50, 24)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "purple", "purple_dark", length=2.0)
ARM = armour(P, "black", "black_dark", trim="gold", panel=(2.4, 2.4))


def build():
    m = Model("zanmetsumon")
    top = m.bone("zanmetsumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(6):
        z0 = -10.0 + i * 4.0
        slab_z(m, bd, 0, 17.0, z0, z0 + 4.2, 8.0, 8.0, FUR)
    m.box(bd, -6.0, 10.0, -12.0, 6.0, 20.0, -10.0, solid(P, "mouth"))                       # chest maw
    for j in range(7):
        x = -5.4 + j * 1.8
        spike(m, bd, (x, 20.0, -11.6), (0, -1, 0), 1.4, 3.6, solid(P, "tooth"), tip=0.8)
        spike(m, bd, (x, 10.0, -11.6), (0, 1, 0), 1.4, 3.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        spike(m, bd, (sx * 6.0, 10.0, -11.0), (sx * 0.4, -0.2, -1), 1.8, 8.0, solid(P, "tooth"), tip=0.8)
    for sx, sz, nm in ((1, -6.0, "leg_front_left"), (-1, -6.0, "leg_front_right"), (1, 8.0, "leg_back_left"),
                       (-1, 8.0, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 5.0, 12.0, sz))
        m.round_box(lg, sx * 5.4, sz, 2.8, 3.0, 0.0, 12.0, FUR, cut=1)
        m.round_box(lg, sx * 5.4, sz, 3.0, 3.2, 3.0, 4.4, metal(P, "gold"), cut=1)
        for t in range(3):
            spike(m, lg, (sx * 5.4 + (t - 1) * 1.6, 0.8, sz - 3.0), (0, -0.2, -1), 1.0, 2.0, solid(P, "tooth"), tip=0.8)
    tl = m.bone("tail", bd, (0, 18, 14))
    pts = [(0, 18.0, 14.0), (0, 24.0, 18.0), (2.0, 30.0, 16.0), (4.0, 32.0, 12.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, FUR, extend=0.4)
    rd = m.bone("rider", bd, (0, 25, -2))                                               # the samurai
    m.round_box(rd, 0, -2.0, 4.0, 3.0, 25.0, 30.0, ARM, cut=1)
    m.round_box(rd, 0, -2.0, 4.4, 3.4, 30.0, 37.0, ARM, cut=1)
    m.round_box(rd, 0, -2.0, 2.4, 2.6, 37.0, 42.0, skin(P, "blue", dark="blue_dark"), cut=1)
    m.box(rd, -1.8, 40.0, -4.8, 1.8, 40.8, -4.5, solid(P, "eye", glow=True))
    m.round_box(rd, 0, -2.0, 3.0, 3.0, 41.6, 43.6, metal(P, "gold", dark="gold_dark"), cut=1)
    spike(m, rd, (0, 43.6, -4.0), (0, 1, -0.4), 1.4, 5.0, metal(P, "gold"), tip=0.8)
    for i, (sx, y, ang) in enumerate(((1, 34.0, 50), (-1, 34.0, -50), (1, 30.0, 25), (-1, 30.0, -25))):
        rod(m, rd, (sx * 4.0, y, -2.0), (sx * 9.0, y + 2.0, -4.0), 1, skin(P, "blue", dark="blue_dark"), extend=0.3)
        h = (sx * 9.0, y + 2.0, -4.0)
        m.box(rd, h[0] - 0.5, h[1], h[2] - 0.5, h[0] + 0.5, h[1] + 20.0, h[2] + 0.5, metal(P, "steel"),
              rotation=(0, 0, -ang), pivot=h)
        m.box(rd, h[0] - 1.0, h[1] + 4.0, h[2] - 1.0, h[0] + 1.0, h[1] + 20.0, h[2] + 1.0, solid(P, "fire", glow=True),
              rotation=(0, 0, -ang), pivot=h)
    return m
