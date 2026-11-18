"""Rare Star Sword (a Digimon of the CobbleEffort: Digital crossover; built after the anime still on wikimon.net, its
only picture): a living blade: a golden five-pointed star for a guard with a ring at its heart, and a long jagged blade
of blazing orange-red flame. 1 block. Child stage (no level on wikimon; by analogy).

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.0)
KIND = "floater"
K = 3
LOOK = "a living blade: a golden five-pointed star guard with a ring at its heart and a long jagged blade of blazing flame"
BASE = {"gold": (250, 220, 60), "gold_dark": (190, 150, 20), "steel": (220, 224, 236), "flame": (250, 120, 30),
        "flame_core": (255, 210, 80), "red": (220, 50, 30)}
SHINY = {"gold": (200, 220, 250), "gold_dark": (120, 150, 210), "flame": (90, 160, 250), "flame_core": (190, 230, 255),
         "red": (60, 90, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["flame_core"] if abs(x) < 0.8 else (p["flame"] if abs(x) < 2.0 else p["red"])
    return c, c


def build():
    m = Model("rarestarsword")
    top = m.bone("rarestarsword", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    for j in range(5):                                                                   # star guard
        ang = math.radians(90 + j * 72)
        spike(m, bd, (0, 24.0, 0), (math.cos(ang), math.sin(ang), 0), 2.6, 5.0, metal(P, "gold", dark="gold_dark"),
              tip=0.8)
    m.round_box(bd, 0, 0, 2.0, 1.2, 23.0, 25.0, metal(P, "gold", dark="gold_dark"), cut=0)
    m.round_box(bd, 0, 0, 1.0, 1.4, 23.6, 24.4, metal(P, "steel"), cut=0)
    for j in range(8):                                                                   # jagged flame blade
        w = 3.0 - j * 0.3
        y0 = 18.0 - j * 2.2
        m.box(bd, -w * 0.6, y0, -0.6, w * 0.6, y0 + 2.4, 0.6, flamef)
        spike(m, bd, ((1 if j % 2 else -1) * w * 0.5, y0 + 1.2, 0), ((1 if j % 2 else -1), 0.5, 0), 1.0, 2.4, flamef,
              tip=0.8)
    spike(m, bd, (0, 2.4, 0), (0, -1, 0), 1.6, 2.4, flamef, tip=0.8)
    return m
