"""Huankunmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
fish that becomes a bird: a great koi-like fish with teal scales and a cream belly, a whiskered face with golden eyes,
long pink feathered pectoral fins spread like wings and a split feathery tail of pink and white plumes. 25 blocks.

Front is -z, y is up. 40 units long; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import fan, feather_wing, slab_z
from _digidetail import feathers, scales, skin, solid, strands
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a great koi-like fish with teal scales, a whiskered face, long pink feathered fins spread like wings and a plumed tail"
BASE = {"teal": (60, 170, 170), "teal_dark": (20, 90, 100), "teal_light": (150, 230, 220), "cream": (246, 236, 210),
        "cream_dark": (200, 180, 150), "pink": (240, 140, 180), "pink_dark": (190, 70, 120), "white": (250, 250, 250),
        "eye": (250, 200, 40), "pupil": (20, 20, 24), "whisker": (240, 220, 160)}
SHINY = {"teal": (230, 170, 60), "teal_dark": (150, 90, 14), "teal_light": (255, 230, 150), "pink": (130, 170, 250),
         "pink_dark": (60, 90, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SC = scales(P, "teal", "teal_dark", size=1.6, light="teal_light", belly_key="cream", belly=lambda x, y, z, f: y < 7.0)
FEATH = feathers(P, "pink", "pink_dark", tip="white")


def build():
    m = Model("huankunmon")
    top = m.bone("huankunmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    n = 10
    for i in range(n):                                                              # fish body, front to back
        t = (i + 0.5) / n
        r = 7.0 * math.sin(math.pi * (0.15 + 0.8 * t)) + 1.0
        slab_z(m, bd, 0, 10.0, -18.0 + i * 3.6, -18.0 + (i + 1) * 3.6 + 0.3, r * 0.75, r, SC)
    hd = m.bone("head", bd, (0, 10, -16))
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.4, -14.0, 0.4, 1.4, 11.0, 13.6, solid(P, "eye", glow=False), cut=0)
        m.round_box(hd, sx * 4.6, -14.2, 0.3, 0.6, 11.8, 12.8, solid(P, "pupil"), cut=0)
        pts = [(sx * 1.6, 8.4, -18.6), (sx * 5.0, 6.0, -22.0), (sx * 9.0, 5.0, -24.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "whisker"), extend=0.2, t2=1)
    m.round_box(hd, 0, -18.6, 2.4, 0.8, 7.0, 9.4, solid(P, "pink_dark"), cut=0)
    for side in (1, -1):                                                            # pectoral feather wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 5.0, 9.0, -8.0))
        feather_wing(m, wb, (side * 5.0, 9.0, -8.0), 22.0, 10.0, 3, FEATH, side=side, sweep=25, droop=-4.0)
    for j in range(6):                                                              # dorsal fin
        spike(m, bd, (0, 17.0, -8.0 + j * 3.0), (0, 1, 0.8), 1.4, 5.0 - abs(j - 2) * 0.6, FEATH, tip=0.8)
    tb = m.bone("tail", bd, (0, 10, 18))
    for sy in (-1, 1):                                                              # split plumed tail
        for j in range(4):
            spike(m, tb, (0, 10.0 + sy * 1.0, 18.0), ((j - 1.5) * 0.3, sy * (0.6 + j * 0.2), 1), 1.8, 14.0 - j * 2.0,
                  FEATH, tip=0.8)
    return m
