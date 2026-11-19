"""Tlalocmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a living rain-god totem: a great round mass of dark green leaves around a carved grey stone
idol face with goggle-ring eyes, curved horns and a crest of red-and-orange feathers, little stone hands holding
leafy sceptres, curling vines below, golden lightning crackling on one side and swirling blue water on the other. 35
blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, feathers, fur, metal, plane, solid
from _route import pal, tone

HEIGHT = 53
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a rain-god totem: a round mass of dark leaves round a carved stone idol face with ring eyes, horns and a red feather crest, lightning and water at its sides"
BASE = {"leaf": (60, 110, 60), "leaf_dark": (24, 60, 30), "stone": (150, 150, 140), "stone_dark": (80, 80, 76),
        "red": (220, 60, 40), "orange": (250, 160, 50), "gold": (250, 210, 60), "water": (110, 200, 250, 200),
        "vine": (50, 100, 70), "eye": (250, 60, 60), "blue": (60, 80, 160)}
SHINY = {"leaf": (140, 90, 160), "leaf_dark": (80, 40, 100)}


def P(v):
    return pal(BASE, SHINY, v)


STONE = armour(P, "stone", "stone_dark", panel=(2.4, 2.4))
LEAF = fur(P, "leaf", "leaf_dark", length=2.0, density=1.4)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 4.4, b - 34.0)
            if d < 1.0:
                return p["eye"], p["eye"]
            if d < 3.2:
                return tone(p["stone_dark"] if d > 2.4 else p["stone"], face), None
        if abs(a) < 3.0 and 26.0 < b < 28.0:
            return tone(p["blue"], face), None
    return STONE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tlalocmon")
    top = m.bone("tlalocmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    for i in range(14):                                                                # leaf mass
        ang = i * 2 * math.pi / 14
        ball(m, bd, (15.0 * math.cos(ang), 32.0 + 15.0 * math.sin(ang), 2.0), 6.4, LEAF, layers=3)
    ball(m, bd, (0, 32.0, 4.0), 12.0, LEAF, layers=4)
    hd = m.bone("head", bd, (0, 32, -6))
    m.round_box(hd, 0, -8.0, 9.0, 3.0, 22.0, 42.0, facef, cut=2)
    m.round_box(hd, 0, -9.0, 10.0, 2.0, 40.0, 44.0, STONE, cut=1)
    for sx in (-1, 1):                                                                 # horns
        pts = [(sx * 9.0, 42.0, -7.0), (sx * 13.0, 46.0, -7.0), (sx * 14.0, 51.0, -6.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, metal(P, "stone", dark="stone_dark"), extend=0.5)
    for j in range(7):                                                                 # feather crest
        ang = (j - 3) * 0.32
        spike(m, hd, (math.sin(ang) * 5.0, 44.0, -8.0), (math.sin(ang), 1, 0), 2.4, 9.0 + (3 - abs(j - 3)) * 1.5,
              feathers(P, "red" if j % 2 else "orange", "red"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # stone hands + sceptres
        ab = m.bone(nm, bd, (sx * 10.0, 22.0, -8.0))
        m.round_box(ab, sx * 13.0, -10.0, 2.0, 2.0, 20.0, 24.0, STONE, cut=1)
        rod(m, ab, (sx * 13.0, 14.0, -11.0), (sx * 14.0, 30.0, -11.0), 1, solid(P, "gold"), extend=0.0)
        ball(m, ab, (sx * 14.0, 31.0, -11.0), 1.6, LEAF, layers=1)
    vn = m.bone("vines", bd, (0, 16, 0))
    for i in range(6):                                                                 # curling vines
        x0 = (i - 2.5) * 4.0
        pts = [(x0, 18.0, 0), (x0 * 1.3, 12.0, -1.0), (x0 * 1.6 + 2.0, 6.0, 0), (x0 * 1.6 - 1.0, 2.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, vn, p0, p1, 1, solid(P, "vine"), extend=0.4)
    for j in range(6):                                                                 # lightning (left), water (right)
        y = 22.0 + j * 5.0
        m.box(bd, 24.0 + (j % 2) * 2.0, y, -1.0, 26.0 + (j % 2) * 2.0, y + 5.4, 1.0, solid(P, "gold", glow=True),
              rotation=(0, 0, 20 if j % 2 else -20), pivot=(25.0, y, 0))
        ball(m, bd, (-24.0 - 2.0 * math.sin(j), y + 2.0, 0), 1.8, solid(P, "water"), layers=1)
    return m
