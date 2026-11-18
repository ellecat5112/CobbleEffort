"""Kokuwamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Kokuwamon awakened by the X-Antibody: a sleek steel-blue jet fighter with a stag-beetle pincer nose,
swept wings and tailfins, yellow thrusters and red lights along its armoured hull, trailing a rainbow streak. Child
stage, 1 block long.

Front is -z, y is up. 18 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(1.0, HEIGHT, 2.6)
KIND = "floater"
K = 4
LOOK = "a sleek steel-blue jet fighter with a stag-beetle pincer nose, swept wings, yellow thrusters and red lights"
BASE = {"blue": (90, 110, 150), "blue_dark": (30, 40, 70), "blue_light": (170, 190, 230), "yellow": (240, 210, 60),
        "red": (220, 40, 40), "silver": (210, 214, 224), "silver_dark": (100, 104, 116)}
SHINY = {"blue": (150, 90, 160), "blue_dark": (70, 30, 80), "blue_light": (230, 170, 230)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "blue", "blue_dark", light="blue_light", trim="red", trim_w=0.2)


def build():
    m = Model("kokuwamonxantibody")
    top = m.bone("kokuwamonxantibody", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    for i in range(6):
        r = 2.6 + 0.8 * math.sin(math.pi * (i + 0.5) / 6)
        slab_z(m, bd, 0, 9.0, -8.0 + i * 3.0, -4.6 + i * 3.0, r, r * 0.8, HULL)
    hd = m.bone("head", bd, (0, 9, -9))
    for sx in (-1, 1):                                                               # pincer nose
        pts = [(sx * 1.4, 9.6, -8.0), (sx * 2.4, 10.4, -12.0), (sx * 0.8, 10.0, -14.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, HULL, extend=0.3, t2=2)
        m.round_box(hd, sx * 1.6, -6.0, 0.4, 0.6, 10.4, 11.4, solid(P, "red", glow=True), cut=0)
    for side in (1, -1):                                                             # swept wings + tailfins
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.4, 9.0, 0))
        x0, x1 = sorted((side * 2.4, side * 12.0))
        m.box(wb, x0, 8.6, -1.0, x1, 9.4, 4.0, HULL, rotation=(0, side * -30, 0), pivot=(side * 2.4, 9.0, 0))
        x0, x1 = sorted((side * 1.6, side * 6.0))
        m.box(wb, x0, 9.0, 7.0, x1, 9.8, 10.0, HULL, rotation=(0, side * -30, side * -30), pivot=(side * 1.6, 9.0, 7.0))
        m.round_box(wb, side * 2.0, 10.4, 1.0, 1.4, 6.6, 8.6, metal(P, "yellow", dark="silver_dark"), cut=0)  # thrusters
    return m
