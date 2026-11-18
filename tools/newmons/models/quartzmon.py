"""Quartzmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the devourer of worlds: a vast black glass sphere swirling with sickly green light, clasped in a
golden rim with red thorns and a golden crescent jaw, carried high on four impossibly long spindly golden legs with
black joints, a faint red magic circle crowning it. 35 blocks.

Front is -z, y is up. 80 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, noise2, solid
from _route import pal, tone

HEIGHT = 80
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 5}
LOOK = "a vast black glass sphere swirling with green light in a golden thorned rim, on four impossibly long spindly golden legs"
BASE = {"black": (24, 26, 30), "green": (90, 200, 80), "green_dark": (30, 110, 40), "gold": (220, 190, 70),
        "gold_dark": (140, 100, 20), "red": (210, 40, 40), "joint": (20, 20, 22), "circle": (240, 90, 90, 170)}
SHINY = {"green": (200, 80, 220), "green_dark": (110, 30, 130), "gold": (200, 204, 216), "gold_dark": (110, 114, 126)}


def P(v):
    return pal(BASE, SHINY, v)


def spheref(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    n = noise2(x * 0.25 + z * 0.15, y * 0.25, 3)
    if n > 0.62 and x > -4.0:
        return tone(p["green"] if n > 0.72 else p["green_dark"], face), p["green"] if n > 0.72 else None
    return tone(p["black"], face), None


GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("quartzmon")
    top = m.bone("quartzmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 56, 0))
    ball(m, bd, (0, 64.0, 0), 14.0, spheref, layers=8)
    for i in range(20):                                                                  # golden rim with thorns
        ang = 2 * math.pi * i / 20
        cx, cz = 14.6 * math.cos(ang), 14.6 * math.sin(ang)
        m.box(bd, cx - 1.6, 63.0, cz - 1.6, cx + 1.6, 66.0, cz + 1.6, GOLD)
        if i % 2 == 0:
            spike(m, bd, (cx, 66.0, cz), (math.cos(ang) * 0.4, 1, math.sin(ang) * 0.4), 1.0, 3.0, solid(P, "red"),
                  tip=0.8)
    for sx in (-1, 1):                                                                   # golden crescent jaw
        rod(m, bd, (sx * 12.0, 58.0, -8.0), (sx * 4.0, 51.0, -12.0), 2, GOLD, extend=0.4)
    rb = m.bone("ring_circle", bd, (0, 80, 0))                                           # red magic circle
    for i in range(16):
        ang = 2 * math.pi * i / 16
        m.box(rb, 7.0 * math.cos(ang) - 1.0, 80.0, 7.0 * math.sin(ang) - 1.0, 7.0 * math.cos(ang) + 1.0, 80.4,
              7.0 * math.sin(ang) + 1.0, solid(P, "circle", glow=True))
    for sx in (-1, 1):                                                                   # four spindly legs
        for sz in (-1, 1):
            nm = f"leg_{'front' if sz < 0 else 'back'}_{'left' if sx > 0 else 'right'}"
            hip = (sx * 11.0, 60.0, sz * 9.0)
            knee = (sx * 26.0, 70.0, sz * 18.0)
            ankle = (sx * 24.0, 22.0, sz * 22.0)
            foot = (sx * 26.0, 1.0, sz * 26.0)
            lg = m.bone(nm, bd, hip)
            rod(m, lg, hip, knee, 2, GOLD, extend=0.4)
            ball(m, lg, knee, 1.6, solid(P, "joint"), layers=2)
            rod(m, lg, knee, ankle, 2, GOLD, extend=0.4)
            ball(m, lg, ankle, 1.4, solid(P, "joint"), layers=2)
            rod(m, lg, ankle, foot, 1, GOLD, extend=0.4)
            spike(m, lg, (foot[0], 1.0, foot[2]), (sx * 0.5, -0.1, sz * 0.5), 1.6, 6.0, GOLD, tip=0.8)
    return m
