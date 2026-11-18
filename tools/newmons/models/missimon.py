"""Missimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little living missile: a pointed blue nose cone with one big red eye, a green armoured body with a
segmented flexible tail, steel fins swept back, a spiked claw underneath and a blue rocket flame at its tail. 0.5
blocks tall.

Front is -z, y is up. 16 units long; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, cutout, flame_inside, local, metal, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a little living missile with a blue nose cone and one big red eye, a green body, steel fins and a blue rocket flame"
BASE = {"blue": (50, 70, 190), "blue_dark": (20, 30, 110), "green": (90, 120, 60), "green_dark": (40, 60, 24),
        "steel": (200, 204, 214), "steel_dark": (100, 104, 116), "eye": (220, 40, 40), "flame": (150, 170, 255, 200),
        "flame_core": (230, 236, 255, 230)}
SHINY = {"blue": (200, 60, 60), "blue_dark": (110, 20, 20), "green": (200, 200, 210), "green_dark": (120, 120, 130)}


def P(v):
    return pal(BASE, SHINY, v)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) > 0.6 else p["flame"]
    return c, c[:3]


def build():
    m = Model("missimon")
    top = m.bone("missimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, -2.0, 4.0, 4.0, 6.0, 12.0, armour(P, "blue", "blue_dark"), cut=1)  # nose cone
    spike(m, bd, (0, 9.0, -5.8), (0, 0, -1), 5.0, 6.0, armour(P, "blue", "blue_dark"), tip=0.8)
    m.round_box(bd, 0, -6.1, 2.2, 0.4, 9.0, 11.4, solid(P, "eye", glow=True), cut=0)
    for j in range(4):                                                                   # segmented body
        m.round_box(bd, 0, 3.0 + j * 2.0, 2.4 - j * 0.3, 1.0, 6.4 + j * 0.4, 10.4 - j * 0.4,
                    armour(P, "green", "green_dark"), cut=0)
    for sx in (-1, 1):                                                                   # swept steel fins
        x0, x1 = sorted((sx * 2.0, sx * 9.0))
        m.box(bd, x0, 10.0, 1.0, x1, 10.6, 6.0, metal(P, "steel", dark="steel_dark"),
              rotation=(0, sx * 25, sx * 10), pivot=(sx * 2.0, 10.3, 2.0))
    spike(m, bd, (0, 6.0, 2.0), (0, -1, -0.5), 1.4, 3.0, metal(P, "steel"), tip=0.8)        # claw underneath
    for ang in (0, 90):                                                                  # rocket flame
        m.box(bd, -1.6, 7.0, 11.0, 1.6, 9.6, 16.0, cutout(flame_inside(3, 0.0, 1), firef), rotation=(0, 0, ang),
              pivot=(0, 8.3, 11.0))
    return m
