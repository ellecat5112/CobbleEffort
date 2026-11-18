"""Mail Birdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the armoured bird-dragon: a sleek navy-blue armoured flying dragon with a swept wedge head and red eye, red-tipped
spikes, big swept armour wings, a silver segmented spined tail, and clawed legs tucked beneath. 15 blocks long.

Front is -z, y is up. 28 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a sleek navy-blue armoured flying dragon with a swept wedge head, big swept armour wings, red-tipped spikes and a silver spined tail"
BASE = {"navy": (40, 70, 170), "navy_dark": (14, 26, 90), "navy_light": (120, 150, 230), "silver": (210, 214, 226),
        "silver_dark": (100, 104, 120), "red": (220, 40, 40), "eye": (240, 40, 40), "black": (30, 30, 34)}
SHINY = {"navy": (200, 60, 50), "navy_dark": (110, 14, 10), "navy_light": (250, 150, 130)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "navy", "navy_dark", light="navy_light", trim="silver", trim_w=0.2)
SIL = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("mailbirdramon")
    top = m.bone("mailbirdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(5):
        r = 4.0 * math.sin(math.pi * (i + 0.5) / 5) + 1.0
        slab_z(m, bd, 0, 16.0, -8.0 + i * 3.4, -4.6 + i * 3.4, r, r * 0.9, ARM)
    hd = m.bone("head", bd, (0, 18, -9))
    m.round_box(hd, 0, -12.0, 2.4, 4.0, 16.0, 20.0, ARM, cut=1)
    spike(m, hd, (0, 18.0, -16.0), (0, 0, -1), 2.0, 4.0, ARM, tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.3, sx * 2.6), 18.6, -14.0, max(sx * 2.3, sx * 2.6), 19.4, -12.6, solid(P, "eye", glow=True))
    spike(m, hd, (0, 20.0, -10.0), (0, 0.6, 1), 1.6, 6.0, ARM, tip=0.8)
    for side in (1, -1):                                                             # swept armour wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 19.0, -2.0))
        for j in range(4):
            x0, x1 = sorted((side * 3.0, side * (20.0 - j * 3.0)))
            m.box(wb, x0, 19.0, -6.0 + j * 2.6, x1, 20.4, -3.6 + j * 2.6, ARM, rotation=(0, side * -25, side * -15),
                  pivot=(side * 3.0, 19.0, -2.0))
        spike(m, wb, (side * 18.0, 22.0, -8.0), (side * 0.6, 0.2, -1), 1.2, 4.0, solid(P, "red"), tip=0.8)
    tb = m.bone("tail", bd, (0, 15, 9))                                              # silver spined tail
    pts = [(0, 15.0, 9.0), (0, 13.0, 16.0), (2.0, 11.0, 23.0), (4.0, 10.0, 30.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 2 - j // 2, SIL, extend=0.4)
        spike(m, tb, p1, (0, 1, 0.3), 0.9, 2.0, SIL, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.4, 13.0, 2.0))
        rod(m, lg, (sx * 2.4, 13.0, 2.0), (sx * 3.0, 6.0, 4.0), 1, ARM, extend=0.3, t2=2)
        for j in range(3):
            spike(m, lg, (sx * 3.0 + (j - 1) * 0.8, 5.6, 3.6), (0, -1, -0.4), 0.8, 2.4, solid(P, "black"), tip=0.8)
    return m
