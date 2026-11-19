"""Tobiumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a flying-fish dragon: a sleek silver-blue shark body with a pointed snout full of teeth and
yellow eyes, a ridge of fin spines, huge translucent pale-blue pectoral fin-wings ribbed like a flying fish, a forked
tail fin, a black band round its tail, and pale clawed legs with red talons. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import cutout, eye, metal, plane, scales, skin, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a sleek silver-blue flying-fish dragon with a toothy snout, huge translucent ribbed fin-wings and red-taloned legs"
BASE = {"silver": (180, 196, 214), "silver_dark": (100, 116, 140), "belly": (236, 240, 246), "fin": (170, 220, 250, 170),
        "rib": (90, 150, 200), "black": (40, 40, 46), "red": (200, 40, 40), "eye": (250, 220, 60), "pupil": (20, 10, 10),
        "white": (255, 255, 255), "mouth": (120, 20, 40), "tooth": (250, 250, 244)}
SHINY = {"silver": (230, 190, 120), "silver_dark": (160, 120, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and -17.0 < z < -14.0:
        c = eye(p, z + 15.4, y - 12.4, 0.9, "eye", slit=True)
        if c is not None:
            return c, None
    if 12.0 < z < 14.0:
        return tone(p["black"], face), None
    if face == "down" or y < 8.6:
        return tone(p["belly"], face), None
    return scales(P, "silver", "silver_dark", size=1.0)(x, y, z, face, variant, box=box, **k)


def finf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and face in ("up", "down"):
        u = (x - box.lo[0]) if box.size[0] else 0
        if (u + (z - box.lo[2]) * 0.6) % 3.0 < 0.5:
            return tone(p["rib"], face), None
    return p["fin"], None


def fin_in(x, y, z, face, box):
    if box is None:
        return True
    u = abs(x - (box.lo[0] if x > 0 else box.lo[0] + box.size[0])) / max(box.size[0], 1e-6)
    v = (z - box.lo[2]) / max(box.size[2], 1e-6)
    return v > u * 0.7 - 0.05


def build():
    m = Model("tobiumon")
    top = m.bone("tobiumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(10):
        z0 = -16.0 + i * 3.4
        t = i / 9
        r = max(1.8, 4.2 * math.sin(min(1.0, 0.25 + t * 0.9) * math.pi) + 0.8)
        slab_z(m, bd, 0, 10.0, z0, z0 + 3.6, r * 0.9, r, bodyf)
    hd = m.bone("head", bd, (0, 10, -16))
    spike(m, hd, (0, 10.6, -16.0), (0, -0.05, -1), 4.0, 6.0, bodyf, tip=0.8)
    m.box(hd, -2.2, 8.4, -21.0, 2.2, 9.6, -16.0, solid(P, "mouth"))
    for j in range(5):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.8, 9.6, -20.0 + j * 0.9), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    for j in range(6):                                                                 # fin spines
        spike(m, bd, (0, 14.0, -8.0 + j * 3.0), (0, 1, 0.5), 1.2, 3.0, solid(P, "silver_dark"), tip=0.8)
    for sx in (-1, 1):                                                                 # pectoral fin-wings
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.4, 11.0, -6.0))
        x0, x1 = sorted((sx * 3.4, sx * 26.0))
        m.box(wb, x0, 11.0, -8.0, x1, 11.0, 10.0, cutout(fin_in, finf), rotation=(0, sx * 14, sx * 8),
              pivot=(sx * 3.4, 11.0, -6.0))
    tl = m.bone("tail", bd, (0, 10, 16))                                               # forked tail fin
    for sy in (-1, 1):
        m.box(tl, -0.4, min(10.0, 10.0 + sy * 8.0), 17.0, 0.4, max(10.0, 10.0 + sy * 8.0), 22.0, solid(P, "fin"),
              rotation=(sy * -25, 0, 0), pivot=(0, 10.0, 17.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.4, 7.0, 2.0))
        rod(m, lg, (sx * 2.4, 7.0, 2.0), (sx * 3.4, 2.0, 0.0), 2, skin(P, "belly", dark="silver_dark"), extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 3.4, 1.6, -0.6), ((j - 1) * 0.4, -0.5, -1), 0.8, 2.2, solid(P, "red"), tip=0.8)
    return m
