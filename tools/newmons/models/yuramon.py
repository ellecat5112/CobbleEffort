"""Yuramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a drifting seed puff: a round ball of pale cream fluff fibres with a violet face-patch and two big black
eyes, and long violet ribbon tendrils curling up from its top. 0.35 blocks.

Front is -z, y is up. Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, plane, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.35, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = "a drifting seed puff of cream fluff with a violet face-patch, two big black eyes and long violet ribbon tendrils"
BASE = {"cream": (250, 240, 200), "cream_dark": (200, 180, 130), "violet": (130, 110, 200), "eye": (20, 20, 26),
        "white": (255, 255, 255)}
SHINY = {"cream": (210, 240, 220), "cream_dark": (140, 190, 160), "violet": (220, 110, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if abs(a) < 4.0 and abs(b - 7.0) < 2.0:
            for sx in (-1, 1):
                d = math.hypot(a - sx * 1.8, b - 7.0)
                if d < 1.2:
                    return (p["white"] if math.hypot(a - sx * 1.8 + 0.4, b - 7.4) < 0.35 else p["eye"]), None
            return tone(p["violet"], face), None
    return fur(P, "cream", "cream_dark", length=1.4)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yuramon")
    top = m.bone("yuramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 7.0, 0), 5.4, bodyf, layers=5)
    for j in range(8):                                                                  # fluff fibres
        ang = j * 2 * math.pi / 8
        spike(m, bd, (4.6 * math.cos(ang), 7.0 + 4.6 * math.sin(ang), 1.0), (math.cos(ang), math.sin(ang), 0.2), 1.0,
              2.0, fur(P, "cream", "cream_dark"), tip=0.8)
    for sx in (-1, 1):                                                                  # ribbon tendrils
        pts = [(sx * 1.6, 12.0, 0), (sx * 3.0, 15.0, 0.4), (sx * 5.0, 17.0, 0.4), (sx * 7.0, 15.6, 0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, solid(P, "violet"), extend=0.2, t2=2)
    return m
