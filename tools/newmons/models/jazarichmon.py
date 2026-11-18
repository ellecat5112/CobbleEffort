"""Jazarichmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the jet machine dragon: a long sleek black-and-navy fighter-jet dragon with a sharp crested head
and red eyes, swept delta wings edged in cyan, cyan tailplanes, a long tail ending in a cyan-lit spearhead and
long folded legs with blade talons hanging beneath. 25 blocks long.

Front is -z, y is up. 30 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a long sleek black fighter-jet dragon with a crested head, cyan-edged delta wings, a spear tail and folded legs"
BASE = {"black": (40, 42, 56), "black_dark": (12, 12, 20), "black_light": (110, 114, 140), "navy": (40, 50, 130),
        "navy_dark": (14, 18, 60), "cyan": (90, 230, 250), "cyan_light": (220, 255, 255), "eye": (240, 40, 40),
        "silver": (200, 204, 216), "silver_dark": (90, 94, 106)}
SHINY = {"black": (220, 222, 232), "black_dark": (140, 144, 160), "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "black", "black_dark", light="black_light", trim="navy", trim_w=0.25)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 18.0 or z > 6.0:
        return tone(p["cyan"], face), None
    return HULL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jazarichmon")
    top = m.bone("jazarichmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    for i in range(8):                                                               # sleek fuselage
        t = (i + 0.5) / 8
        r = 4.6 * math.sin(math.pi * (0.2 + 0.7 * t)) + 0.6
        slab_z(m, bd, 0, 18.0, -14.0 + i * 3.6, -14.0 + (i + 1) * 3.6 + 0.3, r, r * 0.8, HULL)
    hd = m.bone("head", bd, (0, 20, -14))
    m.round_box(hd, 0, -17.0, 2.2, 4.0, 18.0, 22.0, HULL, cut=1)
    spike(m, hd, (0, 19.6, -21.0), (0, -0.2, -1), 2.0, 4.0, HULL, tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.8, sx * 2.3), 20.4, -19.0, max(sx * 1.8, sx * 2.3), 21.4, -17.4, solid(P, "eye", glow=True))
    for j in range(4):
        spike(m, hd, (0, 21.8, -16.0 + j * 1.6), (0, 0.6, 1), 1.2, 5.0 - j * 0.6, HULL, tip=0.8)
    for side in (1, -1):                                                             # delta wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 19.0, -2.0))
        for j in range(5):
            x0, x1 = sorted((side * 3.0, side * (22.0 - j * 3.0)))
            m.box(wb, x0, 19.0, -6.0 + j * 2.4, x1, 20.0, -3.6 + j * 2.4, wingf,
                  rotation=(0, side * -25, side * -10), pivot=(side * 3.0, 19.0, -2.0))
        x0, x1 = sorted((side * 2.0, side * 9.0))
        m.box(wb, x0, 19.0, 12.0, x1, 20.0, 15.0, wingf, rotation=(0, side * -30, side * -20), pivot=(side * 2.0, 19.0, 12.0))
    tb = m.bone("tail", bd, (0, 18, 14))                                              # long spear tail
    pts = [(0, 18.0, 14.0), (0, 14.0, 22.0), (0, 10.0, 30.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, HULL, extend=0.3, t2=2)
    spike(m, tb, pts[-1], (0, -0.4, 1), 2.0, 5.0, gem(P, "cyan", "cyan_light"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # folded legs
        lg = m.bone(nm, bd, (sx * 3.0, 15.0, 2.0))
        rod(m, lg, (sx * 3.0, 15.0, 2.0), (sx * 4.0, 8.0, 0.0), 2, armour(P, "navy", "navy_dark"), extend=0.4)
        rod(m, lg, (sx * 4.0, 8.0, 0.0), (sx * 4.0, 2.0, 3.0), 1, metal(P, "silver", dark="silver_dark"), extend=0.3, t2=2)
        for j in range(3):
            spike(m, lg, (sx * 4.0 + (j - 1) * 1.0, 1.6, 3.0), ((j - 1) * 0.4, -1, -0.4), 0.9, 4.0, armour(P, "navy", "navy_dark"),
                  tip=0.8)
    return m
