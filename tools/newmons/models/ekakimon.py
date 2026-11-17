"""Ekakimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
living colour pencil. A tall orange hexagonal pencil body with a sharpened black-and-red tip for a head, a wide toothy
grin and narrow red eyes, a gold ferrule band at its waist, striped rainbow arms ending in gloves whose fingertips are
coloured crayons, and pencil-stub legs with coloured points; one hand trails a stroke of rainbow. Child stage, 1 block
tall.

Front is -z, y is up. 36 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import local, metal, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a tall orange hexagonal pencil with a sharpened black-and-red tip, a toothy grin, a gold ferrule band, rainbow-"
        "striped arms and crayon fingertips")
BASE = {"orange": (250, 170, 50), "orange_dark": (200, 110, 20), "wood": (240, 210, 160), "black": (30, 28, 32),
        "red": (220, 40, 40), "gold": (240, 200, 60), "gold_dark": (160, 120, 20), "white": (250, 250, 250),
        "c0": (230, 50, 50), "c1": (250, 200, 50), "c2": (70, 190, 90), "c3": (60, 120, 230), "c4": (170, 80, 200)}
SHINY = {"orange": (90, 170, 230), "orange_dark": (40, 100, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 20.0 < y < 23.0 and abs(x) < 3.0:                                    # toothy grin
            return tone(p["black"] if abs(y - 21.5) < 0.2 or (x * 1.4) % 1.4 < 0.15 else p["white"], face), None
        for sx in (-1, 1):
            if abs(y - (25.0 + (abs(x) - 1.6) * 0.4)) < 0.3 and 0.8 < abs(x) < 2.6 and x * sx > 0:
                return p["red"], p["red"]
    if face in ("east", "west", "north", "south") and abs((x + z) % 2.0) < 0.15:
        return tone(p["orange_dark"], face), None                               # hexagon facet lines
    return skin(P, "orange", dark="orange_dark", var=0.02)(x, y, z, face, variant, box=box, **k)


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["c%d" % (int(abs(x) + y) % 5)], face), None


def build():
    m = Model("ekakimon")
    top = m.bone("ekakimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 4.0, 4.0, 8.0, 27.0, bodyf, cut=1)                         # pencil body
    m.round_box(bd, 0, 0, 4.3, 4.3, 8.0, 10.6, metal(P, "gold", dark="gold_dark"), cut=1)   # ferrule
    hd = m.bone("head", bd, (0, 27, 0))
    for j, r in enumerate((3.6, 2.8, 2.0)):                                          # sharpened wood + lead tip
        m.round_box(hd, 0, 0, r, r, 27.0 + j * 2.0, 29.0 + j * 2.0, solid(P, "wood" if j < 2 else "black"), cut=1)
    spike(m, hd, (0, 33.0, 0), (0, 1, 0), 2.6, 3.0, solid(P, "red"), tip=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 22.0, 0))
        rod(m, ab, (sx * 4.0, 22.0, 0), (sx * 10.0, 24.0, -2.0), 2, stripef, extend=0.4)
        m.round_box(ab, sx * 11.6, -2.0, 1.8, 1.8, 23.0, 26.0, solid(P, "white"), cut=1)
        for j in range(4):                                                          # crayon fingertips
            spike(m, ab, (sx * 11.6 + (j - 1.5) * 0.9, 26.0, -2.0), ((j - 1.5) * 0.15, 1, 0), 0.8, 2.4,
                  solid(P, "c%d" % j), tip=0.3)
    al = "arm_left"                                                                  # a stroke of rainbow
    for j in range(5):
        m.box(al, 12.0 + j * 2.0, 30.0 + j * 0.8, -2.2, 14.0 + j * 2.0, 31.0 + j * 0.8, -1.8, solid(P, "c%d" % j))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 8.0, 0))
        rod(m, lg, (sx * 2.0, 8.0, 0), (sx * 4.0, 2.0, -1.0), 2, stripef, extend=0.4)
        spike(m, lg, (sx * 4.0, 2.0, -1.0), (0, -1, -0.2), 1.6, 2.4, solid(P, "c%d" % (1 if sx > 0 else 3)), tip=0.4)
    return m
