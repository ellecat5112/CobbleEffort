"""Zanbamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a centaur samurai of the battlefield: a black horse-like lower body barded in gold, an armoured
samurai torso in gold and black with a horned kabuto, a great streaming mane of red and orange flame-hair, and a long
golden zanbato blade held low in both hands. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 42
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a centaur samurai with a black horse body barded in gold, a horned gold kabuto, a great flame-coloured mane and a long golden zanbato"
BASE = {"black": (40, 36, 40), "black_dark": (14, 12, 14), "gold": (240, 196, 60), "gold_dark": (170, 120, 20),
        "red": (220, 60, 30), "orange": (250, 150, 40), "steel": (230, 220, 160), "eye": (255, 230, 100)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (120, 130, 160), "red": (70, 120, 230), "orange": (130, 190, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", trim="black", panel=(3.0, 3.0))
BLACK = skin(P, "black", dark="black_dark")


def build():
    m = Model("zanbamon")
    top = m.bone("zanbamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(6):
        z0 = -10.0 + i * 3.6
        slab_z(m, bd, 0, 16.0, z0, z0 + 3.8, 4.6, 4.6, GOLD if i in (0, 1, 5) else BLACK)
    for sx, sz, nm in ((1, -8.0, "leg_front_left"), (-1, -8.0, "leg_front_right"), (1, 8.0, "leg_back_left"),
                       (-1, 8.0, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 3.0, 13.0, sz))
        rod(m, lg, (sx * 3.0, 13.0, sz), (sx * 3.2, 5.0, sz - 0.6), 2, BLACK, extend=0.4)
        rod(m, lg, (sx * 3.2, 5.0, sz - 0.6), (sx * 3.2, 1.6, sz), 2, GOLD, extend=0.4)
        m.round_box(lg, sx * 3.2, sz - 0.4, 1.6, 1.8, 0.0, 1.8, solid(P, "black_dark"), cut=0)
    tor = m.bone("torso", bd, (0, 20, -9))
    m.round_box(tor, 0, -9.0, 4.4, 3.4, 20.0, 31.0, GOLD, cut=1)
    for sx in (-1, 1):
        m.round_box(tor, sx * 6.0, -9.0, 2.6, 2.8, 28.0, 32.0, GOLD, cut=1)
    hd = m.bone("head", tor, (0, 32, -9))
    m.round_box(hd, 0, -9.0, 2.6, 2.8, 32.0, 38.0, BLACK, cut=1)
    m.box(hd, -2.2, 34.6, -12.0, 2.2, 35.4, -11.7, solid(P, "eye", glow=True))
    m.round_box(hd, 0, -9.0, 3.4, 3.4, 37.0, 39.4, metal(P, "gold", dark="gold_dark"), cut=1)   # kabuto
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 39.0, -11.0), (sx * 0.5, 1, -0.3), 1.0, 5.0, metal(P, "gold"), tip=0.8)
    for j in range(9):                                                                  # flame mane
        ang = (j - 4) * 0.3
        spike(m, hd, (math.sin(ang) * 2.4, 38.0, -7.0), (math.sin(ang) * 0.6, 0.6, 1), 2.0, 14.0 - abs(j - 4),
              strands(P, "red" if j % 2 else "orange", "red"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, tor, (sx * 6.0, 29.0, -9.0))
        rod(m, ab, (sx * 6.0, 29.0, -9.0), (sx * 3.0, 22.0, -15.0), 2, GOLD, extend=0.4)
    zb = m.bone("zanbato", tor, (0, 22, -15))
    m.box(zb, -0.6, 21.0, -16.0, 0.6, 23.0, -12.0, solid(P, "black"))
    m.box(zb, -0.6, 21.0, -40.0, 0.6, 24.6, -16.0, metal(P, "steel"), rotation=(-12, 25, 0), pivot=(0, 22.0, -16.0))
    return m
