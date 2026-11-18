"""Rhino Kabuterimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the hybrid beast-spirit of thunder: a colossal rhinoceros-beetle tank: a deep navy-violet
domed carapace edged in rust-red, a huge golden curved horn sweeping up from its head, smaller golden horns flanking it,
and six thick navy legs ending in great golden spiked cuffs. 25 blocks.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 5}
LOOK = "a colossal rhino-beetle tank with a navy-violet domed carapace edged in rust-red, a huge golden curved horn and golden spiked leg cuffs"
BASE = {"navy": (70, 70, 150), "navy_dark": (24, 24, 70), "rust": (150, 70, 50), "rust_dark": (80, 30, 20),
        "gold": (240, 210, 120), "gold_dark": (170, 130, 50), "eye": (250, 220, 60), "black": (24, 22, 28)}
SHINY = {"navy": (40, 120, 70), "navy_dark": (14, 60, 30), "gold": (220, 224, 236), "gold_dark": (140, 144, 160)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "navy", "navy_dark", trim="rust", trim_w=0.4)
GOLD = armour(P, "gold", "gold_dark")


def build():
    m = Model("rhinokabuterimon")
    top = m.bone("rhinokabuterimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    for i in range(6):                                                                   # domed carapace
        r = 12.0 - i * 1.6
        m.round_box(bd, 0, 2.0, r, r * 1.2, 12.0 + i * 3.0, 15.0 + i * 3.0, SHELL, cut=max(1, round(r * 0.35)))
    for sx in (-1, 1):
        for j in range(3):
            spike(m, bd, (sx * 10.0, 22.0 - j * 2.0, -6.0 + j * 7.0), (sx * 1, 0.5, 0), 2.0, 5.0,
                  armour(P, "rust", "rust_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 20, -14))
    m.round_box(hd, 0, -15.0, 5.0, 3.0, 16.0, 23.0, SHELL, cut=1)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.0, sx * 3.2))
        m.box(hd, x0, 19.0, -18.2, x1, 20.0, -17.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 4.0, 22.0, -14.0), (sx * 0.6, 1, -0.3), 2.0, 7.0, GOLD, tip=0.8)
    pts = [(0, 22.0, -16.0), (0, 30.0, -22.0), (0, 40.0, -20.0), (0, 44.0, -12.0)]       # huge curved horn
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 6 - i * 2, GOLD, extend=0.8)
    spike(m, hd, pts[-1], (0, 0.2, 1), 1.6, 4.0, GOLD, tip=0.8)
    for sx in (-1, 1):                                                                   # six legs
        for j, zz in enumerate((-8.0, 0.0, 8.0)):
            nm = f"leg_{('front', 'mid', 'back')[j]}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 9.0, 14.0, zz))
            rod(m, lg, (sx * 9.0, 14.0, zz), (sx * 14.0, 6.0, zz), 4, SHELL, extend=0.6)
            m.round_box(lg, sx * 14.0, zz, 3.6, 3.6, 0.0, 6.0, GOLD, cut=1)
            spike(m, lg, (sx * 14.0, 6.0, zz - 3.0), (sx * 0.3, 0.6, -1), 1.6, 5.0, GOLD, tip=0.8)
    return m
