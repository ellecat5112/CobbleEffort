"""Tomorimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little will-o'-the-wisp: a soft sky-blue blob with one huge pink eye and a tiny fanged mouth,
wrapped in flickering pale-blue flame edged with wisps of black. 0.35 blocks.

Front is -z, y is up. Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, plane, skin, solid
from _route import pal, tone

HEIGHT = 19
SCALE, HITBOX = sized(0.35, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a little sky-blue blob with one huge pink eye wrapped in flickering pale-blue flame edged with black"
BASE = {"blue": (150, 210, 250), "blue_dark": (80, 150, 220), "eye": (230, 60, 140), "pupil": (60, 10, 40),
        "white": (255, 255, 255), "flame": (140, 220, 255, 200), "black": (20, 20, 30), "fang": (255, 255, 255)}
SHINY = {"blue": (250, 180, 120), "blue_dark": (220, 120, 60), "flame": (255, 190, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        c = eye(p, a + 0.4, b - 8.0, 2.2, "eye")
        if c is not None:
            return c, None
        if abs(b - 4.6) < 0.25 and abs(a) < 0.8:
            return p["black"], None
    return skin(P, "blue", dark="blue_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tomorimon")
    top = m.bone("tomorimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 7.0, 0), 5.0, bodyf, layers=5, squash=0.8, ry=4.0)
    fl = m.bone("flame", bd, (0, 8, 2))
    for j in range(8):
        ang = (j - 3.5) * 0.4
        spike(m, fl, (math.sin(ang) * 4.6, 8.0 + math.cos(ang) * 2.0, 2.6), (math.sin(ang) * 0.6, 1, 0.3), 2.4,
              6.0 + 4.0 * math.cos(ang), solid(P, "flame", glow=True), tip=0.8)
    for j in range(3):
        spike(m, fl, (3.0 + j * 1.2, 12.0, 3.4), (0.4, 1, 0.2), 0.9, 7.0 + j * 2.0, solid(P, "black"), tip=0.8)
    return m
