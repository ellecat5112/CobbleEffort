"""Shakamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the enlightened one: a golden sage seated in meditation in flowing golden robes, a calm golden face
with a jewelled crown, long silver hair streaming down, a great radiant sunburst halo behind, a golden sun-orb glowing
beneath, and a ring of golden coin-seals orbiting. 35 blocks.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, solid, strands
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a golden sage seated in meditation in flowing golden robes with silver hair, a radiant sunburst halo, a sun-orb beneath and orbiting coin-seals"
BASE = {"gold": (240, 200, 80), "gold_dark": (170, 120, 30), "silver": (220, 220, 232), "silver_dark": (150, 150, 170),
        "sun": (255, 220, 100), "face": (230, 190, 90), "black": (40, 30, 20), "gem": (220, 40, 60)}
SHINY = {"gold": (220, 224, 240), "gold_dark": (140, 144, 170), "face": (210, 214, 230), "sun": (190, 220, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ROBE = fabric(P, "gold", "gold_dark", axis="y", period=2.6)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("shakamon")
    top = m.bone("shakamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 12.0, 0), 6.0, solid(P, "sun", glow=True), layers=4)                    # sun-orb beneath
    m.round_box(bd, 0, 0, 10.0, 7.0, 20.0, 25.0, ROBE, cut=3)                               # crossed legs
    m.round_box(bd, 0, 0.6, 5.4, 4.0, 24.0, 40.0, ROBE, cut=1)                              # seated body
    for sx in (-1, 1):
        rod(m, bd, (sx * 5.6, 38.0, 0), (sx * 7.0, 28.0, -3.0), 3, ROBE, extend=0.4)
        rod(m, bd, (sx * 7.0, 28.0, -3.0), (sx * 2.0, 26.0, -5.0), 3, ROBE, extend=0.4)
    m.round_box(bd, 0, -5.4, 2.0, 1.4, 25.0, 27.6, solid(P, "face"), cut=0)                  # folded hands
    hd = m.bone("head", bd, (0, 40, 0))
    m.round_box(hd, 0, -0.4, 3.0, 3.2, 40.0, 47.0, solid(P, "face"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 44.0, -3.7, max(sx * 0.6, sx * 2.0), 44.4, -3.5, solid(P, "black"))
    m.round_box(hd, 0, 0, 3.2, 3.4, 46.4, 48.4, GOLD, cut=1)                                 # jewelled crown
    for j in range(5):
        spike(m, hd, (-2.4 + j * 1.2, 48.4, -2.6), (0, 1, 0), 0.9, 2.6 + (j == 2) * 2.0, GOLD, tip=0.8)
    m.box(hd, -0.6, 47.0, -3.6, 0.6, 48.2, -3.3, solid(P, "gem"))
    m.box(hd, -4.0, 22.0, 1.0, 4.0, 46.0, 4.0, strands(P, "silver", "silver_dark"))           # long silver hair
    hb = m.bone("halo", bd, (0, 44, 6))                                                  # sunburst halo
    for i in range(16):
        ang = 2 * math.pi * i / 16
        spike(m, hb, (0, 44.0, 7.0), (math.cos(ang), math.sin(ang), 0), 1.6, 10.0 + (i % 2) * 5.0, GOLD, tip=0.8)
    for i in range(12):
        ang = 2 * math.pi * i / 12
        m.box(hb, 9.0 * math.cos(ang) - 1.0, 44.0 + 9.0 * math.sin(ang) - 1.0, 6.4, 9.0 * math.cos(ang) + 1.0,
              44.0 + 9.0 * math.sin(ang) + 1.0, 7.6, GOLD)
    rb = m.bone("ring_coins", bd, (0, 36, 0))                                            # orbiting coin-seals
    for j in range(10):
        ang = 2 * math.pi * j / 10
        c = (20.0 * math.cos(ang), 36.0 + 8.0 * math.sin(ang * 2), 20.0 * math.sin(ang))
        m.round_box(rb, c[0], c[2], 1.4, 1.4, c[1] - 0.4, c[1] + 0.4, GOLD, cut=0)
    return m
