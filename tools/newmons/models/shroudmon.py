"""Shroudmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a hulking demon brawler: red hide crackling with a white heartbeat line across the chest, a
horned violet demon face with a red-gold crown of horns, a ghostly blue flame rising behind it, one arm ending in a
giant iron skull-gauntlet hung with chains and the other a spiked iron fist, black trousers strapped with violet, and
spiked iron boots. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking red demon brawler with a heartbeat line on its chest, a horned violet face, a giant iron skull-gauntlet and ghostly blue flame"
BASE = {"red": (190, 40, 40), "red_dark": (110, 14, 14), "violet": (110, 60, 160), "violet_dark": (50, 20, 90),
        "gold": (230, 180, 60), "black": (30, 28, 32), "black_dark": (10, 10, 12), "iron": (110, 90, 80),
        "iron_dark": (50, 40, 34), "steel": (190, 194, 206), "white": (250, 250, 255), "flame": (150, 170, 255, 180),
        "eye": (250, 220, 60), "chain": (200, 160, 70)}
SHINY = {"red": (60, 90, 170), "red_dark": (20, 34, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 44.0 < y < 50.0:
        t = (x + 6.0) * 1.2
        yy = 47.0 + (2.4 if int(t) % 5 == 2 else (-2.0 if int(t) % 5 == 3 else 0.0))
        if abs(y - yy) < 0.3:
            return p["white"], p["white"]
    return skin(P, "red", dark="red_dark")(x, y, z, face, variant, box=box, **k)


IRON = metal(P, "iron", dark="iron_dark")


def build():
    m = Model("shroudmon")
    mats = {"skin": hidef, "pelvis": fabric(P, "black", "black_dark", axis="y"), "thigh": fabric(P, "black", "black_dark"),
            "knee": armour(P, "violet", "violet_dark"), "shin": fabric(P, "black", "black_dark"),
            "foot": IRON, "talon": metal(P, "steel")}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.45, leg_bulk=1.2, talons=True, name="shroudmon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 6.0, 4.6, 31.0, 33.4, solid(P, "violet"), cut=1)
    ball(m, bd, (0, 32.0, -5.0), 1.4, solid(P, "eye", glow=True), layers=1)                  # belt eye
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 2.8, 3.2, 54.0, 60.0, skin(P, "violet", dark="violet_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.4, -4.1, max(sx * 0.8, sx * 2.2), 58.2, -3.9, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 60.0, -1.0), (sx * 0.3, 1, 0.1), 1.4, 7.0, solid(P, "gold"), tip=0.8)
    for j in range(5):
        spike(m, hd, (-2.0 + j, 60.0, 0.6), ((j - 2) * 0.2, 1, 0.2), 0.9, 3.0, solid(P, "red"), tip=0.8)
    fb = m.bone("flame", bd, (0, 52, 4))                                                 # ghostly blue flame
    for j in range(5):
        spike(m, fb, ((j - 2) * 2.6, 52.0, 5.0), ((j - 2) * 0.2, 1, 0.3), 3.0, 14.0 + (2 - abs(j - 2)) * 4.0,
              solid(P, "flame", glow=True), tip=0.8)
    h = a["arm_left"]["hand"]                                                            # giant skull gauntlet
    ab = a["arm_left"]["bone"]
    m.round_box(ab, h[0] + 1.0, h[2] - 2.0, 6.0, 6.0, h[1] - 4.0, h[1] + 8.0, IRON, cut=2)
    for sx in (-1, 1):
        m.box(ab, h[0] + 1.0 + sx * 2.4 - 1.2, h[1] + 3.0, h[2] - 8.2, h[0] + 1.0 + sx * 2.4 + 1.2, h[1] + 5.4, h[2] - 7.8,
              solid(P, "black"))
    for j in range(5):
        spike(m, ab, (h[0] - 2.0 + j * 1.6, h[1] - 3.0, h[2] - 7.6), (0, -1, -0.2), 0.9, 2.0, solid(P, "white"), tip=0.8)
    for j in range(5):                                                                   # hanging chain
        m.round_box(ab, h[0] + 7.6, h[2] - 2.0, 0.8, 0.8, h[1] - 4.0 - j * 2.0, h[1] - 3.0 - j * 2.0,
                    metal(P, "chain"), cut=0)
    h = a["arm_right"]["hand"]                                                           # spiked iron fist
    ball(m, a["arm_right"]["bone"], h, 3.6, IRON, layers=3)
    for j in range(5):
        ang = 2 * math.pi * j / 5
        spike(m, a["arm_right"]["bone"], (h[0] + 3.2 * math.cos(ang), h[1] + 3.2 * math.sin(ang), h[2]),
              (math.cos(ang), math.sin(ang), 0), 1.0, 2.6, metal(P, "steel"), tip=0.8)
    return m
