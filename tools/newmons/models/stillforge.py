"""Stillforge, the Pot Still Pokémon (Steel/Fire), a Liquor Meadows Pokémon (the user's design): a towering, gleaming
copper-and-brass automaton shaped like a swan-necked alembic pot still: a great round riveted copper belly with a
glowing firebox window, a helmet head topped by a domed cap whose long swan-neck lyne arm arches back over its
shoulder into a coiled condenser, pipe arms ending in brass valve-wheel hands, piston legs, venting steam.

Shiny: polished silver with blue fire.

Front is -z, y is up. 42 units tall; baseScale 0.95 (2.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod
from _liquor import helix, palette, puff, tiers, translucent
from _route import tone

SHINY = {"copper": (200, 206, 216), "copper_dark": (140, 146, 158), "copper_light": (236, 240, 246), "brass": (170, 176, 190),
         "ember": (80, 160, 255), "ember_hot": (180, 230, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.95
HITBOX = [2.0, 2.6]
KIND = "biped"
K = 3
HEIGHT = 42
LOOK = ("a towering copper-and-brass pot-still automaton: a riveted copper belly with a glowing firebox, a swan-neck "
        "arm arching into a coiled condenser, pipe arms and piston legs, venting steam")


def potf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.6 and 11.0 < y < 15.0:
        c = p["ember_hot"] if abs(x) < 1.4 and y < 13.4 else p["ember"]
        return c, c                                                           # the firebox window
    if face == "north" and (abs(abs(x) - 2.8) < 0.3) and 10.6 < y < 15.4:
        return p["brass"], None
    u = x if face in ("north", "south") else z
    if (abs(y - 18.0) < 0.3 or abs(y - 24.0) < 0.3) or (abs(y - 18.0) < 0.6 and int(u * 1.5) % 3 == 0):
        return p["copper_dark"], None                                         # seams and rivets
    return tone(p["copper_light"] if face == "up" else p["copper"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(y - 31.6) < 0.6 and abs(x) < 2.2:
        c = p["ember"]
        return c, c                                                           # a glowing visor slit
    return tone(p["copper"], face), None


def build() -> Model:
    m = Model("stillforge")
    top = m.bone("stillforge", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    tiers(m, bd, [(9.0, 11.0, 5.6), (11.0, 15.0, 7.4), (15.0, 21.0, 8.0), (21.0, 25.0, 7.2), (25.0, 27.0, 5.0)], potf)
    hd = m.bone("head", bd, (0, 27, 0))
    tiers(m, hd, [(27.0, 29.0, 3.4), (29.0, 33.4, 3.8), (33.4, 35.4, 3.0), (35.4, 36.6, 1.6)], headf)
    nk = m.bone("neck_lyne", hd, (0, 36, 0))
    chain(m, nk, [(0, 36.2, 0.0), (0, 38.4, 2.0), (0, 38.0, 6.0), (0, 34.0, 9.6), (0, 27.0, 11.6)], [1.6, 1.4, 1.2, 1.2],
          solid("copper"))                                                      # the swan-neck lyne arm
    helix(m, nk, (0, 0, 12.4), 2.0, 16.0, 26.0, 3.0, 1.0, solid("copper_light"))  # the coiled condenser
    for c, r in (((1.6, 38.8, 2.4), 1.6), ((3.0, 40.6, 3.8), 1.3), ((0.4, 15.0, 13.0), 1.2)):
        puff(m, nk, c, r, translucent(P, "steam"))                              # venting steam
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 7.6, 23, 0))
        chain(m, ar, [(sx * 7.6, 23.0, 0.0), (sx * 10.6, 19.0, -0.6), (sx * 11.2, 13.0, -1.6)], [2.0, 1.8], solid("brass"))
        for i in range(4):                                                      # valve-wheel hands
            a = math.pi * i / 4
            rod(m, ar, (sx * 11.2 + math.cos(a) * 1.8, 11.4 + math.sin(a) * 1.8, -1.8),
                (sx * 11.2 - math.cos(a) * 1.8, 11.4 - math.sin(a) * 1.8, -1.8), 0.6, solid("copper_dark"), extend=0.2)
        lb = m.bone(f"leg_{side}", top, (sx * 4, 9, 0))
        m.round_box(lb, sx * 4.2, 0, 1.6, 1.6, 2.0, 9.6, solid("steel_dark"), cut=0.5)   # piston legs
        m.round_box(lb, sx * 4.2, -0.6, 2.8, 3.4, 0.0, 2.2, solid("copper_dark"), cut=0.8)
    return m
