"""Agavolem, the Agave Golem Pokémon (Ground/Grass), a Liquor Meadows Pokémon (the user's design): a rugged golem of
cracked terracotta with a massive blue agave heart (piña) bursting from its torso: a ring of thick spiny blue-green
agave leaves fanning out of its chest, over a round, cross-hatched piña core; deep-set amber eyes and heavy fists.

Shiny: sun-bleached sand-coloured clay with a golden agave.

Front is -z, y is up. 32 units tall; baseScale 0.9 (1.8 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _liquor import palette
from _route import tone

SHINY = {"terracotta": (222, 196, 150), "terracotta_dark": (180, 150, 106), "terracotta_light": (240, 220, 180),
         "agave": (220, 190, 80), "agave_dark": (170, 140, 50), "agave_light": (246, 224, 140)}
P, solid, ramp = palette(SHINY)
SCALE = 0.9
HITBOX = [1.6, 2.0]
KIND = "biped"
K = 3
HEIGHT = 32
LOOK = "a rugged cracked-terracotta golem with a huge spiny blue agave heart bursting from its chest"


def clayf(x, y, z, face, variant, **k):
    p = P(variant)
    if (abs(math.sin(x * 1.7 + y * 0.9) + math.cos(z * 1.3 - y * 0.6)) < 0.08):
        return p["terracotta_dark"], None                                     # cracks
    return tone(p["terracotta"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.6 and abs(y - 27.6) < 0.4:
                return p["amber_light"], p["amber_light"]
    return clayf(x, y, z, face, variant)


def pinaf(x, y, z, face, variant, **k):
    p = P(variant)
    u = x if face in ("north", "south") else z
    if abs(((u + y) % 1.6) - 0.8) < 0.18 or abs(((u - y) % 1.6) - 0.8) < 0.18:
        return p["agave_dark"], None                                          # the piña's cross-hatched scales
    return tone(p["agave_light"], face), None


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["agave"] if face in ("up", "north") else p["agave_dark"], face), None


def build() -> Model:
    m = Model("agavolem")
    top = m.bone("agavolem", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11, 0))
    m.round_box(bd, 0, 0.6, 6.0, 4.8, 10.0, 23.0, clayf, cut=1.8)              # the terracotta torso
    m.round_box(bd, 0, -4.6, 3.4, 1.6, 13.4, 19.6, pinaf, cut=1.0)            # the piña core
    for i in range(9):                                                        # spiny agave leaves bursting out
        a = math.pi * (0.1 + 0.8 * i / 8)
        d = (math.cos(a) * 1.0, math.sin(a) * 0.9 + 0.3, -0.75)
        spike(m, bd, (math.cos(a) * 2.4, 16.4 + math.sin(a) * 2.0, -5.0), d, 1.8, 6.0 + (i % 2) * 1.6, leaff, tip=0.9)
    hd = m.bone("head", bd, (0, 23, 0))
    m.round_box(hd, 0, 0, 3.2, 3.0, 23.0, 29.6, headf, cut=1.0)
    m.box(hd, -3.4, 28.6, -3.2, 3.4, 29.6, -2.0, solid("terracotta_dark"))     # a heavy brow
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 6, 21, 0))
        rod(m, ar, (sx * 6.0, 21.0, 0.6), (sx * 8.4, 13.0, 0.0), 3.4, clayf, extend=0.4)
        m.round_box(ar, sx * 8.6, -0.4, 2.6, 2.6, 8.0, 13.2, clayf, cut=1.0)  # heavy fists
        lb = m.bone(f"leg_{side}", top, (sx * 3, 10, 0))
        m.round_box(lb, sx * 3.2, 0.4, 2.4, 2.8, 0.0, 10.6, clayf, cut=0.8)
    return m
