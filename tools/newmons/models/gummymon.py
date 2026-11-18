"""Gummymon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Baby II drop of pale mint jelly with a pointed horn, two long floppy ears, big black eyes and a happy fanged smile,
its base spreading in soft lobes. Half a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a drop of pale mint jelly with a pointed horn, long floppy ears, big black eyes and a happy fanged smile"
BASE = {"mint": (220, 245, 210), "mint_dark": (170, 210, 160), "eye": (24, 22, 28), "shine": (250, 250, 250),
        "mouth": (200, 50, 60), "tooth": (250, 250, 250), "black": (30, 28, 32)}
SHINY = {"mint": (250, 220, 240), "mint_dark": (220, 170, 200)}


def P(v):
    return pal(BASE, SHINY, v)


MINT = skin(P, "mint", dark="mint_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 9.0)
            if d < 0.35:
                return tone(p["shine"], face), None
            if d < 1.0:
                return tone(p["eye"], face), None
        if abs(y - 6.0 - 0.15 * x * x) < 0.5 and abs(x) < 1.6:
            return tone(p["mouth"], face), None
    return MINT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gummymon")
    top = m.bone("gummymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0, 5.0, 4.0, 0.0, 12.0, bodyf, cut=2)
    for j in range(4):                                                            # soft lobes
        ang = math.pi * (0.1 + 0.8 * j / 3)
        m.round_box(bd, 5.0 * math.cos(ang) * 1.0, -3.0 * math.sin(ang) * 0.4, 1.8, 1.8, 0.0, 2.4, MINT, cut=1)
    hd = m.bone("head", bd, (0, 12, 0))
    spike(m, hd, (0, 12.0, 0), (0, 1, 0.1), 2.0, 4.0, MINT, tip=0.8)
    spike(m, hd, (0, 14.6, 0.3), (0, 1, 0.1), 1.0, 1.4, solid(P, "black"))
    for sx in (-1, 1):                                                            # long floppy ears
        rod(m, hd, (sx * 4.0, 11.0, 0.4), (sx * 9.0, 10.0, 1.0), 1, MINT, extend=0.3, t2=3)
        rod(m, hd, (sx * 9.0, 10.0, 1.0), (sx * 10.6, 8.0, 1.0), 1, MINT, extend=0.3, t2=2)
    return m
