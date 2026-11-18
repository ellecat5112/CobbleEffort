"""Hubmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
golden serpent of cables: a box-shaped hub head with "HUB" port slots and round glasses, a long coiling gold snake body
banded with black ports and a plug tail with a silver USB tip. Child stage, 1 block long.

Front is -z, y is up. 22 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import metal, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 0}
LOOK = "a golden serpent of cables with a box hub head, port slots, round glasses and a USB plug tail"
BASE = {"gold": (240, 200, 60), "gold_dark": (160, 120, 20), "gold_light": (255, 240, 160), "black": (30, 30, 34),
        "silver": (220, 224, 232), "silver_dark": (110, 114, 126), "glass": (190, 230, 250), "eye": (20, 20, 24)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 150), "gold_light": (250, 250, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def bandf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (math.hypot(x, z) * 1.0 + y) % 3.0 < 0.6:
        return tone(p["black"], face), None
    return GOLD(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 17.4)
            if d < 0.6:
                return tone(p["eye"], face), None
            if d < 1.3:
                return tone(p["glass"], face), None
            if d < 1.6:
                return tone(p["black"], face), None
        if 13.6 < y < 14.8 and abs(x) < 3.0 and (x + 3.0) % 2.0 < 1.4:
            return tone(p["black"], face), None
    return GOLD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hubmon")
    top = m.bone("hubmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    pts = []
    for i in range(14):                                                             # coiled cable body
        t = i / 13
        ang = t * 2.6 * math.pi
        r = 5.0 - t * 1.6
        pts.append((r * math.cos(ang), 1.2 + t * 9.0, r * math.sin(ang)))
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 2, bandf, extend=0.6)
    m.round_box(bd, pts[0][0], pts[0][2] + 2.4, 1.2, 1.4, 0.4, 2.2, metal(P, "silver", dark="silver_dark"), cut=0)
    m.round_box(bd, pts[0][0], pts[0][2] + 3.8, 0.8, 0.8, 0.8, 1.8, solid(P, "black"), cut=0)
    rod(m, bd, pts[-1], (0, 12.0, 0), 2, bandf, extend=0.8)                           # neck up into the hub
    hd = m.bone("head", bd, (0, 12, 0))
    m.round_box(hd, 0, 0, 3.6, 3.0, 11.4, 20.0, headf, cut=1)
    return m
