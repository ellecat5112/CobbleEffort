"""Leafmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a Baby I
pale-green bean-shaped blob with two little nub ears, round black eyes and a pink bubble at its mouth, sheltering
under a big leaf on a curving green stalk. A third of a block tall.

Front is -z, y is up. 14 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, local, skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = "a pale-green bean blob with nub ears, round black eyes and a pink bubble, under a big leaf on a curving stalk"
BASE = {"green": (200, 236, 170), "green_dark": (140, 190, 110), "leaf": (130, 200, 110), "leaf_dark": (60, 130, 60),
        "eye": (20, 20, 24), "pink": (250, 170, 190)}
SHINY = {"green": (250, 230, 160), "green_dark": (210, 180, 100), "leaf": (230, 150, 80)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 4.4) < 0.7:
                return tone(p["eye"], face), None
    return skin(P, "green", dark="green_dark")(x, y, z, face, variant, box=box, **k)


def leaf_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    return a * a / 0.25 + b * b / 0.25 < 1.0


def build():
    m = Model("leafmon")
    top = m.bone("leafmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 4.0, 0), 4.0, bodyf, layers=3, squash=0.85)
    m.round_box(bd, -2.6, -3.6, 1.0, 0.8, 2.0, 4.0, solid(P, "pink"), cut=0)
    for sx in (-1, 1):
        spike(m, bd, (sx * 2.4, 7.0, 0), (sx * 0.5, 1, 0), 1.2, 1.6, skin(P, "green", dark="green_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 7, 2))
    pts = [(1.0, 6.0, 3.6), (3.0, 10.0, 4.0), (2.0, 13.0, 2.0)]                         # curving stalk
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 1, skin(P, "leaf", dark="leaf_dark"), extend=0.2, t2=1)
    m.box(hd, -4.0, 13.0, -5.0, 4.0, 13.0, 5.0, cutout(leaf_in, skin(P, "leaf", dark="leaf_dark")),
          rotation=(-15, 0, 10), pivot=(0, 13.0, 0))
    return m
