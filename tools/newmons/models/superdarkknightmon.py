"""Super Dark Knightmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Dark Knightmon merged with Skull Knightmon and Dead Ly Axemon: a stocky black-and-gold
armoured knight with a horned gold crown-helm, a bone-skull chest, a huge rust-red drill lance thrust from one arm
under a fanged dragon skull, great black dragon wings, a coiled black serpent tail with red spines, and gold-taloned
feet. 25 blocks. Perfect stage (no level on wikimon; by analogy).

Front is -z, y is up. 64 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a black-and-gold knight with a horned crown-helm, a bone-skull chest, a rust-red drill lance under a dragon skull and great black wings"
BASE = {"black": (40, 38, 44), "black_dark": (12, 12, 16), "gold": (236, 196, 70), "gold_dark": (150, 110, 20),
        "bone": (230, 222, 200), "bone_dark": (150, 140, 120), "rust": (170, 80, 50), "rust_dark": (100, 40, 20),
        "red": (200, 50, 40), "eye": (250, 220, 60)}
SHINY = {"black": (210, 210, 224), "black_dark": (130, 130, 146)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "black", "black_dark", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")
BONE = armour(P, "bone", "bone_dark")


def drillf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["rust"] if (z * 1.4 + y) % 2.0 < 1.2 else p["rust_dark"], face), None


def build():
    m = Model("superdarkknightmon")
    mats = {"skin": PLATE, "chest": BONE, "talon": GOLD, "claw": GOLD}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.2, leg_bulk=1.15, talons=True, claws=True, name="superdarkknightmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.8, 3.0, 54.0, 60.0, GOLD, cut=1)
    m.box(hd, -1.8, 57.0, -3.7, 1.8, 57.8, -3.5, solid(P, "eye", glow=True))
    for j in range(5):                                                                   # horned crown
        spike(m, hd, (-2.4 + j * 1.2, 60.0, -1.0), ((j - 2) * 0.2, 1, 0), 1.0, 3.0 + (j == 2) * 3.0, GOLD, tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # dragon skull + drill lance
    ab = a["arm_right"]["bone"]
    m.round_box(ab, w[0], w[2] - 4.0, 3.4, 5.0, w[1] - 3.0, w[1] + 4.0, BONE, cut=1)
    for j in range(4):
        spike(m, ab, (w[0] - 2.0 + j * 1.3, w[1] - 3.0, w[2] - 8.0), (0, -1, -0.2), 0.9, 2.0, BONE, tip=0.8)
    spike(m, ab, (w[0], w[1], w[2] - 9.0), (0, 0.1, -1), 4.0, 20.0, drillf, tip=0.8)
    for sx in (-1, 1):
        bat_wing(m, bd, (sx * 4.0, 50.0, 4.0), 30.0, 18.0, 4, metal(P, "black"), skin(P, "black", dark="black_dark"),
                 side=sx, sweep=25)
    tl = m.bone("tail", bd, (0, 32, 4))                                                  # coiled serpent tail
    pts = [(0, 32.0, 4.0), (6.0, 24.0, 10.0), (12.0, 18.0, 6.0), (14.0, 10.0, -2.0), (10.0, 6.0, -6.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 4 - i // 2, PLATE, extend=0.5)
        spike(m, tl, p1, (0.3, 1, 0.3), 1.2, 3.0, solid(P, "red"), tip=0.8)
    return m
