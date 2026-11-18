"""Rare Raremon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a towering trunk of green rotting sludge sprouting snarling reptile heads from its
flanks, crowned by a huge black armoured mask set with many small red eyes and a grinning row of teeth, spiked steel
studs and cables sunk in its flesh, all oozing down into root-like tendrils and webbed feet; dark smoke drifts round
it. 25 blocks.

Front is -z, y is up. 52 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 52
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a towering trunk of green rotting sludge sprouting reptile heads, crowned by a huge black mask of many red eyes"
BASE = {"green": (120, 150, 70), "green_dark": (60, 80, 30), "black": (36, 34, 44), "black_dark": (12, 12, 16),
        "eye": (230, 40, 40), "tooth": (236, 230, 210), "steel": (150, 154, 166), "steel_dark": (70, 74, 86),
        "mouth": (130, 20, 40), "smoke": (90, 90, 96, 150)}
SHINY = {"green": (150, 110, 170), "green_dark": (80, 50, 100)}


def P(v):
    return pal(BASE, SHINY, v)


SLUDGE = skin(P, "green", dark="green_dark", var=0.08)
STEEL = metal(P, "steel", dark="steel_dark")


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for ex, ey in ((-2.0, 46.0), (2.0, 46.0), (-3.4, 43.6), (3.4, 43.6), (0, 44.0), (-1.4, 41.6), (1.4, 41.6)):
            if math.hypot(x - ex, y - ey) < 0.55:
                return p["eye"], p["eye"]
        if 37.0 < y < 39.6 and abs(x) < 4.0:
            return tone(p["tooth"] if (x * 1.4) % 1.2 > 0.2 else p["black_dark"], face), None
    return armour(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)


def snake_head(m, bone, c, d, s=1.0):
    cx, cy, cz = c
    m.round_box(bone, cx + d * 3.0 * s, cz - 1.0, 3.6 * s, 2.4 * s, cy - 2.0 * s, cy + 2.0 * s, SLUDGE, cut=1)
    m.box(bone, min(cx + d * 3.0 * s, cx + d * 7.4 * s), cy - 1.0 * s, cz - 3.0 * s,
          max(cx + d * 3.0 * s, cx + d * 7.4 * s), cy - 0.2 * s, cz + 1.0 * s, solid(P, "mouth"))
    for j in range(3):
        spike(m, bone, (cx + d * (4.0 + j * 1.2) * s, cy - 0.2 * s, cz - 2.0 * s), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"),
              tip=0.8)


def build():
    m = Model("rareraremon")
    top = m.bone("rareraremon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(8):                                                                   # sludge trunk
        r = 7.0 + 1.6 * math.sin(i * 0.9)
        m.round_box(bd, 0.4 * math.sin(i), 0, r, r * 0.85, 6.0 + i * 4.0, 10.6 + i * 4.0, SLUDGE, cut=2)
    for j in range(6):                                                                   # root tendrils
        ang = 2 * math.pi * j / 6
        rod(m, bd, (5.0 * math.cos(ang), 8.0, 5.0 * math.sin(ang)), (11.0 * math.cos(ang), 1.0, 11.0 * math.sin(ang)),
            2, SLUDGE, extend=0.4)
    hd = m.bone("head", bd, (0, 40, 0))
    m.round_box(hd, 0, -1.0, 6.0, 6.0, 36.0, 52.0, maskf, cut=2)                            # black mask
    for j in range(6):
        spike(m, hd, (-5.0 + j * 2.0, 51.0, 0), ((j - 2.5) * 0.15, 1, 0.2), 1.0, 3.0, STEEL, tip=0.8)
    for sx, y, s in ((1, 30.0, 1.0), (-1, 26.0, 1.2), (1, 18.0, 0.9), (-1, 36.0, 0.8)):
        snake_head(m, bd, (sx * 6.0, y, -2.0), sx, s)
    for j in range(5):                                                                   # steel studs
        ang = j * 1.3
        spike(m, bd, (7.4 * math.cos(ang), 14.0 + j * 4.6, 6.0 * math.sin(ang)), (math.cos(ang), 0.2, math.sin(ang)),
              1.0, 2.4, STEEL, tip=0.8)
    for c in ((-10.0, 44.0, 4.0), (10.0, 40.0, 6.0), (-8.0, 30.0, 8.0)):                 # dark smoke
        ball(m, bd, c, 3.0, solid(P, "smoke"), layers=2)
    return m
