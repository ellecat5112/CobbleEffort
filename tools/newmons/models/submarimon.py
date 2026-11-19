"""Submarimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of reliability: a silver submarine-fish with a long spiralled sawfish-drill
nose, a clear blue glass cockpit canopy, yellow flame-fin cheek marks, a green eye, a violet underside, swept white
fins and a tall dorsal fin. 15 blocks.

Front is -z, y is up. 24 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a silver submarine-fish with a long spiralled drill nose, a blue glass canopy, yellow fin marks, a green eye and swept white fins"
BASE = {"silver": (220, 224, 236), "silver_dark": (120, 124, 140), "violet": (80, 60, 140), "glass": (120, 190, 250, 180),
        "yellow": (250, 220, 60), "green": (90, 200, 120), "white": (246, 248, 252), "steel": (190, 194, 206)}
SHINY = {"silver": (250, 200, 110), "silver_dark": (180, 120, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def hullf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "down" or y < 9.0:
        return tone(p["violet"], face), None
    return armour(P, "silver", "silver_dark")(x, y, z, face, variant, box=box, **k)


def drillf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["steel"] if (z * 1.4 + math.atan2(y - 12.0, x) * 0.6) % 1.6 < 0.9 else p["silver_dark"], face), None


def build():
    m = Model("submarimon")
    top = m.bone("submarimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(8):
        t = (i + 0.5) / 8
        r = 5.0 * math.sin(math.pi * (0.25 + 0.7 * t)) + 0.8
        slab_z(m, bd, 0, 12.0, -10.0 + i * 3.4, -10.0 + (i + 1) * 3.4 + 0.2, r, r * 0.9, hullf)
    spike(m, bd, (0, 12.0, -11.0), (0, 0, -1), 2.4, 14.0, drillf, tip=0.8)                  # drill nose
    ball(m, bd, (0, 17.0, -2.0), 3.0, solid(P, "glass"), layers=2, squash=1.6)             # glass canopy
    for sx in (-1, 1):
        m.box(bd, min(sx * 4.6, sx * 4.9), 12.0, -8.0, max(sx * 4.6, sx * 4.9), 14.0, -6.0, solid(P, "green"))
        for j in range(3):
            spike(m, bd, (sx * 4.6, 12.0, -4.0 + j), (sx * 0.4, 0.6 - j * 0.3, 1), 0.8, 3.0, solid(P, "yellow"), tip=0.8)
        spike(m, bd, (sx * 4.0, 10.0, 4.0), (sx * 1, -0.3, 0.6), 1.6, 8.0, solid(P, "white"), tip=0.8)   # swept fins
    spike(m, bd, (0, 17.0, 6.0), (0, 1, 0.6), 2.0, 7.0, solid(P, "white"), tip=0.8)          # dorsal fin
    for sx in (-1, 1):
        spike(m, bd, (0, 12.0, 16.0), (0, sx * 0.8, 0.6), 1.6, 6.0, solid(P, "white"), tip=0.8)
    return m
