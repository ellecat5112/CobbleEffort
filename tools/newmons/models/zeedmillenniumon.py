"""Zeed Millenniumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the wicked god of the ages: a vast ragged mass of torn dark violet-and-rust flesh with
two great snarling dragon heads, clawed limbs trailing tatters, and glowing green rings of digital code spinning
round it like an orrery. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fbm, skin, solid
from _route import pal, tone

HEIGHT = 55
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a vast ragged mass of torn violet-and-rust flesh with two great snarling dragon heads, clawed tatters and spinning green code rings"
BASE = {"violet": (90, 80, 120), "violet_dark": (36, 30, 56), "rust": (130, 80, 60), "rust_dark": (70, 40, 26),
        "code": (90, 230, 150, 190), "tooth": (240, 236, 220), "eye": (255, 240, 120), "claw": (200, 190, 220)}
SHINY = {"violet": (150, 150, 160), "violet_dark": (70, 70, 80), "rust": (60, 90, 140), "rust_dark": (24, 40, 80),
         "code": (240, 120, 200, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def fleshf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = fbm(x * 0.15, y * 0.15, z * 0.15, seed=11)
    key = "rust" if x > 0 else "violet"
    c = p[key] if t < 0.55 else p[key + "_dark"]
    return tone(c, face), None


def head(m, bone, c, sx):
    x, y, z = c
    m.round_box(bone, x, z - 3.0, 3.4, 6.0, y - 3.0, y + 3.4, fleshf, cut=1)
    jb = m.bone(bone + "_jaw", bone, (x, y - 3.0, z - 2.0))
    m.round_box(jb, x, z - 3.0, 3.0, 5.4, y - 5.0, y - 3.0, fleshf, cut=1)
    for j in range(5):
        for s in (-1, 1):
            spike(m, bone, (x + s * 2.6, y - 3.0, z - 7.0 + j * 1.4), (0, -1, 0), 0.9, 1.8, solid(P, "tooth"), tip=0.8)
    ball(m, bone, (x + sx * 2.8, y + 1.6, z - 5.0), 0.7, solid(P, "eye", glow=True), layers=1)
    for j in range(3):
        spike(m, bone, (x + (j - 1) * 1.6, y + 3.0, z), (sx * 0.3, 1, 0.6), 1.4, 6.0, fleshf, tip=0.8)


def build():
    m = Model("zeedmillenniumon")
    top = m.bone("zeedmillenniumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    for (x, y, z, r) in ((0, 30, 0, 12.0), (-8, 22, 2, 8.0), (8, 22, 2, 8.0), (-10, 38, 0, 7.0), (10, 38, 0, 7.0),
                         (0, 16, 2, 7.0)):
        ball(m, bd, (x, y, z), r, fleshf, layers=3)
    for i in range(10):                                                                 # torn tatters
        ang = (i - 4.5) * 0.35
        spike(m, bd, (math.sin(ang) * 10.0, 14.0, 2.0), (math.sin(ang) * 0.5, -1, 0.1), 2.4, 10.0 + (i % 3) * 3.0,
              fleshf, tip=0.8)
    hl = m.bone("head_left", bd, (8, 44, -4))
    head(m, hl, (11.0, 48.0, -6.0), 1)
    hr = m.bone("head_right", bd, (-8, 44, -4))
    head(m, hr, (-11.0, 48.0, -6.0), -1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 12.0, 26.0, -2.0))
        rod(m, ab, (sx * 12.0, 26.0, -2.0), (sx * 18.0, 14.0, -4.0), 2, fleshf, extend=0.5)
        for f in range(3):
            spike(m, ab, (sx * 18.0, 14.0, -4.0), (sx * 0.3 + (f - 1) * 0.3, -1, -0.4), 1.0, 5.0, solid(P, "claw"), tip=0.8)
    rg = m.bone("rings", bd, (0, 30, 0))                                               # spinning code rings
    for k, (tilt_y, tilt_x) in enumerate(((0.0, 0.0), (1.0, 0.5), (-1.0, 0.5))):
        for i in range(24):
            ang = i * 2 * math.pi / 24
            cx = 18.0 * math.cos(ang)
            cy = 30.0 + 18.0 * math.sin(ang) * (0.3 + 0.7 * abs(tilt_x)) * (1 if k else 0.25)
            cz = 18.0 * math.sin(ang) * (1.0 if k == 0 else 0.4) + tilt_y * 2.0
            if cy < 1.0:
                continue
            m.box(rg, cx - 1.2, cy - 0.8, cz - 1.2, cx + 1.2, cy + 0.8, cz + 1.2, solid(P, "code", glow=True))
    return m
