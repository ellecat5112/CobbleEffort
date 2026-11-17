"""Citramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
anime art on wikimon.net): the citrus muscleman. A big round orange fruit body with dimpled peel and a little green
leaf on a stalk, wraparound red sunglasses, a wide shouting mouth, and two muscular red arms flexed overhead.
15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import Bulge, cutout, local, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a big round orange fruit with a leaf on top, red sunglasses, a shouting mouth and two muscular red arms flexed overhead"
BASE = {"orange": (246, 140, 30), "orange_dark": (200, 90, 10), "orange_light": (255, 200, 110), "red": (200, 40, 30),
        "red_dark": (120, 14, 10), "red_light": (250, 110, 90), "glass": (220, 30, 30), "frame": (250, 230, 230),
        "mouth": (80, 20, 20), "tongue": (230, 90, 100), "leaf": (80, 170, 60), "stalk": (110, 80, 40)}
SHINY = {"orange": (250, 230, 60), "orange_dark": (210, 180, 10), "orange_light": (255, 250, 170)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = skin(P, "red", dark="red_dark", light="red_light", var=0.03,
           bulges=[Bulge("north", sx * 11.0, 30.0, 2.0, 3.6, light=0.35, shadow=0.45) for sx in (-1, 1)])


def peelf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 21.6 < y < 24.0 and abs(x) < 6.6:
            return tone(p["frame"] if abs(y - 22.8) > 0.9 or abs(x) > 6.0 else p["glass"], face), None
        if 14.0 < y < 19.6 and abs(x) < 3.4 - max(0.0, 17.0 - y) * 0.4:
            return tone(p["tongue"] if y < 15.6 else p["mouth"], face), None
    if (math.sin(x * 2.4) * math.sin(y * 2.1) * math.sin(z * 2.3)) > 0.6:
        return tone(p["orange_dark"], face), None                        # dimpled peel
    return skin(P, "orange", dark="orange_dark", light="orange_light", var=0.04)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("citramon")
    top = m.bone("citramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 19.0, 0), 10.0, peelf, layers=8)
    hd = m.bone("head", bd, (0, 29, 0))
    rod(m, hd, (0, 28.6, 0), (0, 31.0, 0), 1, solid(P, "stalk"), extend=0)
    m.box(hd, 0.0, 30.0, -0.2, 5.0, 33.0, 0.2, solid(P, "leaf"), rotation=(0, 0, 20), pivot=(0, 30.0, 0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                  # muscular arms flexed overhead
        ab = m.bone(nm, bd, (sx * 9.0, 22.0, 0))
        rod(m, ab, (sx * 9.0, 22.0, 0), (sx * 14.0, 30.0, -1.0), 5, ARM, extend=0.6)
        rod(m, ab, (sx * 14.0, 30.0, -1.0), (sx * 10.0, 37.0, -1.0), 4, ARM, extend=0.6)
        m.round_box(ab, sx * 9.6, -1.0, 2.6, 2.6, 36.0, 40.0, ARM, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 10.0, 0))
        rod(m, lg, (sx * 4.0, 11.0, 0), (sx * 4.4, 2.0, 0), 4, ARM, extend=0.5)
        m.box(lg, sx * 4.4 - 2.4, 0.0, -3.4, sx * 4.4 + 2.4, 2.4, 1.6, solid(P, "red_dark"))
    return m
