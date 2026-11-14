"""Peatling, the Peat Pokémon (Rock/Fire), a Liquor Meadows Pokémon (the user's design): a compact, earthy little
creature of compressed bog turf, layered in dark peat bands with a mossy green top and tufts of bog grass, glowing
cracks of smouldering charcoal along its sides and a smoky, earthy-smelling breath curling from its snout.

Shiny: pale grey ashy turf with blue embers.

Front is -z, y is up. 12 units tall; baseScale 0.45 (0.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _liquor import palette, puff, translucent
from _route import tone

SHINY = {"peat": (150, 146, 140), "peat_dark": (110, 106, 102), "ember": (80, 160, 255), "ember_hot": (180, 230, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.45
HITBOX = [0.8, 0.6]
KIND = "quadruped"
K = 5
HEIGHT = 12
LOOK = "a compact block of layered bog turf with a mossy top, glowing charcoal cracks and smoky breath"


def turff(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" or (face != "down" and y > 8.6):
        return tone(p["moss"] if (int(x * 2) + int(z * 2)) % 4 else p["moss_light"], face), None
    if face in ("east", "west", "south") and abs(math.sin(z * 0.9 + y * 1.6)) < 0.12 and y < 8.0:
        return p["ember_hot"], p["ember_hot"]                                 # glowing charcoal cracks
    band = int(y * 1.2) % 2
    return tone(p["peat"] if band else p["peat_dark"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.5 and abs(y - 7.2) < 0.5:
                return p["ember"], p["ember"]                                 # ember eyes
    return turff(x, y, z, face, variant)


def build() -> Model:
    m = Model("peatling")
    top = m.bone("peatling", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 1.0, 3.6, 4.6, 2.0, 9.4, turff, cut=1.2)
    hd = m.bone("head", bd, (0, 6, -4))
    m.round_box(hd, 0, -4.4, 2.8, 1.8, 3.6, 9.0, headf, cut=0.8)
    for dx in (-1.4, 0.0, 1.4):
        spike(m, bd, (dx, 9.2, 1.0 + dx * 0.4), (dx * 0.2, 1, 0.1), 0.6, 1.8, solid("moss_light"))   # bog grass tufts
    puff(m, hd, (0.4, 9.6, -6.6), 0.9, translucent(P, "smoke"))                 # smoky breath
    puff(m, hd, (0.9, 11.4, -6.2), 0.7, translucent(P, "smoke"))
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -2.4), ("back", 4.0)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 2.2, 2.4, z))
            m.round_box(lb, sx * 2.2, z, 1.0, 1.0, 0.0, 2.6, solid("peat_dark"), cut=0.4)
    return m
