"""Herissmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
hedgehog: a round white hedgehog with a mane of silver-grey spines streaked yellow, a crest of golden spikes, big blue
eyes, a fanged smile, pink-tipped ears and red claws on its little paws and feet. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid, strands
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a round white hedgehog with silver-grey spines streaked yellow, a golden spike crest, blue eyes and red claws"
BASE = {"white": (246, 246, 250), "white_dark": (190, 192, 206), "spine": (170, 174, 186), "spine_dark": (90, 94, 106),
        "gold": (250, 210, 40), "gold_dark": (200, 150, 10), "eye": (60, 170, 230), "pupil": (16, 20, 30),
        "pink": (240, 120, 140), "claw": (220, 50, 70), "mouth": (180, 40, 60), "tooth": (250, 250, 250)}
SHINY = {"spine": (100, 70, 150), "spine_dark": (50, 30, 90), "gold": (90, 220, 200), "gold_dark": (40, 150, 140)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = fur(P, "white", "white_dark", length=0.8)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 18.0)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.2:
                return tone(p["eye"], face), None
        if abs(y - 15.6) < 0.5 and abs(x) < 1.6:
            return tone(p["mouth"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("herissmon")
    top = m.bone("herissmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 10.0, 0.6), 5.4, WHITE, layers=5)
    hd = m.bone("head", bd, (0, 14, -1))
    m.round_box(hd, 0, -1.0, 3.8, 3.4, 13.0, 21.0, headf, cut=2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.0, 15.4, -4.4), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
        spike(m, hd, (sx * 3.0, 20.0, 0), (sx * 0.6, 1, 0.2), 1.4, 2.4, solid(P, "pink"), tip=0.8)
    for i in range(18):                                                                   # mane of spines
        ang = math.radians(-170 + i * 20)
        spike(m, bd, (5.0 * math.cos(ang), 12.0 + 4.0 * math.sin(ang), 3.0), (math.cos(ang), math.sin(ang) + 0.3, 0.8),
              1.6, 6.0, strands(P, "spine", "spine_dark", tip="gold"), tip=0.8)
    for j in range(5):                                                                    # golden spike crest
        spike(m, hd, ((j - 2) * 1.0, 20.6, -1.0 + abs(j - 2) * 0.6), ((j - 2) * 0.25, 1, 0.3), 1.2, 6.0 - abs(j - 2),
              solid(P, "gold"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.4, 12.0, -1.0))
        rod(m, ab, (sx * 4.4, 12.0, -1.0), (sx * 6.0, 8.0, -3.0), 2, WHITE, extend=0.4)
        spike(m, ab, (sx * 6.0, 7.6, -3.6), (0, -0.6, -1), 1.2, 2.6, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 6.0, 0))
        m.round_box(lg, sx * 2.6, -0.6, 1.8, 2.4, 0.0, 6.0, WHITE, cut=1)
        spike(m, lg, (sx * 2.6, 0.6, -3.0), (0, -0.2, -1), 1.2, 2.0, solid(P, "claw"), tip=0.8)
    return m
