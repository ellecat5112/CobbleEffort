"""Tyrant Kabuterimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a tyrant beetle of dark violet chitin: a shark-jawed horned head with a forward-swept
crest, heavy silver-plated arms ending in great hooked claws, a glowing orange core in its chest, a segmented body
that tapers into a long tail ending in a spiked mace, and four translucent amber insect wings. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 55
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a dark violet tyrant beetle with a shark-jawed horned head, silver hooked claws, an orange core, amber insect wings and a mace tail"
BASE = {"violet": (90, 40, 110), "violet_dark": (36, 12, 50), "silver": (200, 204, 216), "silver_dark": (100, 104, 120),
        "core": (255, 150, 40), "wing": (250, 190, 90, 140), "mouth": (130, 20, 40), "tooth": (250, 250, 244),
        "eye": (255, 220, 60)}
SHINY = {"violet": (30, 100, 70), "violet_dark": (10, 50, 30)}


def P(v):
    return pal(BASE, SHINY, v)


CHITIN = armour(P, "violet", "violet_dark", panel=(3.0, 3.0))
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("tyrantkabuterimon")
    top = m.bone("tyrantkabuterimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 36, 0))
    m.round_box(bd, 0, 0, 7.0, 5.0, 34.0, 46.0, CHITIN, cut=2)
    ball(m, bd, (0, 40.0, -5.4), 1.8, solid(P, "core", glow=True), layers=2)
    for j in range(4):                                                                 # tapering segmented abdomen
        r = 5.4 - j * 1.0
        m.round_box(bd, 0, 1.0 + j * 0.8, r, r * 0.8, 28.0 - j * 5.0, 33.6 - j * 5.0, CHITIN, cut=1)
    tl = m.bone("tail", bd, (0, 14, 3))
    pts = [(0, 14.0, 3.0), (2.0, 8.0, 5.0), (5.0, 4.0, 4.0), (8.0, 3.0, 1.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, CHITIN, extend=0.3)
    ball(m, tl, (8.6, 3.0, 0.4), 1.6, SILVER, layers=2)
    for j in range(6):
        ang = j * math.pi / 3
        spike(m, tl, (8.6 + 1.4 * math.cos(ang), 3.0 + 1.4 * math.sin(ang), 0.4), (math.cos(ang), math.sin(ang), 0), 0.8,
              1.8, SILVER, tip=0.8)
    hd = m.bone("head", bd, (0, 46, -2))
    m.round_box(hd, 0, -4.0, 3.6, 4.6, 46.0, 52.0, CHITIN, cut=1)
    m.box(hd, -3.0, 46.4, -10.0, 3.0, 48.4, -5.0, solid(P, "mouth"))
    for j in range(5):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.6, 48.4, -9.4 + j * 1.0), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 3.4), 50.0, -8.8, max(sx * 1.6, sx * 3.4), 50.8, -8.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 3.0, 51.0, -3.0), (sx * 0.5, 1, 0.3), 1.4, 6.0, CHITIN, tip=0.8)
    spike(m, hd, (0, 52.0, -6.0), (0, 0.6, -1), 2.0, 9.0, CHITIN, tip=0.8)                  # forward crest
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # silver claw arms
        ab = m.bone(nm, bd, (sx * 7.0, 44.0, 0))
        m.round_box(ab, sx * 9.0, 0, 3.0, 3.0, 40.0, 47.0, SILVER, cut=1)
        rod(m, ab, (sx * 9.0, 40.0, 0), (sx * 11.0, 30.0, -4.0), 3, SILVER, extend=0.4)
        for f in range(4):
            ang = (f - 1.5) * 0.5
            pts = [(sx * 11.0, 30.0, -4.0), (sx * (11.0 + math.sin(ang) * 4.0), 26.0, -6.0 - math.cos(ang) * 2.0),
                   (sx * (11.0 + math.sin(ang) * 5.0), 22.0, -4.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 1, SILVER, extend=0.2)
    wb = m.bone("wings", bd, (0, 44, 4))
    for sx in (-1, 1):
        for j, (ang, L) in enumerate(((35, 22.0), (-10, 18.0))):
            x0, x1 = sorted((sx * 2.0, sx * (2.0 + L)))
            m.box(wb, x0, 42.0, 5.0, x1, 48.0, 5.2, solid(P, "wing", glow=True), rotation=(0, 0, sx * ang),
                  pivot=(sx * 2.0, 45.0, 5.1))
    return m
