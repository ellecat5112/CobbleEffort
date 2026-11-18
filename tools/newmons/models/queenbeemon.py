"""Queenbeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the queen of the hive: a slender figure in gleaming black-and-gold banded bee armour from helm to
heeled sabatons, white fur trim at the collar, wrists and knees, a golden visored helm with two long violet antennae,
long lilac hair braided down into a golden striped stinger-gauntlet, a golden fan of flame in one hand, and four
great translucent pale-green wings shimmering behind. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, fur, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a slender queen in black-and-gold banded bee armour with fur trim, a golden helm with violet antennae and four translucent wings"
BASE = {"gold": (236, 190, 60), "gold_dark": (150, 100, 20), "black": (36, 32, 36), "black_dark": (12, 10, 12),
        "white": (250, 248, 240), "white_dark": (200, 196, 186), "violet": (110, 90, 200), "lilac": (180, 140, 220),
        "lilac_dark": (120, 80, 170), "wing": (220, 246, 210, 150), "flame": (250, 210, 80), "visor": (240, 120, 40)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (140, 144, 160), "lilac": (240, 150, 170), "lilac_dark": (180, 90, 110)}


def P(v):
    return pal(BASE, SHINY, v)


def bandf(x, y, z, face, variant, box=None, **k):
    if (y % 4.0) < 1.6:
        return armour(P, "gold", "gold_dark")(x, y, z, face, variant, box=box, **k)
    return armour(P, "black", "black_dark", trim="gold", trim_w=0.15)(x, y, z, face, variant, box=box, **k)


FUR = fur(P, "white", "white_dark", length=0.8)
GOLD = metal(P, "gold", dark="gold_dark")


def wing_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    du, dv = (u / max(W, 1e-6)) - 0.5, (v / max(H, 1e-6)) - 0.5
    return du * du + dv * dv * 1.4 < 0.25


def build():
    m = Model("queenbeemon")
    mats = {"skin": bandf, "neck": FUR, "knee": FUR, "hand": bandf, "finger": GOLD, "foot": bandf}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.75, leg_bulk=0.8, name="queenbeemon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 4.6, 3.8, 50.0, 53.0, FUR, cut=1)                                 # fur collar
    for side in ("arm_left", "arm_right"):
        w = a[side]["wrist"]
        m.round_box(a[side]["bone"], w[0], w[2], 1.8, 1.8, w[1], w[1] + 2.0, FUR, cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.0, GOLD, cut=1)                            # golden visored helm
    m.box(hd, -1.8, 57.0, -3.3, 1.8, 57.8, -3.1, solid(P, "visor", glow=True))
    for sx in (-1, 1):                                                                   # violet antennae
        rod(m, hd, (sx * 1.0, 60.0, -1.0), (sx * 2.6, 68.0, -2.0), 1, solid(P, "violet"), extend=0.2)
        spike(m, hd, (sx * 2.6, 68.0, -2.0), (sx * 0.2, 1, -0.2), 1.0, 3.0, solid(P, "violet"), tip=0.8)
    pts = [(0, 58.0, 2.6), (6.0, 52.0, 6.0), (12.0, 50.0, 2.0), (16.0, 52.0, -4.0)]      # lilac braid
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 2, strands(P, "lilac", "lilac_dark"), extend=0.4)
    m.round_box(hd, 17.0, -5.0, 2.4, 2.4, 50.0, 55.0, bandf, cut=1)                         # stinger gauntlet
    spike(m, hd, (17.0, 52.6, -7.4), (0.2, 0, -1), 1.6, 3.0, GOLD, tip=0.8)
    w = a["arm_right"]["wrist"]                                                          # golden flame fan
    for j in range(5):
        ang = math.radians(60 + j * 15)
        spike(m, a["arm_right"]["bone"], (w[0], w[1] - 1.0, w[2] - 1.0), (-math.cos(ang), math.sin(ang), -0.3), 1.0,
              7.0, solid(P, "flame", glow=True), tip=0.8)
    wb = m.bone("wings", bd, (0, 46, 3))                                                 # four translucent wings
    for sx in (-1, 1):
        for j, (ang, ln) in enumerate(((30, 26.0), (-20, 22.0))):
            x0, x1 = sorted((sx * 2.0, sx * (2.0 + ln)))
            m.box(wb, x0, 40.0, 4.0 + j * 0.4, x1, 52.0, 4.0 + j * 0.4, cutout(wing_in, solid(P, "wing")),
                  rotation=(0, -sx * 15, sx * ang), pivot=(sx * 2.0, 46.0, 4.0))
    return m
