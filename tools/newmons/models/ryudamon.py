"""Ryudamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little armoured dragon: a golden-furred beast body with a cream chest, a long tail and back covered
in overlapping black-violet scale plates edged purple, a samurai kabuto helm with tall crescent horns and a red visor,
a red topknot plume, green eyes, and white claws. 1 block.

Front is -z, y is up. 26 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, fur, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little golden-furred dragon armoured in black-violet scale plates with a samurai kabuto helm of tall crescent horns"
BASE = {"gold": (230, 190, 100), "gold_dark": (170, 120, 50), "cream": (250, 236, 200), "violet": (60, 40, 80),
        "violet_dark": (20, 12, 30), "purple": (170, 90, 210), "bronze": (170, 110, 60), "bronze_dark": (100, 60, 30),
        "red": (210, 40, 40), "eye": (90, 200, 90), "claw": (240, 240, 236)}
SHINY = {"gold": (200, 200, 214), "gold_dark": (130, 130, 150), "violet": (120, 40, 40), "violet_dark": (60, 14, 14)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "gold", "gold_dark", length=1.2)


def platef(x, y, z, face, variant, box=None, **k):
    if face in ("up", "east", "west", "south"):
        return scales(P, "violet", "purple", size=2.0)(x, y, z, face, variant, box=box, **k)
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ryudamon")
    mats = {"skin": platef, "belly": fur(P, "cream", "gold_dark"), "head": FUR, "snout": FUR, "jaw": FUR,
            "leg_upper": FUR, "leg_lower": FUR, "paw": FUR, "claw": solid(P, "claw"), "tail": platef}
    a = quadruped(m, mats, "ryudamon", length=22.0, body_y=10.0, body_rx=5.0, body_ry=4.6, neck=((0, 14, -12),
                  (0, 17, -15)), head_len=8.0, head_w=3.6, head_h=4.0, teeth=4, tail=((0, 12, 11), (0, 14, 18),
                  (0, 13, 24)), tail_r=(2.6, 2.0, 1.4))
    hd = a["head"]
    m.round_box(hd, 0, -15.0, 4.0, 3.6, 18.6, 21.0, armour(P, "bronze", "bronze_dark", trim="red", trim_w=0.2), cut=1)
    m.box(hd, -2.4, 18.0, -18.8, 2.4, 19.0, -18.4, solid(P, "red"))                        # red visor
    for sx in (-1, 1):                                                                   # crescent horns
        pts = [(sx * 1.2, 21.0, -17.0), (sx * 3.6, 25.0, -18.0), (sx * 5.0, 29.0, -16.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, metal(P, "bronze", dark="bronze_dark"), extend=0.2, t2=2)
        x0, x1 = sorted((sx * 3.5, sx * 3.8))
        m.box(hd, x0, 17.0, -17.0, x1, 17.8, -15.8, solid(P, "eye"))
    for j in range(4):                                                                   # red topknot plume
        rod(m, hd, (0, 21.0, -13.0), ((j - 1.5) * 0.8, 24.0, -6.0 - j), 1, strands(P, "red", "violet_dark"), extend=0.2, t2=2)
    return m
