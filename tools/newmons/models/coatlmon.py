"""Coatlmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the feathered serpent. A long white serpent banded in red with gold Aztec-style patterns, a white
helmeted head with a green feather crest, great white feathered wings at its neck, and a gold flame-shaped ornament
at the tip of its coiled tail. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage (Armor; floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import feathers, metal, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "floater"
K = 3
LOOK = ("a long white serpent banded in red with gold patterns, a helmeted head with a green feather crest, great "
        "white feathered wings and a gold flame ornament on its tail")
BASE = {"white": (240, 240, 244), "white_dark": (180, 184, 196), "red": (200, 40, 40), "gold": (230, 190, 70),
        "gold_dark": (160, 120, 20), "green": (60, 160, 70), "green_dark": (24, 100, 40), "eye": (250, 210, 50),
        "pupil": (30, 20, 10), "wing": (246, 246, 250), "wing_dark": (190, 194, 210)}
SHINY = {"white": (40, 44, 56), "white_dark": (16, 18, 24), "red": (220, 190, 60), "green": (200, 60, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (x * 0.4 + y * 0.6 + z * 0.5) % 5.0
    if t < 0.9:
        return tone(p["red"], face), None
    if 1.4 < t < 1.8 or (t > 3.0 and abs((x + z) % 2.0 - 1.0) < 0.2):
        return tone(p["gold"], face), None
    return skin(P, "white", dark="white_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("coatlmon")
    top = m.bone("coatlmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    pts = [(0, 44.0, -6.0), (0, 38.0, -4.0), (3.0, 32.0, -1.0), (5.0, 26.0, 2.0), (3.0, 20.0, 5.0), (-2.0, 16.0, 5.0),
           (-5.0, 12.0, 2.0), (-3.0, 8.0, -2.0), (2.0, 6.0, -3.0), (6.0, 4.0, 0.0), (5.0, 3.0, 5.0), (0.0, 3.0, 8.0),
           (-5.0, 4.0, 9.0)]
    bones = [bd]
    for j in range(1, 4):
        bones.append(m.bone(f"coil_{j}", bones[-1], pts[j * 3]))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        r = 2.8 - i * 0.14
        rod(m, bones[min(3, i // 3)], p0, p1, max(2, round(2 * r)), bandf, extend=0.6)
    e = pts[-1]                                                                   # gold flame tail ornament
    for j, d in enumerate(((-1, 0.5, 0.2), (-1, 0, 0.6), (-1, -0.4, 0.2), (-0.6, 0.9, 0.3))):
        spike(m, bones[-1], e, d, 1.4, 3.0 + (j % 2), metal(P, "gold", dark="gold_dark"), tip=0.4)
    hd = m.bone("head", bd, pts[0])
    m.round_box(hd, 0, -7.0, 3.0, 3.4, 42.0, 47.0, bandf, cut=1)
    m.box(hd, -2.2, 42.4, -13.0, 2.2, 45.0, -9.0, bandf)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.8, sx * 3.2), 45.0, -9.6, max(sx * 2.8, sx * 3.2), 46.0, -8.4, solid(P, "eye", glow=True))
    for i in range(9):                                                            # green feather crest
        spike(m, hd, ((i - 4) * 0.6, 46.6, -6.0 + abs(i - 4) * 0.4), ((i - 4) * 0.15, 1, 0.6), 1.2,
              5.0 - abs(i - 4) * 0.4, feathers(P, "green", "green_dark", size=(0.8, 1.6)), tip=0.4)
    wb = m.bone("wings", bd, (0, 38, -3))                                         # great white wings
    WING = feathers(P, "wing", "wing_dark", size=(1.4, 3.0), flow=(0, 1))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.0, sx * 20.0))
        for j, ang in enumerate((40, 15)):
            m.box(wb, x0, 36.0, -2.0 + j, x1, 42.0, -2.0 + j, WING, rotation=(0, sx * 20, sx * ang),
                  pivot=(sx * 2.0, 39.0, -2.0 + j))
    return m
