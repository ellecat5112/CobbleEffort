"""Marin Bullmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the sea slug beast: a big hunched hot-pink slug-whale streaked with cyan stripes, a stitched scar, a long gaping
mouth, a crest of cyan fins, a curling horn of orange-to-yellow, a frilled mane of green ribbon gills on its back,
clawed cyan-tipped hands, a ringed belt and a long drooping pink mantle trailing to the floor. 25 blocks long.

Front is -z, y is up. 36 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
LOOK = "a big hunched hot-pink sea slug beast with cyan stripes, a crest of fins, a curling horn, green ribbon gills and a trailing mantle"
BASE = {"pink": (230, 80, 160), "pink_dark": (150, 30, 100), "pink_light": (250, 170, 210), "cyan": (60, 200, 230),
        "green": (60, 200, 120), "green_dark": (20, 120, 60), "orange": (240, 140, 40), "yellow": (250, 220, 60),
        "white": (240, 240, 244), "steel": (150, 154, 166), "mouth": (40, 30, 40), "eye": (30, 30, 34)}
SHINY = {"pink": (240, 170, 60), "pink_dark": (170, 100, 20), "pink_light": (255, 220, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(z * 0.6 - y * 0.3)) > 0.93:
        return tone(p["cyan"], face), None
    return skin(P, "pink", dark="pink_dark", light="pink_light")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("marinbullmon")
    top = m.bone("marinbullmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 6.0, 9.0, 12.0, 0.0, 4.0, hidef, cut=3)                         # trailing mantle
    m.round_box(bd, 0, 2.0, 6.0, 8.0, 4.0, 20.0, hidef, cut=3)
    m.round_box(bd, 0, 0, 6.2, 6.0, 10.0, 12.0, metal(P, "steel", dark="mouth"), cut=2)     # ringed belt
    hd = m.bone("head", bd, (0, 20, -6))
    m.round_box(hd, 0, -8.0, 3.6, 7.0, 18.0, 28.0, hidef, cut=2)                       # long head
    m.round_box(hd, 0, -14.4, 2.6, 0.8, 19.0, 22.0, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.5, sx * 3.8), 25.0, -12.0, max(sx * 3.5, sx * 3.8), 26.0, -10.6, solid(P, "eye"))
    pts = [(0, 28.0, -12.0), (0, 32.0, -16.0), (-1.0, 36.0, -14.0)]                    # curling horn
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 1, solid(P, "orange" if j == 0 else "yellow"), extend=0.3, t2=2)
    for j in range(6):                                                               # cyan fin crest
        spike(m, hd, (0, 28.0, -10.0 + j * 2.4), (0, 1, 0.5), 1.0, 3.0, solid(P, "cyan"), tip=0.8)
    for i in range(10):                                                              # green ribbon gills
        ang = math.radians(-60 + i * 14)
        spike(m, bd, (5.0 * math.sin(ang), 20.0, 6.0), (math.sin(ang), 1, 0.5), 1.8, 10.0, strands(P, "green", "green_dark"),
              tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 16.0, -4.0))
        rod(m, ab, (sx * 6.0, 16.0, -4.0), (sx * 8.0, 8.0, -10.0), 2, hidef, extend=0.4)
        for j in range(4):
            spike(m, ab, (sx * 8.0 + (j - 1.5) * 1.0, 7.0, -11.0), (0, -0.4, -1), 0.9, 3.0, solid(P, "cyan"), tip=0.8)
    return m
