"""Shoemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little cream mouse-puppet with a red patch stitched over one eye and a pointed red cap, peeking out of
a big patched orange boot with a green eye on its toe, a white sticking plaster across it, a dark tread sole, and a
long sewing needle held like a lance. 1 block.

Front is -z, y is up. 26 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, leather, metal, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = "a little cream mouse-puppet in a pointed red cap peeking out of a big patched orange boot with a green eye, holding a sewing needle"
BASE = {"cream": (250, 240, 190), "cream_dark": (210, 190, 130), "red": (220, 60, 40), "red_dark": (130, 20, 14),
        "orange": (240, 130, 40), "orange_dark": (170, 70, 10), "green": (60, 180, 120), "black": (30, 26, 30),
        "white": (250, 250, 246), "sole": (60, 60, 80), "steel": (210, 214, 226)}
SHINY = {"orange": (90, 150, 220), "orange_dark": (30, 80, 160), "red": (240, 190, 50), "red_dark": (170, 120, 10)}


def P(v):
    return pal(BASE, SHINY, v)


BOOT = leather(P, "orange", "orange_dark", stitch="black")


def bootf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x - 0.0) < 2.2 and 3.0 < y < 5.0 and abs((x + y) % 2.0 - 1.0) < 0.6:
        return tone(p["white"], face), None
    if face in ("north", "east") and math.hypot(x - 2.6, y - 6.0) < 1.4:
        return tone(p["green"] if math.hypot(x - 2.6, y - 6.0) > 0.6 else p["black"], face), None
    return BOOT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("shoemon")
    top = m.bone("shoemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.box(bd, -5.0, 0.0, -8.0, 5.0, 2.0, 6.0, solid(P, "sole"))                              # tread sole
    m.round_box(bd, 0, -2.0, 4.6, 6.0, 2.0, 8.0, bootf, cut=2)                               # boot foot
    m.round_box(bd, 0, 2.6, 4.0, 3.6, 7.0, 15.0, bootf, cut=1)                              # boot shaft
    hd = m.bone("head", bd, (0, 15, 2))
    ball(m, hd, (0, 17.6, 2.0), 3.4, fabric(P, "cream", "cream_dark", axis="y"), layers=3)
    m.round_box(hd, -1.4, -1.2, 1.2, 0.4, 17.4, 19.6, solid(P, "red"), cut=0)                 # eye patch
    m.box(hd, -2.0, 18.2, -1.7, -0.8, 18.8, -1.5, solid(P, "black"))
    m.box(hd, 0.8, 17.6, -1.5, 1.8, 19.0, -1.3, solid(P, "green"))
    spike(m, hd, (0, 20.4, 2.6), (0.6, 1, 0.6), 2.6, 6.0, fabric(P, "red", "red_dark", axis="y"), tip=0.8)   # red cap
    for sx in (-1, 1):
        ball(m, hd, (sx * 3.4, 20.0, 2.0), 1.4, fabric(P, "cream", "cream_dark", axis="y"), layers=2)
    rod(m, hd, (-3.0, 15.6, 0.0), (-8.0, 26.0, -4.0), 1, metal(P, "steel"), extend=0.2, t2=1)   # sewing needle
    return m
