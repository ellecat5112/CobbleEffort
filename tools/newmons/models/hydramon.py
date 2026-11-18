"""Hydramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the plant hydra: a great mass of twisted green vines and bark rising from a tangle of roots, three
serpentine plant heads with fanged red maws, leafy frills and glowing yellow eyes, thorny tendrils and a crown of
leaves along its back. 35 blocks tall.

Front is -z, y is up. 44 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, local, skin, solid, twisted
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
LOOK = "a great mass of twisted green vines on tangled roots with three fanged serpentine plant heads, leafy frills and thorns"
BASE = {"green": (70, 140, 50), "green_dark": (24, 70, 20), "green_light": (150, 210, 100), "bark": (110, 80, 50),
        "bark_dark": (60, 40, 24), "leaf": (90, 190, 70), "leaf_dark": (40, 110, 30), "red": (200, 40, 50),
        "tooth": (246, 240, 220), "eye": (250, 230, 60), "thorn": (230, 210, 150)}
SHINY = {"green": (150, 70, 140), "green_dark": (70, 20, 70), "green_light": (220, 150, 210), "leaf": (230, 120, 180),
         "leaf_dark": (150, 50, 110)}


def P(v):
    return pal(BASE, SHINY, v)


VINE = twisted(P, "green", "green_dark", light="green_light")
BARK = twisted(P, "bark", "bark_dark", period=1.6)


def leaf_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6)
    return abs(a) < 0.5 * math.sin(math.pi * min(1.0, b)) + 0.02


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["leaf_dark"] if abs(u / max(W, 1e-6) - 0.5) < 0.06 else p["leaf"], face), None


LEAF = cutout(leaf_in, leaff)


def head(m, bone, c):
    x, y, z = c
    m.round_box(bone, x, z, 2.6, 4.0, y - 1.6, y + 2.4, VINE, cut=1)
    m.round_box(bone, x, z - 4.6, 2.0, 2.6, y - 0.8, y + 1.6, VINE, cut=1)
    m.round_box(bone, x, z - 4.0, 2.0, 3.0, y - 3.4, y - 1.6, VINE, cut=1)
    m.round_box(bone, x, z - 4.4, 1.6, 2.4, y - 1.8, y - 0.8, solid(P, "red"), cut=0)
    for sx in (-1, 1):
        m.box(bone, min(x + sx * 2.4, x + sx * 2.8), y + 0.6, z - 2.4, max(x + sx * 2.4, x + sx * 2.8), y + 1.6, z - 1.0,
              solid(P, "eye", glow=True))
        for j in range(3):
            spike(m, bone, (x + sx * (0.6 + j * 0.5), y - 0.8, z - 6.6 + j * 1.2), (0, -1, 0), 0.8, 1.6,
                  solid(P, "tooth"), tip=0.8)
    for i in range(5):                                                              # leafy frill
        ang = math.radians(-70 + i * 35)
        m.box(bone, x - 1.6, y + 1.0, z + 2.0, x + 1.6, y + 7.0, z + 2.0, LEAF,
              rotation=(-30, 0, -math.degrees(ang) * 0.9), pivot=(x, y + 1.0, z + 2.0))


def build():
    m = Model("hydramon")
    top = m.bone("hydramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(10):                                                             # tangled roots
        ang = 2 * math.pi * i / 10 + 0.2
        rod(m, top, (3.0 * math.cos(ang), 8.0, 3.0 * math.sin(ang)), (13.0 * math.cos(ang), 0.6, 12.0 * math.sin(ang)),
            2, BARK, extend=0.6)
    for j, (r, y0, y1) in enumerate(((9.0, 6.0, 14.0), (10.0, 13.0, 22.0), (8.4, 21.0, 28.0))):   # vine mass
        m.round_box(bd, 0, 1.0, r, r * 0.8, y0, y1, VINE, cut=max(1, int(r * 0.3)))
    for i in range(7):
        ang = math.radians(-60 + i * 20)
        rod(m, bd, (7.0 * math.sin(ang), 12.0, -6.0 * math.cos(ang)), (8.6 * math.sin(ang), 25.0, -5.0 * math.cos(ang)),
            1, BARK, extend=0.4)
    for i in range(6):                                                              # leaf crown along the back
        m.box(bd, -2.0, 27.0, -4.0 + i * 2.4, 2.0, 34.0, -4.0 + i * 2.4, LEAF, rotation=(-20, 0, (i - 2.5) * 12),
              pivot=(0, 27.0, -4.0 + i * 2.4))
    for k, (sx, nm) in enumerate(((0, "head"), (1, "neck_left"), (-1, "neck_right"))):    # three heads
        nb = m.bone(nm, bd, (sx * 5.0, 26.0, -4.0))
        pts = [(sx * 5.0, 26.0, -4.0), (sx * 9.0, 32.0, -9.0), (sx * 10.0, 38.0 - abs(sx) * 2, -12.0),
               (sx * 9.0, 40.0 - abs(sx) * 2, -15.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, nb, p0, p1, 3, VINE, extend=0.8)
        for p in pts[1:3]:
            spike(m, nb, p, (sx * 0.5, 0.4, 0.8), 0.9, 2.6, solid(P, "thorn"), tip=0.8)
        head(m, nb, (sx * 9.0, 40.0 - abs(sx) * 2, -17.0))
    for sx in (-1, 1):                                                              # thorny tendrils
        pts = [(sx * 8.0, 18.0, -4.0), (sx * 14.0, 16.0, -9.0), (sx * 17.0, 10.0, -12.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, VINE, extend=0.3, t2=2)
            spike(m, bd, p1, (sx, 0.5, -0.4), 0.9, 2.0, solid(P, "thorn"), tip=0.8)
    return m
