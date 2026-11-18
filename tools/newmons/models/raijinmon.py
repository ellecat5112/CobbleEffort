"""Raijinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the thunder god machine: a cream-and-steel robot with a ring of thunder drums on its back like
Raijin's, each drum marked with a pink swirl and a red cross, a crested pink-visored helm, one huge steel fist and
one jointed claw arm, pink orb joints, a coiled yellow power cable for a tail, and clawed feet. 35 blocks.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a cream-and-steel thunder-god robot with a ring of drums on its back, a pink-visored helm, one huge steel fist and a cable tail"
BASE = {"cream": (240, 236, 210), "cream_dark": (180, 170, 140), "steel": (190, 194, 206), "steel_dark": (90, 94, 108),
        "pink": (230, 110, 140), "red": (210, 40, 40), "yellow": (250, 210, 50), "visor": (240, 120, 160)}
SHINY = {"cream": (60, 64, 80), "cream_dark": (24, 26, 36), "pink": (90, 200, 240)}


def P(v):
    return pal(BASE, SHINY, v)


CREAM = armour(P, "cream", "cream_dark", trim="steel", trim_w=0.2)
STEEL = metal(P, "steel", dark="steel_dark")


def drumf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south", "east", "west"):
        u, v = (x + z), y
        cu = round(u / 6.0) * 6.0
        d = math.hypot(u - cu, v - round(v / 6.0) * 6.0)
        if d < 0.6:
            return tone(p["red"], face), None
        if d < 1.8 and int(d * 3) % 2 == 0:
            return tone(p["pink"], face), None
    return CREAM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("raijinmon")
    mats = {"skin": CREAM, "neck": STEEL, "knee": solid(P, "pink"), "forearm": STEEL, "hand": STEEL, "finger": STEEL,
            "talon": STEEL, "shin": STEEL}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, talons=True, name="raijinmon")
    bd = a["body"]
    for j in range(6):                                                                   # ring of thunder drums
        ang = math.radians(-60 + j * 24 + (0 if j < 3 else 72))
        if j >= 3:
            ang = math.radians(60 + (j - 3) * 30)
        cx, cy = 13.0 * math.cos(ang + math.pi / 2), 52.0 + 10.0 * math.sin(ang + math.pi / 2) * 0.6
        rod(m, bd, (cx, cy, 5.0), (cx, cy, 11.0), 6, drumf, extend=0.2)
    rb = m.bone("drum_ring", bd, (0, 50, 6))
    for i in range(14):
        ang = math.pi * i / 13
        m.box(rb, 13.0 * math.cos(ang) - 0.8, 48.0 + 9.0 * math.sin(ang) - 0.8, 7.4, 13.0 * math.cos(ang) + 0.8,
              48.0 + 9.0 * math.sin(ang) + 0.8, 8.6, STEEL)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, CREAM, cut=1)
    m.box(hd, -1.8, 57.0, -3.3, 1.8, 58.0, -3.1, solid(P, "visor", glow=True))
    spike(m, hd, (0, 60.0, -1.0), (0, 1, 0.4), 1.4, 5.0, STEEL, tip=0.8)
    for sx in (-1, 1):
        ball(m, bd, (sx * 7.6, 48.0, 0), 2.6, solid(P, "pink"), layers=2)                 # pink shoulder orbs
    h = a["arm_left"]["hand"]                                                            # huge steel fist
    ball(m, a["arm_left"]["bone"], (h[0] + 1.0, h[1], h[2]), 5.0, STEEL, layers=4)
    tl = m.bone("tail", bd, (0, 32, 3))                                                  # coiled cable tail
    pts = [(0, 32.0, 3.0), (3.0, 24.0, 8.0), (8.0, 12.0, 10.0), (12.0, 4.0, 6.0), (16.0, 2.0, 2.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, solid(P, "yellow"), extend=0.2, t2=2)
    m.box(tl, 16.0, 1.0, 0.6, 18.0, 3.0, 3.4, STEEL)
    return m
