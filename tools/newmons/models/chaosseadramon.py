"""Chaos Seadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official render on wikimon.net): a corrupted machine sea serpent. A long serpent of alternating black segments and
pale silver armour plates with spiked fins down its length, a silver helmeted head with a cannon nose, a red crest
and a long blade horn, ending in a bladed tail fin. 35 blocks long.

Front is -z, y is up. 40 units tall; Ultimate stage (floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "floater"
K = 3
LOOK = ("a long corrupted machine sea serpent of black segments and silver plates with spiked fins, a helmeted head "
        "with a cannon nose, a red crest and a blade horn")
BASE = {"silver": (200, 206, 226), "silver_dark": (110, 116, 140), "silver_light": (240, 244, 255), "black": (40, 40, 48),
        "black_light": (90, 90, 104), "red": (180, 30, 30), "eye": (240, 40, 40), "steel": (160, 164, 180)}
SHINY = {"silver": (220, 190, 110), "silver_dark": (150, 110, 40), "silver_light": (255, 240, 180), "red": (40, 150, 220)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = armour(P, "silver", "silver_dark", light="silver_light")
BLACK = metal(P, "black", dark="black", light="black_light")


def build():
    m = Model("chaosseadramon")
    top = m.bone("chaosseadramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    # the coiled body: a chain of segments along a sinuous path
    pts = []
    for i in range(18):
        t = i / 17
        pts.append((8.0 * math.sin(t * 5.0), 34.0 - 30.0 * t + 4.0 * math.sin(t * 7.0), -10.0 + 34.0 * t))
    bones = [bd]
    for j in range(1, 4):
        bones.append(m.bone(f"coil_{j}", bones[-1], pts[j * 4]))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        bn = bones[min(3, i // 4)]
        r = 5.0 * (1 - i / 22)
        rod(m, bn, p0, p1, max(2, round(2 * r)), SILVER if i % 2 == 0 else BLACK, extend=0.6)
        if i % 2 == 0:
            spike(m, bn, p1, (0, 1, 0.4), 1.6, 3.4, solid(P, "steel"))
            for sx in (-1, 1):
                spike(m, bn, p1, (sx, -0.2, 0.3), 1.2, 2.6, solid(P, "steel"))
    e = pts[-1]                                                               # bladed tail fin
    for d in ((0, 1, 0.6), (0, -0.4, 1), (0.6, 0.4, 0.8), (-0.6, 0.4, 0.8)):
        spike(m, bones[-1], e, d, 1.6, 5.0, SILVER, tip=0.4)
    hd = m.bone("head", bd, pts[0])                                           # helmeted head
    hx, hy, hz = pts[0]
    m.round_box(hd, hx, hz - 3.0, 3.6, 4.0, hy - 3.0, hy + 3.4, SILVER, cut=1)
    m.box(hd, hx - 2.6, hy - 2.4, hz - 13.0, hx + 2.6, hy + 1.6, hz - 6.0, SILVER)
    m.box(hd, hx - 1.6, hy - 1.6, hz - 14.0, hx + 1.6, hy + 0.8, hz - 13.0, BLACK)       # cannon nose
    for sx in (-1, 1):
        m.box(hd, min(hx + sx * 3.5, hx + sx * 3.8), hy + 0.6, hz - 6.0, max(hx + sx * 3.5, hx + sx * 3.8), hy + 1.6, hz - 4.6,
              solid(P, "eye", glow=True))
    m.box(hd, hx - 1.0, hy + 3.4, hz - 4.0, hx + 1.0, hy + 5.4, hz + 1.0, solid(P, "red"))
    spike(m, hd, (hx, hy + 3.4, hz - 6.0), (0, 1, -0.3), 2.0, 10.0, SILVER, tip=0.5)
    return m
