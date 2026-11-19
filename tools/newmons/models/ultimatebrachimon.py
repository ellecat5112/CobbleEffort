"""Ultimate Brachimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a colossal cyborg brachiosaur: a steel-banded body with a great domed steam engine and a
row of smoking funnels on its back, gold-trimmed armour plates, thick armoured legs, a very long segmented steel neck
rising to a spiked dragon head with a toothy jaw, and a long segmented tail ending in a huge double-bladed axe. 35
blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 61
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a colossal cyborg brachiosaur with a domed steam engine and funnels on its back, a very long segmented steel neck and an axe-bladed tail"
BASE = {"steel": (170, 176, 190), "steel_dark": (80, 86, 100), "blue": (80, 100, 130), "blue_dark": (34, 44, 64),
        "gold": (230, 186, 60), "gold_dark": (160, 110, 20), "mouth": (160, 20, 30), "tooth": (250, 250, 244),
        "eye": (250, 60, 50), "smoke": (130, 130, 140, 160), "black": (30, 30, 34)}
SHINY = {"steel": (200, 170, 120), "steel_dark": (120, 90, 50), "blue": (130, 80, 60), "blue_dark": (70, 34, 20)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = riveted(P, "steel", "steel_dark")
BAND = metal(P, "steel", dark="steel_dark")
ARM = armour(P, "blue", "blue_dark", trim="gold", panel=(3.0, 3.0))


def build():
    m = Model("ultimatebrachimon")
    top = m.bone("ultimatebrachimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    for i in range(7):
        z0 = -12.0 + i * 4.0
        r = 8.6 - abs(i - 3) * 0.7
        slab_z(m, bd, 0, 20.0, z0, z0 + 4.2, r, r * 0.9, STEEL if i % 2 else ARM)
    ball(m, bd, (0, 28.0, 2.0), 6.0, metal(P, "steel", dark="steel_dark"), layers=4)      # steam engine dome
    for j in range(5):                                                                 # funnels + smoke
        m.round_box(bd, -3.0 + j * 1.5, -4.0 + j * 0.4, 0.7, 0.7, 28.0, 34.0, metal(P, "black"), cut=0)
    for j in range(4):
        ball(m, bd, (2.0 + j * 2.0, 37.0 + j * 2.0, -4.0 + j), 2.4 + j * 0.6, solid(P, "smoke"), layers=1)
    for sx, sz, nm in ((1, -8.0, "leg_front_left"), (-1, -8.0, "leg_front_right"), (1, 8.0, "leg_back_left"),
                       (-1, 8.0, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 6.0, 16.0, sz))
        m.round_box(lg, sx * 6.4, sz, 3.0, 3.2, 0.0, 16.0, ARM, cut=1)
        for t in range(3):
            spike(m, lg, (sx * 6.4 + (t - 1) * 1.6, 0.8, sz - 3.0), (0, -0.2, -1), 1.0, 2.0, solid(P, "steel"), tip=0.8)
    nk = m.bone("neck", bd, (0, 24, -12))                                              # long segmented neck
    pts = [(0, 24.0, -12.0), (0, 32.0, -18.0), (0, 42.0, -22.0), (0, 50.0, -24.0), (0, 55.0, -27.0)]
    for p0, p1 in zip(pts, pts[1:]):
        for t in range(3):
            q = tuple(p0[c] + (p1[c] - p0[c]) * (t + 0.5) / 3 for c in range(3))
            ball(m, nk, q, 2.6, BAND, layers=1)
            spike(m, nk, (q[0], q[1] + 2.0, q[2] + 0.6), (0, 0.6, 1), 0.9, 2.4, solid(P, "steel"), tip=0.8)
    hd = m.bone("head", nk, (0, 55, -27))
    m.round_box(hd, 0, -30.0, 2.6, 4.0, 54.0, 58.4, STEEL, cut=1)
    m.box(hd, -2.0, 53.0, -35.0, 2.0, 54.4, -30.0, solid(P, "mouth"))
    for j in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.6, 54.0, -34.0 + j * 1.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.4, sx * 2.7), 56.4, -32.0, max(sx * 1.4, sx * 2.7), 57.2, -31.2, solid(P, "eye", glow=True))
    for j in range(5):
        spike(m, hd, (0, 58.0, -32.0 + j * 1.4), (0, 1, 0.8), 1.0, 3.0 + j * 0.4, solid(P, "steel"), tip=0.8)
    tl = m.bone("tail", bd, (0, 20, 14))                                               # segmented tail + axe
    pts = [(0, 20.0, 14.0), (0, 14.0, 24.0), (0, 8.0, 32.0), (0, 5.0, 40.0)]
    for p0, p1 in zip(pts, pts[1:]):
        for t in range(3):
            q = tuple(p0[c] + (p1[c] - p0[c]) * (t + 0.5) / 3 for c in range(3))
            ball(m, tl, q, 2.2, BAND, layers=1)
    m.box(tl, -0.6, 1.6, 40.0, 0.6, 8.6, 46.0, metal(P, "gold", dark="gold_dark"))
    for sx in (-1, 1):
        m.box(tl, min(sx * 0.6, sx * 8.0), 3.0, 41.0, max(sx * 0.6, sx * 8.0), 7.0, 41.8, metal(P, "steel"),
              rotation=(0, sx * -10, 0), pivot=(0, 5.0, 41.4))
    return m
