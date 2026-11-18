"""Giga Seadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the armoured sea dragon: a long serpentine body coiled in loops, plated in gold and
violet armour with glowing cyan seams, a sharp-snouted helmed head with blade fins, rows of swept blade-fins along
its back and a forked blade tail. 35 blocks long.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a long serpentine sea dragon coiled in loops, plated in gold and violet armour with glowing cyan seams, a "
        "helmed head with blade fins and swept blade-fins along its back")
BASE = {"gold": (230, 180, 80), "gold_dark": (150, 100, 30), "gold_light": (255, 230, 150), "violet": (90, 80, 170),
        "violet_dark": (40, 34, 100), "cyan": (100, 230, 255), "blade": (220, 224, 240), "blade_dark": (120, 124, 140),
        "eye": (250, 60, 80), "red": (200, 30, 50)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (120, 130, 150), "gold_light": (250, 250, 255), "violet": (170, 40, 60)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD0 = armour(P, "gold", "gold_dark", light="gold_light", trim="violet", trim_w=0.35)
BLADE = metal(P, "blade", dark="blade_dark")


def goldf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "east", "west") and abs((z * 0.5 + x * 0.5) % 3.0 - 1.5) < 0.1:
        return p["cyan"], p["cyan"]
    return GOLD0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gigaseadramon")
    top = m.bone("gigaseadramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    pts = []
    for i in range(30):                                                               # coiled serpentine body
        t = i / 29
        ang = t * 3.6 * math.pi
        r = 12.0 - 4.0 * t
        pts.append((r * math.cos(ang), 6.0 + 18.0 * (1 - t) + 4.0 * math.sin(ang * 0.5), r * math.sin(ang) + 4.0))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, max(2, 5 - j // 8), goldf, extend=0.6)
        if j % 3 == 0:
            spike(m, bd, p0, (0, 1, 0.6), 1.2, 4.0, BLADE, tip=0.8)                     # back blade-fins
    tail = pts[-1]
    for sy in (-1, 1):
        spike(m, bd, tail, (0.4, sy * 0.4, 1), 1.6, 6.0, BLADE, tip=0.8)                # forked blade tail
    hd = m.bone("head", bd, pts[0])
    h = pts[0]
    m.round_box(hd, h[0], h[2] - 4.0, 3.0, 6.0, h[1] - 1.0, h[1] + 4.0, goldf, cut=1)
    spike(m, hd, (h[0], h[1] + 1.0, h[2] - 10.0), (0, -0.1, -1), 2.4, 6.0, goldf, tip=0.9)   # sharp snout
    for sx in (-1, 1):
        m.box(hd, h[0] + sx * 3.0 - (0.3 if sx > 0 else -0.0), h[1] + 2.0, h[2] - 6.0,
              h[0] + sx * 3.0 + (0.0 if sx > 0 else 0.3), h[1] + 3.0, h[2] - 4.0, solid(P, "eye", glow=True))
        spike(m, hd, (h[0] + sx * 2.6, h[1] + 3.0, h[2] - 1.0), (sx * 0.6, 0.6, 1), 1.6, 8.0, BLADE, tip=0.8)
    spike(m, hd, (h[0], h[1] + 4.0, h[2] - 3.0), (0, 0.8, 1), 1.6, 7.0, BLADE, tip=0.8)
    return m
