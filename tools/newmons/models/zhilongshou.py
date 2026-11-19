"""Zhilongshou (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after an anime still
on wikimon.net): a young golden dragon of the Shou: a long cream-bellied serpentine body coiled like an S, a shaggy
orange mane, a golden dragon head with big dark eyes and long whiskers, small clawed forelegs and a tufted orange tail.
15 blocks.

Front is -z, y is up. Adult stage (by analogy: wikimon gives no level).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fur, scales, skin, solid
from _route import pal, tone

HEIGHT = 37
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a young golden serpentine dragon coiled like an S, with a shaggy orange mane, big dark eyes, long whiskers and a tufted tail"
BASE = {"gold": (230, 180, 70), "gold_dark": (170, 110, 30), "cream": (246, 236, 210), "orange": (240, 140, 50),
        "orange_dark": (170, 80, 20), "eye": (40, 40, 90), "pupil": (10, 10, 20), "white": (255, 255, 255),
        "claw": (240, 230, 210)}
SHINY = {"gold": (150, 200, 120), "gold_dark": (80, 130, 50), "orange": (90, 170, 220), "orange_dark": (40, 110, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" or face == "down":
        return skin(P, "cream", dark="gold_dark")(x, y, z, face, variant, box=box, **k)
    return scales(P, "gold", "gold_dark", size=1.0)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 6.0, y - 33.0, 1.2, "eye")
        if c is not None:
            return c, None
    return skin(P, "gold", dark="gold_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("zhilongshou")
    top = m.bone("zhilongshou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    pts = []
    for i in range(14):                                                                 # S-shaped coil
        t = i / 13
        pts.append((6.0 * math.sin(t * 2 * math.pi), 4.0 + t * 26.0, 2.0 * math.cos(t * 2 * math.pi)))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, max(2, 3 - i // 6), bodyf, extend=0.6)
    for j in range(4):
        spike(m, bd, pts[0], ((j - 1.5) * 0.4, -1, 0.3), 1.6, 5.0, fur(P, "orange", "orange_dark"), tip=0.8)
    hd = m.bone("head", bd, pts[-1])
    m.round_box(hd, 0, -4.0, 3.0, 4.0, 30.0, 36.0, headf, cut=1)
    for j in range(9):                                                                  # shaggy mane
        ang = (j - 4) * 0.4
        spike(m, hd, (math.sin(ang) * 3.0, 34.0, -1.0), (math.sin(ang), 0.6, 0.8), 1.8, 6.0,
              fur(P, "orange", "orange_dark"), tip=0.8)
    for sx in (-1, 1):
        pts2 = [(sx * 1.6, 31.0, -8.0), (sx * 5.0, 30.0, -9.0), (sx * 7.0, 27.0, -7.0)]
        for p0, p1 in zip(pts2, pts2[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "orange_dark"), extend=0.2)
        lg = m.bone("arm_" + ("left" if sx > 0 else "right"), bd, (sx * 2.0, 26.0, -2.0))
        rod(m, lg, (sx * 2.0, 26.0, -2.0), (sx * 5.0, 22.0, -4.0), 1, bodyf, extend=0.3)
        for t in range(3):
            spike(m, lg, (sx * 5.0, 22.0, -4.0), ((t - 1) * 0.5, -0.6, -1), 0.8, 1.6, solid(P, "claw"), tip=0.8)
    return m
