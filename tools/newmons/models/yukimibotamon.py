"""Yukimi Botamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little puff of snow: a soft white blob with two round bear ears, shiny black eyes, pink cheeks
and a cat mouth. 0.35 blocks.

Front is -z, y is up. Baby I stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 13
SCALE, HITBOX = sized(0.35, HEIGHT, 1.6)
KIND = "biped"
K = 4
LOOK = "a little puff of snow with round bear ears, shiny black eyes, pink cheeks and a cat mouth"
BASE = {"snow": (250, 252, 255), "snow_dark": (200, 214, 236), "eye": (20, 20, 26), "white": (255, 255, 255),
        "pink": (250, 180, 190)}
SHINY = {"snow": (250, 236, 200), "snow_dark": (220, 196, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            d = math.hypot(a - sx * 2.2, b - 6.0)
            if d < 1.1:
                return (p["white"] if math.hypot(a - sx * 2.2 + 0.4, b - 6.4) < 0.35 else p["eye"]), None
            if math.hypot(a - sx * 3.6, b - 4.4) < 0.8:
                return p["pink"], None
        if abs(b - 4.0) < 0.25 and abs(a) < 1.0:
            return p["eye"], None
    return skin(P, "snow", dark="snow_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yukimibotamon")
    top = m.bone("yukimibotamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 1, 0))
    ball(m, bd, (0, 6.0, 0), 5.6, bodyf, layers=5, squash=0.8)
    for sx in (-1, 1):
        ball(m, bd, (sx * 4.0, 10.6, 0), 2.0, bodyf, layers=2, squash=0.6)
    return m
