"""Reverse Weddinmon (a Digimon of the CobbleEffort: Digital crossover; built after the manga panel on wikimon.net, its
only picture): Weddinmon turned upside down: a great wedding cake hanging point-down, its tiers frilled with white
lace and studded with rosettes and bead-eyes, a laughing face set in the widest tier, flower-faced rosettes along
its rim and a tassel dangling from its tip. 25 blocks. Perfect stage (no level on wikimon; by analogy with
Weddinmon).

Front is -z, y is up. 48 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "an upside-down wedding cake hanging point-down, its tiers frilled with lace and rosettes, a laughing face in its widest tier"
BASE = {"cream": (250, 246, 236), "cream_dark": (210, 200, 180), "lace": (255, 255, 255), "pink": (240, 170, 190),
        "black": (30, 28, 30), "gold": (230, 190, 90), "mouth": (180, 50, 70)}
SHINY = {"cream": (60, 50, 60), "cream_dark": (30, 24, 30), "lace": (200, 60, 90), "pink": (60, 50, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def tierf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 38.0 < y < 46.0:
        for sx in (-1, 1):
            if math.hypot(x - sx * 4.0, y - 43.0) < 1.2:
                return tone(p["black"], face), None
        if 38.6 < y < 41.0 and abs(x) < 6.0 - (41.0 - y) * 1.5:
            return tone(p["mouth"], face), None
    if face not in ("up", "down") and (y % 4.0) < 0.6:
        return tone(p["lace"], face), None
    if face not in ("up", "down") and math.hypot(((x + z) % 3.0) - 1.5, (y % 4.0) - 2.2) < 0.4:
        return tone(p["black"], face), None
    return fabric(P, "cream", "cream_dark", axis="y", period=2.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("reverseweddinmon")
    top = m.bone("reverseweddinmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 24, 0))
    for i in range(6):                                                                   # inverted tiers
        r = 4.0 + i * 3.0
        m.round_box(bd, 0, 0, r, r, 8.0 + i * 6.0, 14.0 + i * 6.0, tierf, cut=max(1, round(r * 0.3)))
        m.round_box(bd, 0, 0, r + 0.6, r + 0.6, 13.4 + i * 6.0, 14.4 + i * 6.0, solid(P, "lace"), cut=max(1, round(r * 0.3)))
    for j in range(12):                                                                  # flower-faced rosettes
        ang = 2 * math.pi * j / 12
        c = (19.6 * math.cos(ang), 46.0, 19.6 * math.sin(ang))
        ball(m, bd, c, 1.8, solid(P, "pink"), layers=2)
    rod(m, bd, (0, 8.0, 0), (0, 2.0, 0), 1, solid(P, "gold"), extend=0.2)                   # tassel
    for j in range(5):
        ang = 2 * math.pi * j / 5
        spike(m, bd, (0, 2.0, 0), (0.3 * math.cos(ang), -1, 0.3 * math.sin(ang)), 0.8, 2.0, solid(P, "gold"), tip=0.8)
    return m
