"""Lampmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
genie of the lamp: a burly green genie with arms folded, a tall violet turban with a jewel, red eyes and pointed ears,
a black goatee, gold armlets, a gold spike on each shoulder, a violet sash, and a body that tapers into a swirl of
blue smoke pouring from a golden oil lamp. 35 blocks tall.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, gem, metal, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a burly green genie with folded arms, a violet turban, a black goatee, gold armlets and a smoky tail rising from a golden lamp"
BASE = {"green": (90, 170, 80), "green_dark": (40, 100, 30), "green_light": (170, 230, 150), "violet": (110, 80, 170),
        "violet_dark": (50, 30, 100), "gold": (240, 200, 60), "gold_dark": (160, 120, 20), "black": (30, 28, 30),
        "eye": (230, 40, 40), "smoke": (130, 160, 230, 200), "smoke_light": (210, 225, 255, 220), "gem": (220, 40, 60),
        "gem_light": (255, 170, 180)}
SHINY = {"green": (80, 120, 210), "green_dark": (30, 50, 150), "green_light": (160, 190, 250)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "green", dark="green_dark", light="green_light")
GOLD = metal(P, "gold", dark="gold_dark")


def smokef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return (p["smoke_light"] if (y * 0.8 + x) % 3.0 < 1.0 else p["smoke"]), None


def build():
    m = Model("lampmon")
    top = m.bone("lampmon", None, (0, 0, 0))
    lb = m.bone("lamp", top, (0, 2, 0))                                              # golden lamp
    m.round_box(lb, 0, 0, 4.0, 2.6, 0.0, 4.0, GOLD, cut=1)
    spike(m, lb, (0, 2.0, -2.6), (0, 0.5, -1), 1.4, 5.0, GOLD, tip=0.8)
    m.round_box(lb, 0, 0, 1.4, 1.4, 4.0, 5.6, GOLD, cut=0)
    pts = [(0, 5.0, 0), (2.0, 9.0, 2.0), (-1.0, 13.0, 1.0), (1.0, 18.0, 0), (0, 22.0, 0)]   # smoke tail
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, lb, p0, p1, 1 + j, smokef, extend=0.6)
    bd = m.bone("body", top, (0, 22, 0))
    m.round_box(bd, 0, 0.6, 7.0, 5.0, 20.0, 36.0, SKIN, cut=2)
    m.round_box(bd, 0, 0.6, 7.2, 5.2, 20.0, 23.0, fabric(P, "violet", "violet_dark"), cut=2)   # sash
    for sx in (-1, 1):                                                               # shoulders + spikes
        m.round_box(bd, sx * 8.0, 0.6, 3.4, 3.6, 31.0, 37.0, SKIN, cut=1)
        spike(m, bd, (sx * 9.0, 36.0, 0.6), (sx * 0.4, 1, 0), 1.6, 4.0, GOLD, tip=0.8)
    ab = m.bone("arm_left", bd, (0, 30, -6))                                         # folded arms
    m.round_box(ab, 0, -6.2, 8.0, 1.8, 26.0, 29.6, SKIN, cut=1)
    m.round_box(ab, 0, -6.2, 8.2, 2.0, 26.6, 28.4, GOLD, cut=1)                         # armlets
    hd = m.bone("head", bd, (0, 36, 0))
    m.round_box(hd, 0, -0.6, 3.6, 3.6, 36.0, 44.0, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 40.6, -4.3, max(sx * 0.8, sx * 2.2), 41.4, -4.1, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 3.6, 41.0, 0), (sx, 0.4, 0.2), 1.0, 2.6, SKIN, tip=0.8)
    spike(m, hd, (0, 37.0, -3.8), (0, -1, -0.4), 1.6, 4.0, solid(P, "black"), tip=0.8)        # goatee
    for j, (r, y0) in enumerate(((4.4, 43.0), (4.0, 45.4), (3.0, 47.6), (1.6, 49.4))):        # violet turban
        m.round_box(hd, 0, -0.2, r, r, y0, y0 + 2.6, fabric(P, "violet", "violet_dark"), cut=max(1, int(r * 0.4)))
    m.round_box(hd, 0, -4.6, 1.0, 0.4, 44.0, 46.0, gem(P, "gem", "gem_light"), cut=0)
    return m
