"""Xiangpengmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the great sky-and-sea bird: a long blue-scaled fish body with a pale belly and a flowing pink
fin-tail trailing into foam, vast white-and-lilac feathered wings, a fierce crested bird head ringed by golden halo
hoops and a white cloud mane, a red ceremonial apron at its breast, and golden taloned legs. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing, slab_z
from _digidetail import fabric, feathers, fur, metal, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a great sky-and-sea bird with a long blue-scaled fish body, a pink fin-tail, vast white-and-lilac wings, golden halo hoops and a red apron"
BASE = {"blue": (70, 130, 220), "blue_dark": (30, 70, 150), "pale": (220, 230, 246), "pink": (240, 140, 190, 220),
        "white": (248, 248, 252), "white_dark": (190, 180, 230), "gold": (240, 200, 70), "gold_dark": (170, 130, 30),
        "red": (210, 40, 40), "red_dark": (130, 14, 14), "eye": (250, 220, 60), "beak": (240, 220, 200)}
SHINY = {"blue": (230, 150, 80), "blue_dark": (160, 90, 30), "pink": (140, 220, 200, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "down":
        return tone(p["pale"], face), None
    return scales(P, "blue", "blue_dark", size=1.2)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("xiangpengmon")
    top = m.bone("xiangpengmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    for i in range(8):
        z0 = -10.0 + i * 4.0
        r = max(1.6, 5.0 - abs(i - 2) * 0.6)
        slab_z(m, bd, 0, 22.0 - i * 0.4, z0, z0 + 4.2, r, r * 0.9, bodyf)
    tl = m.bone("tail", bd, (0, 19, 22))
    for j in range(5):                                                                  # flowing pink fin-tail
        spike(m, tl, (0, 19.0, 22.0), ((j - 2) * 0.3, (j - 2) * 0.25, 1), 2.4, 16.0, solid(P, "pink", glow=True), tip=0.8)
    hd = m.bone("head", bd, (0, 28, -10))
    ball(m, hd, (0, 30.0, -12.0), 3.4, feathers(P, "white", "white_dark"), layers=3)
    spike(m, hd, (0, 29.6, -15.0), (0, -0.4, -1), 1.6, 4.0, metal(P, "beak"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 3.0), 31.0, -14.6, max(sx * 1.6, sx * 3.0), 31.8, -14.2, solid(P, "eye", glow=True))
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.8, 33.0, -11.0), ((j - 2) * 0.3, 1, 0.4), 1.0, 6.0, solid(P, "gold"), tip=0.8)
    for k, (r, y) in enumerate(((4.4, 34.0), (3.4, 36.0))):                             # golden halo hoops
        for i in range(12):
            ang = i * 2 * math.pi / 12
            m.box(hd, r * math.cos(ang) - 0.5, y - 0.5 + k, -11.0 + r * math.sin(ang) - 0.5, r * math.cos(ang) + 0.5,
                  y + 0.5 + k, -11.0 + r * math.sin(ang) + 0.5, metal(P, "gold", dark="gold_dark"))
    for j in range(6):                                                                  # cloud mane
        ball(m, hd, ((j - 2.5) * 1.6, 28.0 - abs(j - 2.5) * 0.6, -8.0), 1.8, fur(P, "white", "white_dark"), layers=1)
    m.box(bd, -2.4, 12.0, -10.6, 2.4, 22.0, -9.6, fabric(P, "red", "red_dark"))           # red apron
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 25.0, -4.0))
        feather_wing(m, wb, (sx * 3.0, 25.0, -4.0), 30.0, 14.0, 3, feathers(P, "white", "white_dark"), side=sx,
                     sweep=30, droop=-10.0)
        lg = m.bone("leg_" + ("left" if sx > 0 else "right"), bd, (sx * 2.4, 17.0, -4.0))
        rod(m, lg, (sx * 2.4, 17.0, -4.0), (sx * 3.0, 6.0, -5.0), 1, metal(P, "gold"), extend=0.3)
        for t in range(3):
            spike(m, lg, (sx * 3.0, 6.0, -5.0), ((t - 1) * 0.5, -0.6, -1), 0.9, 3.0, metal(P, "gold"), tip=0.8)
    return m
