"""Tonosama Gekomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the frog lord: a huge squat red toad with a round yellow belly, drooping lazy eyes and
long whiskers, a ruff of green leaves round its neck, a purple top-knot, two curving golden horns ending in
trumpet bells, and red suction-cup fingers and toes. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a huge squat red toad lord with a yellow belly, lazy eyes, a ruff of leaves, a purple top-knot and two golden trumpet horns"
BASE = {"red": (220, 60, 40), "red_dark": (140, 24, 14), "yellow": (240, 220, 80), "yellow_dark": (190, 160, 30),
        "leaf": (70, 150, 60), "leaf_dark": (30, 90, 30), "purple": (110, 60, 160), "purple_dark": (60, 24, 100),
        "gold": (240, 200, 70), "gold_dark": (170, 120, 30), "eye": (250, 240, 140), "black": (30, 20, 20),
        "mouth": (110, 20, 20), "tooth": (250, 250, 240)}
SHINY = {"red": (60, 140, 200), "red_dark": (20, 80, 140)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark")
GOLD = metal(P, "gold", dark="gold_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if abs(b - 25.0 - 0.06 * a * a) < 0.35 and abs(a) < 6.0:
            return p["mouth"], None
    return RED(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tonosamagekomon")
    top = m.bone("tonosamagekomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 11.0, 0), 10.0, skin(P, "yellow", dark="yellow_dark"), layers=6)     # round yellow belly
    ball(m, bd, (0, 12.0, 3.0), 9.6, RED, layers=5)
    hd = m.bone("head", bd, (0, 22, -2))
    ball(m, hd, (0, 26.0, -3.0), 7.4, headf, layers=5, squash=0.7)
    for sx in (-1, 1):                                                                 # lazy eyes
        ball(m, hd, (sx * 3.6, 30.0, -6.0), 2.2, solid(P, "eye"), layers=2)
        m.box(hd, sx * 3.6 - 1.6, 30.4, -8.3, sx * 3.6 + 1.6, 31.6, -7.9, RED)
        m.box(hd, sx * 3.6 - 0.4, 29.2, -8.2, sx * 3.6 + 0.4, 30.4, -8.0, solid(P, "black"))
        pts = [(sx * 5.0, 25.0, -8.0), (sx * 9.0, 24.0, -9.0), (sx * 12.0, 26.0, -8.0)]        # whiskers
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "purple"), extend=0.3)
        pts = [(sx * 4.0, 31.0, 0), (sx * 9.0, 35.0, 0), (sx * 12.0, 33.0, 0), (sx * 14.0, 36.0, 0)]  # trumpet horns
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, GOLD, extend=0.4)
        m.round_box(hd, sx * 14.4, 0, 2.6, 2.6, 36.0, 39.0, GOLD, cut=1)
    for j in range(5):                                                                 # purple top-knot
        spike(m, hd, ((j - 2) * 0.8, 32.0, -1.0), ((j - 2) * 0.3, 1, -0.2), 1.6, 5.0, strands(P, "purple",
              "purple_dark"), tip=0.8)
    for i in range(12):                                                                # leaf ruff
        ang = i * 2 * math.pi / 12
        spike(m, bd, (6.0 * math.sin(ang), 21.0, 6.0 * math.cos(ang) - 1.0), (math.sin(ang), -0.2, math.cos(ang)), 2.6,
              5.0, fur(P, "leaf", "leaf_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.0, 16.0, -4.0))
        rod(m, ab, (sx * 8.0, 16.0, -4.0), (sx * 12.0, 10.0, -8.0), 2, RED, extend=0.4)
        for j in range(4):
            ang = (j - 1.5) * 0.5
            rod(m, ab, (sx * 12.0, 10.0, -8.0), (sx * 12.0 + math.sin(ang) * 3.0, 8.0, -8.0 - math.cos(ang) * 3.0), 1, RED,
                extend=0.2)
            ball(m, ab, (sx * 12.0 + math.sin(ang) * 3.4, 8.0, -8.0 - math.cos(ang) * 3.4), 0.9, RED, layers=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 4.0, 0))
        ball(m, lg, (sx * 8.0, 4.0, 1.0), 4.0, RED, layers=3)
        for j in range(3):
            ang = (j - 1) * 0.5
            rod(m, lg, (sx * 8.0, 1.0, -2.0), (sx * 8.0 + math.sin(ang) * 3.0, 0.6, -5.0), 1, RED, extend=0.2)
    return m
