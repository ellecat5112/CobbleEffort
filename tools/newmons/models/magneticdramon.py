"""Magneticdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the magnet dragon: a great black-rock dragon body seamed with crackling yellow lightning, two
long serpent heads on lightning-wreathed necks, horseshoe-magnet claw arms with red-and-blue poles, a cluster of
copper coil cylinders on its back, golden claws and black gold-ringed halos floating round it. 35 blocks tall.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a great black-rock dragon seamed with yellow lightning, two serpent heads, horseshoe-magnet claws, copper coil cylinders and golden claws"
BASE = {"rock": (50, 46, 50), "rock_dark": (16, 14, 18), "rock_light": (110, 104, 110), "bolt": (255, 230, 60),
        "copper": (210, 130, 60), "copper_dark": (130, 70, 20), "red": (220, 40, 50), "blue": (60, 110, 230),
        "gold": (250, 210, 60), "gold_dark": (170, 120, 10), "eye": (240, 40, 60), "white": (240, 240, 240)}
SHINY = {"bolt": (120, 220, 255), "gold": (200, 220, 255), "gold_dark": (100, 130, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def rockf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    s = math.sin(x * 1.2 + y * 0.8) + math.sin(y * 1.0 - z * 1.1)
    if abs(s) < 0.15:
        return tone(p["bolt"], face), p["bolt"]
    return armour(P, "rock", "rock_dark", light="rock_light")(x, y, z, face, variant, box=box, **k)


BOLT = solid(P, "bolt", glow=True)


def build():
    m = Model("magneticdramon")
    top = m.bone("magneticdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 2.0, 9.0, 8.0, 14.0, 32.0, rockf, cut=3)
    for k_, sx in enumerate((-1, 1)):                                                  # two serpent heads
        nb = m.bone("neck_left" if sx > 0 else "neck_right", bd, (sx * 4.0, 30.0, -4.0))
        pts = [(sx * 4.0, 30.0, -4.0), (sx * 10.0, 38.0, -6.0), (sx * 12.0, 46.0, -4.0), (sx * 10.0, 50.0, -8.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, nb, p0, p1, 2, rockf, extend=0.6)
            rod(m, nb, (p0[0] + sx * 2.0, p0[1], p0[2]), (p1[0] + sx * 2.0, p1[1], p1[2]), 1, BOLT, extend=0, t2=1)
        e = pts[-1]
        m.round_box(nb, e[0], e[2] - 2.0, 2.0, 4.0, e[1] - 1.6, e[1] + 1.6, armour(P, "rock", "rock_dark"), cut=1)
        m.box(nb, min(e[0] + sx * 1.9, e[0] + sx * 2.2), e[1] + 0.2, e[2] - 4.0, max(e[0] + sx * 1.9, e[0] + sx * 2.2), e[1] + 1.0,
              e[2] - 2.8, solid(P, "eye", glow=True))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # horseshoe-magnet claws
        ab = m.bone(nm, bd, (sx * 9.0, 26.0, -2.0))
        rod(m, ab, (sx * 9.0, 26.0, -2.0), (sx * 16.0, 22.0, -6.0), 3, rockf, extend=0.6)
        c = (sx * 18.0, 18.0, -8.0)
        for i in range(7):
            a0, a1 = math.pi * i / 7, math.pi * (i + 1) / 7
            rod(m, ab, (c[0] + 4.0 * math.cos(a0), c[1] + 4.0 * math.sin(a0), c[2]), (c[0] + 4.0 * math.cos(a1),
                c[1] + 4.0 * math.sin(a1), c[2]), 2, rockf, extend=0.3)
        m.round_box(ab, c[0] - 4.0, c[2], 1.6, 1.6, c[1] - 3.0, c[1], solid(P, "red"), cut=0)
        m.round_box(ab, c[0] + 4.0, c[2], 1.6, 1.6, c[1] - 3.0, c[1], solid(P, "blue"), cut=0)
    for j in range(4):                                                               # copper coil cylinders
        rod(m, bd, (-4.0 + j * 2.6, 28.0, 6.0), (-6.0 + j * 4.0, 36.0, 14.0), 2, metal(P, "copper", dark="copper_dark"), extend=0)
        m.round_box(bd, -6.0 + j * 4.0, 14.4, 1.6, 1.6, 35.4, 36.6, solid(P, "rock_dark"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # golden-clawed legs
        lg = m.bone(nm, top, (sx * 5.0, 16.0, 0))
        rod(m, lg, (sx * 5.0, 16.0, 0), (sx * 7.0, 6.0, -2.0), 3, rockf, extend=0.6)
        for j in range(3):
            spike(m, lg, (sx * 7.0 + (j - 1) * 1.6, 5.0, -3.0), (0, -0.6, -1), 1.4, 5.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    rb = m.bone("ring_halos", bd, (0, 24, 0))                                          # floating halos
    for k_ in range(4):
        ang = 2 * math.pi * k_ / 4
        c = (16.0 * math.cos(ang), 40.0, 16.0 * math.sin(ang))
        for i in range(8):
            a0, a1 = 2 * math.pi * i / 8, 2 * math.pi * (i + 1) / 8
            rod(m, rb, (c[0] + 2.0 * math.cos(a0), c[1] + 2.0 * math.sin(a0), c[2]), (c[0] + 2.0 * math.cos(a1),
                c[1] + 2.0 * math.sin(a1), c[2]), 1, solid(P, "gold"), extend=0.1, t2=1)
    return m
