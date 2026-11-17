"""Cthyllamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the little eldritch ghost. A round blue ghostly body with a sly grin and narrow yellow eyes, two long
squiggly antennae, ragged violet bat wings, a black studded collar, a red skull on its belly, and a wispy tail
ending in a coiled cord. Ultimate stage, but small and mischievous.

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, ball
from _digidetail import leather, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a round blue ghostly body with a sly grin, narrow yellow eyes, long squiggly antennae, ragged violet bat wings, "
        "a studded collar and a red skull on its belly")
BASE = {"blue": (50, 70, 190), "blue_dark": (20, 30, 110), "blue_light": (110, 140, 240), "eye": (250, 220, 50),
        "mouth": (16, 16, 30), "violet": (150, 100, 210), "violet_dark": (80, 40, 140), "black": (30, 30, 36),
        "black_light": (90, 90, 100), "skull": (210, 40, 50), "steel": (200, 204, 216)}
SHINY = {"blue": (40, 140, 90), "blue_dark": (14, 80, 40), "blue_light": (120, 210, 160), "violet": (240, 120, 80)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = skin(P, "blue", dark="blue_dark", light="blue_light", var=0.03)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(y - 30.0 - sx * x * 0.25 + 1.0) < 0.5 and 1.0 < x * sx < 4.4:
                return p["eye"], p["eye"]
        zig = 26.0 + 0.5 * abs(((x * 1.2) % 2) - 1)
        if abs(x) < 4.0 and abs(y - zig) < 0.3:
            return tone(p["mouth"], face), None
        if math.hypot(x, y - 16.0) < 2.0 and not (abs(x) < 0.5 and y < 15.6):
            return tone(p["skull"], face), None
    return BLUE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cthyllamon")
    top = m.bone("cthyllamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 27.0, 0), 8.0, bodyf, layers=6)
    for r, y0, y1 in ((6.0, 12.0, 20.0), (4.0, 8.0, 12.0)):                      # ghostly lower body
        m.round_box(bd, 0, 0.4, r, r * 0.86, y0, y1, bodyf, cut=max(1, round(r * 0.3)))
    tl = m.bone("tail", bd, (0, 8, 2))                                           # wispy tail with coiled cord
    pts = [(0, 8.0, 2.0), (3.0, 4.0, 4.0), (7.0, 3.0, 5.0), (10.0, 4.0, 5.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 3 - j), BLUE, extend=0.4)
    for i in range(5):
        rod(m, tl, (10.0 + i * 1.0, 4.0 + (i % 2), 5.0), (11.0 + i * 1.0, 4.0 + ((i + 1) % 2), 5.0), 1,
            solid(P, "black"), extend=0)
    m.round_box(bd, 0, 0, 6.4, 5.6, 20.0, 21.4, leather(P, "black", "black_light", stitch="steel"), cut=2)  # collar
    hd = m.bone("head", bd, (0, 34, 0))
    for sx in (-1, 1):                                                           # squiggly antennae
        pts = [(sx * 2.0, 34.0, 0)] + [(sx * (3.0 + j * 2.0), 36.0 + j * 1.6 + (1.4 if j % 2 else -0.6), 0.6 * j)
                                      for j in range(1, 6)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, BLUE, extend=0.3)
    for side in (1, -1):                                                         # ragged violet bat wings
        bat_wing(m, bd, (side * 6.0, 26.0, 2.0), 18.0, 12.0, 4, solid(P, "violet_dark"), solid(P, "violet"),
                 side=side, sweep=10)
    return m
