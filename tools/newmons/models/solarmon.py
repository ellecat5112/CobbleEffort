"""Solarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a living cogwheel: a big golden-orange gear with a riveted round face, one plain and one spiral
red-ringed eye and a jagged grin, flanked by two smaller spinning cogs. 1 block.

Front is -z, y is up. 24 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living golden-orange cogwheel with a riveted face, one spiral red eye, a jagged grin and two little spinning side cogs"
BASE = {"gold": (250, 190, 60), "gold_dark": (190, 110, 20), "orange": (240, 130, 40), "red": (210, 40, 40),
        "white": (250, 250, 250), "black": (30, 26, 24)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (120, 130, 160), "orange": (150, 170, 210)}


def P(v):
    return pal(BASE, SHINY, v)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.4, y - 15.0)
            if d < 1.6:
                if d < 0.5:
                    return tone(p["black"], face), None
                if sx > 0 and int(d * 3) % 2 == 0:
                    return tone(p["red"], face), None
                return tone(p["white"] if sx < 0 else p["orange"], face), None
        if abs(y - 11.4 - 0.6 * abs(math.sin(x * 1.6))) < 0.25 and abs(x) < 3.0:
            return tone(p["black"], face), None
    return metal(P, "orange", dark="gold_dark")(x, y, z, face, variant, box=box, **k)


def cog(m, bone, c, r, teeth, shader, depth):
    cx, cy, cz = c
    for i in range(teeth):
        ang = 2 * math.pi * i / teeth
        spike(m, bone, (cx + r * math.cos(ang), cy + r * math.sin(ang), cz), (math.cos(ang), math.sin(ang), 0), 1.8,
              r * 0.35 + 1.0, shader, tip=1.2)


def build():
    m = Model("solarmon")
    top = m.bone("solarmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for i in range(6):                                                                   # round gear disc
        t = -1 + (i + 0.5) / 3
        hw = 7.0 * math.sqrt(max(0.05, 1 - t * t))
        m.box(bd, -hw, 14.0 + 7.0 * (t - 1 / 6), -1.6, hw, 14.0 + 7.0 * (t + 1 / 6), 1.6, facef)
    cog(m, bd, (0, 14.0, 0), 7.0, 12, metal(P, "gold", dark="gold_dark"), 1.6)
    for sx in (-1, 1):                                                                   # little side cogs
        sb = m.bone("ring_cog_left" if sx > 0 else "ring_cog_right", bd, (sx * 10.0, 12.0, 0))
        m.box(sb, sx * 10.0 - 2.0, 10.0, -0.8, sx * 10.0 + 2.0, 14.0, 0.8, metal(P, "orange", dark="gold_dark"))
        cog(m, sb, (sx * 10.0, 12.0, 0), 2.4, 8, metal(P, "orange", dark="gold_dark"), 0.8)
    return m
