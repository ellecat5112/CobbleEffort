"""Digimon Slingshot (a Digimon of the CobbleEffort: Digital crossover; after the art on wikimon.net, where it is filed
as "Pickmons Slingshot"): one of the Pickmons, a living slingshot band. A loop of plaited white cord flecked with
dark chevrons, hanging from which a bright yellow pouch tag smiles a simple little face. It floats along, swinging
its long tail of cord. Child stage, 1 block long.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import solid, twisted
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "floater"
K = 4
LOOK = "a loop of plaited white cord flecked with dark chevrons, with a smiling bright yellow pouch tag"
BASE = {"cord": (236, 238, 244), "cord_dark": (150, 156, 176), "chevron": (40, 50, 80), "yellow": (250, 240, 110),
        "yellow_dark": (200, 180, 60), "face": (40, 40, 40)}
SHINY = {"cord": (240, 200, 220), "cord_dark": (180, 120, 150), "yellow": (130, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


TW = twisted(P, "cord", "cord_dark", period=1.6)


def cordf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(((x + y + z) * 0.7) % 3.0 - 1.5) < 0.18:
        return tone(p["chevron"], face), None
    return TW(x, y, z, face, variant, box=box, **k)


def tagf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.0, y - 7.0) < 0.35:
                return tone(p["face"], face), None
        if abs(y - (5.8 + 0.25 * x * x)) < 0.2 and abs(x) < 1.2:
            return tone(p["face"], face), None
    return tone(p["yellow"], face), None


def build():
    m = Model("digimonslingshot")
    top = m.bone("digimonslingshot", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    n = 14                                                                  # the loop of plaited cord
    pts = [(7.0 * math.cos(2 * math.pi * i / n), 12.0 + 6.0 * math.sin(2 * math.pi * i / n), 0.0) for i in range(n + 1)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 2, cordf, extend=0.6)
    hd = m.bone("head", bd, (0, 6, 0))
    m.round_box(hd, 0, 0, 4.0, 1.4, 4.0, 9.0, tagf, cut=1)                    # the smiling yellow tag
    tl = m.bone("tail", bd, (7, 12, 0))                                     # trailing cord
    tp = [(7.0, 12.0, 0.0), (12.0, 15.0, 2.0), (17.0, 19.0, 1.0), (21.0, 22.0, 3.0)]
    for p0, p1 in zip(tp, tp[1:]):
        rod(m, tl, p0, p1, 2, cordf, extend=0.6)
    return m
