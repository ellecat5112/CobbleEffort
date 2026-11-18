"""Reptilimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a crystal dragon-warrior: a hulking black-hided dragon with a lavender fur ruff and a fiery red
mane under a golden dragon-skull helm, great clusters of faceted red crystal growing from its shoulders and back,
red crystal claws and toes, golden bands, a long red-and-gold patterned loincloth and a thick lavender tail. 25 blocks.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking black dragon-warrior with a lavender ruff, a red mane, a golden skull helm and great clusters of faceted red crystal"
BASE = {"black": (40, 36, 44), "black_dark": (14, 12, 16), "lavender": (190, 170, 230), "lavender_dark": (130, 110, 180),
        "red": (220, 40, 60), "crystal": (240, 60, 80), "gold": (236, 190, 60), "gold_dark": (150, 100, 20),
        "white": (255, 230, 230), "eye": (250, 220, 60)}
SHINY = {"red": (60, 140, 230), "crystal": (90, 180, 250), "black": (240, 236, 230), "black_dark": (180, 176, 170)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "black", dark="black_dark")
CRYST = gem(P, "crystal", "white", glow=False)
GOLD = metal(P, "gold", dark="gold_dark")


def clothf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(abs(x) - (y % 4.0)) < 0.3 or abs(x) < 0.3:
        return tone(p["white"], face), None
    return fabric(P, "red", "black_dark", axis="y", period=3.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("reptilimon")
    mats = {"skin": HIDE, "claw": CRYST, "talon": CRYST, "knee": GOLD}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.25, leg_bulk=1.3, claws=True, talons=True, digitigrade=True,
                 name="reptilimon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 7.4, 5.4, 46.0, 53.0, fur(P, "lavender", "lavender_dark", length=1.6), cut=2)   # ruff
    m.box(bd, -2.4, 12.0, -5.6, 2.4, 32.0, -5.0, clothf)                                   # loincloth
    m.round_box(bd, 0, 0, 6.0, 4.4, 31.0, 33.0, GOLD, cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.6, 2.8, 4.0, 54.0, 60.0, HIDE, cut=1)
    m.round_box(hd, 0, -2.0, 3.0, 4.2, 58.0, 61.0, GOLD, cut=1)                            # golden skull helm
    spike(m, hd, (0, 59.0, -5.6), (0, 0.2, -1), 1.6, 3.0, GOLD, tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.7, sx * 2.9), 57.0, -4.0, max(sx * 2.7, sx * 2.9), 58.0, -2.6, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.6, 61.0, -1.0), (sx * 0.5, 1, 0.3), 1.6, 6.0, solid(P, "crystal"), tip=0.8)
    for j in range(8):                                                                   # fiery red mane
        spike(m, hd, ((j % 2 * 2 - 1) * 1.2, 60.0 - j * 0.6, 1.0 + j * 0.8), ((j % 2 * 2 - 1) * 0.4, 0.6, 1), 1.4,
              6.0, strands(P, "red", "black_dark"), tip=0.8)
    for sx in (-1, 1):                                                                   # crystal clusters
        for j in range(5):
            ang = math.radians(20 + j * 28)
            spike(m, bd, (sx * 8.0, 50.0, 1.0 + j * 0.6), (sx * math.cos(ang), math.sin(ang), 0.4), 2.4,
                  8.0 + (j % 3) * 2.0, CRYST, tip=0.8)
    for j in range(4):
        spike(m, bd, ((j - 1.5) * 2.4, 44.0 - j * 2.0, 4.6), ((j - 1.5) * 0.3, 0.4, 1), 2.0, 6.0, CRYST, tip=0.8)
    tl = m.bone("tail", bd, (0, 32, 4))
    pts = [(0, 32.0, 4.0), (0, 22.0, 12.0), (2.0, 12.0, 18.0), (4.0, 6.0, 24.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 6 - i * 1, fur(P, "lavender", "lavender_dark", length=1.6), extend=0.6)
    return m
