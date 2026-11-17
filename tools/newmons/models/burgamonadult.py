"""Burgamon Adult (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the burger chef duo. Two round-faced little cooks with onion-bulb heads standing side
by side: one in a white chef's jacket with a blue scarf, flipping a towering cheeseburger on a big spatula, the other
in a violet smock hoisting a giant red sausage. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = ("two round-faced onion-headed cooks side by side: one in a chef's jacket flipping a towering cheeseburger, "
        "the other in a violet smock hoisting a giant sausage")
BASE = {"onion": (226, 160, 90), "onion_dark": (170, 100, 40), "onion_light": (250, 210, 150), "face": (252, 230, 200),
        "face_dark": (220, 190, 150), "eye": (30, 20, 20), "white": (250, 250, 250), "white_dark": (200, 204, 214),
        "blue": (70, 150, 220), "violet": (150, 110, 190), "violet_dark": (90, 60, 130), "bun": (180, 100, 40),
        "bun_light": (226, 150, 80), "lettuce": (110, 190, 60), "patty": (110, 60, 30), "cheese": (250, 200, 50),
        "sausage": (220, 40, 40), "sausage_light": (255, 120, 110), "steel": (200, 204, 216),
        "steel_dark": (100, 104, 116), "handle": (40, 120, 160), "seed": (250, 240, 210)}
SHINY = {"onion": (180, 120, 200), "onion_dark": (120, 60, 140), "onion_light": (230, 190, 240), "violet": (90, 170, 110),
         "violet_dark": (40, 110, 60), "blue": (230, 120, 60)}


def P(v):
    return pal(BASE, SHINY, v)


FACE = skin(P, "face", dark="face_dark", var=0.03)
ONION = skin(P, "onion", dark="onion_dark", light="onion_light", var=0.04)


def facef(cx):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if abs(x - cx - sx * 1.6) < 0.5 and abs(y - 19.0) < 0.7:
                    return tone(p["eye"], face), None
            if abs(y - 17.0 + 0.2 * (x - cx) ** 2) < 0.2 and abs(x - cx) < 1.0:
                return tone(p["eye"], face), None
        return FACE(x, y, z, face, variant, box=box, **k)
    return s


def cook(m, bd, cx, coat):
    """One cook: a round body in its coat, an onion-bulb head with a face, stubby legs."""
    m.round_box(bd, cx, 0, 4.2, 3.6, 4.0, 14.0, coat, cut=1)
    ball(m, bd, (cx, 19.0, 0), 5.4, facef(cx), layers=5)
    for r, y0, y1 in ((5.8, 20.0, 23.0), (4.6, 23.0, 25.0), (2.6, 25.0, 26.4)):            # onion bulb hair
        m.round_box(bd, cx, 0.6, r, r, y0, y1, ONION, cut=max(1, round(r * 0.35)))
    m.box(bd, cx - 0.6, 26.4, 0.0, cx + 0.6, 28.4, 1.2, ONION)
    for sx in (-1, 1):
        m.box(bd, cx + sx * 2.0 - 1.2, 0.0, -2.6, cx + sx * 2.0 + 1.2, 4.0, 1.4, FACE)


def build():
    m = Model("burgamonadult")
    top = m.bone("burgamonadult", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    WHITE = fabric(P, "white", "white_dark", axis="y", period=2.0)
    cook(m, bd, -6.0, WHITE)
    m.round_box(bd, -6.0, 0, 3.4, 3.0, 13.2, 14.6, solid(P, "blue"), cut=1)                  # blue scarf
    cook(m, bd, 6.0, fabric(P, "violet", "violet_dark", axis="y", period=2.0))
    # arms: the chef's spatula + the burger, the other cook's sausage
    ar = m.bone("arm_right", bd, (-10.0, 12.0, 0))
    rod(m, ar, (-9.6, 12.0, 0), (-7.0, 8.0, -5.0), 2, WHITE, extend=0.3)
    rod(m, ar, (-7.0, 8.0, -5.0), (-4.0, 5.0, -10.0), 1, solid(P, "handle"), extend=0)
    m.box(ar, -6.0, 4.6, -16.0, 0.0, 5.2, -9.6, metal(P, "steel", dark="steel_dark"))       # spatula blade
    burger = ((5.2, 6.8, "bun"), (6.8, 7.6, "patty"), (7.6, 8.0, "cheese"), (8.0, 8.6, "lettuce"),
              (8.6, 9.6, "patty"), (9.6, 10.2, "lettuce"), (10.2, 12.6, "bun_light"))
    for y0, y1, key in burger:
        m.round_box(ar, -3.0, -12.8, 3.4, 3.0, y0, y1, solid(P, key), cut=1)
    m.round_box(ar, -3.0, -12.8, 2.4, 2.0, 12.6, 13.6, solid(P, "bun_light"), cut=1)
    al = m.bone("arm_left", bd, (10.0, 12.0, 0))
    rod(m, al, (9.6, 12.0, 0), (12.0, 18.0, -1.0), 2, solid(P, "violet"), extend=0.3)
    pts = [(12.0, 19.0, -1.0), (13.0, 24.0, -0.6), (12.6, 29.0, 0.0), (10.4, 32.0, 0.4)]
    for p0, p1 in zip(pts, pts[1:]):                                                         # giant sausage
        rod(m, al, p0, p1, 3, solid(P, "sausage"), extend=0.8)
    for sx in (-1, 1):
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 6.0, 6.0, 0))
        m.box(lg, sx * 6.0 - 1.0, 0.0, -0.6, sx * 6.0 + 1.0, 6.0, 0.6, FACE)
    return m
