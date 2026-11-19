"""Zhuqiaomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Vermilion Bird, holy beast of the south: a blazing crimson phoenix patterned with golden flame,
a long spear-like beak, a black face-ring set with glowing red orbs, vast swept wings of red-and-gold feathers, black
talons, and a long fan of fiery tail feathers trailing sparks. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, metal, solid
from _route import pal, tone

HEIGHT = 37
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a blazing crimson phoenix patterned with golden flame, a spear-like beak, red orbs on a black face-ring and vast red-and-gold wings"
BASE = {"red": (210, 40, 30), "red_dark": (130, 14, 10), "gold": (250, 200, 60), "black": (30, 26, 30),
        "orb": (255, 90, 90), "beak": (250, 210, 80), "spark": (255, 220, 120)}
SHINY = {"red": (60, 100, 220), "red_dark": (20, 40, 130), "gold": (150, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(x * 0.7 + y * 0.9) + math.cos(z * 0.6 - x * 0.3)) < 0.25:
        return tone(p["gold"], face), p["gold"]
    return feathers(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zhuqiaomon")
    top = m.bone("zhuqiaomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 21.0, 0), 5.6, flamef, layers=4, ry=7.0)
    hd = m.bone("head", bd, (0, 26, -6))
    ball(m, hd, (0, 28.0, -8.0), 3.4, flamef, layers=3)
    spike(m, hd, (0, 27.4, -11.0), (0, -0.1, -1), 1.6, 10.0, metal(P, "beak"), tip=0.8)
    m.round_box(hd, 0, -9.6, 3.0, 1.0, 26.6, 30.0, solid(P, "black"), cut=0)
    for sx in (-1, 1):
        ball(m, hd, (sx * 2.0, 28.6, -10.6), 0.8, solid(P, "orb", glow=True), layers=1)
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.8, 30.6, -6.0), ((j - 2) * 0.3, 1, 0.8), 1.2, 7.0, flamef, tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 4.0, 25.0, 0))
        feather_wing(m, wb, (sx * 4.0, 25.0, 0), 34.0, 14.0, 3, flamef, side=sx, sweep=30, droop=-6.0)
        lg = m.bone("leg_" + ("left" if sx > 0 else "right"), bd, (sx * 2.0, 15.0, 0))
        rod(m, lg, (sx * 2.0, 15.0, 0), (sx * 2.6, 8.0, -1.0), 1, solid(P, "black"), extend=0.3)
        for t in range(3):
            spike(m, lg, (sx * 2.6, 8.0, -1.0), ((t - 1) * 0.5, -0.6, -1), 0.9, 3.0, solid(P, "black"), tip=0.8)
    tl = m.bone("tail", bd, (0, 18, 6))
    for j in range(7):
        spike(m, tl, (0, 18.0, 6.0), ((j - 3) * 0.3, -0.4 + abs(j - 3) * 0.1, 1), 1.6, 18.0 - abs(j - 3) * 2.0, flamef,
              tip=0.8)
    for j in range(6):
        ball(m, tl, (-6.0 + j * 2.4, 12.0 + (j % 2) * 3.0, 22.0 + j), 0.8, solid(P, "spark", glow=True), layers=1)
    return m
