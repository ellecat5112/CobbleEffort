"""Aegisdramon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a golden
dragon-ship of the deep seas: a long golden hull with a grey armoured deck, a red eye in its prow, cannons along its
flanks, white lances bristling forward and silver claws hanging beneath. 35 blocks long.

Front is -z, y is up. 22 units tall, 50 long; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digiwar import make_palette, solid_of
from _route import tone

HEIGHT = 22
SCALE, HITBOX = sized(35 * 22 / 50, HEIGHT, 2.2)
KIND = "floater"
K = 2
LOOK = "a golden dragon-ship: a long golden hull with a grey armoured deck, a red eye in its prow, flank cannons, white lances bristling forward and silver claws beneath"

BASE = {"gold": (230, 184, 60), "gold_dark": (170, 126, 30), "deck": (150, 152, 164), "deck_dark": (100, 102, 114),
        "eye": (230, 40, 40), "lance": (240, 240, 246), "cannon": (70, 72, 82), "claw": (200, 204, 214),
        "jet": (120, 220, 255)}
SHINY = {"gold": (200, 204, 216), "gold_dark": (140, 146, 160), "deck": (60, 64, 90), "deck_dark": (40, 42, 60),
         "eye": (60, 220, 120)}
P = make_palette(BASE, SHINY)
solid = solid_of(P)


def hullf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 9.0) < 0.4:
        return tone(p["gold_dark"], face), None
    if face == "down":
        return tone(p["gold_dark"], face), None
    return tone(p["gold"], face), None


def build():
    m = Model("aegisdramon")
    top = m.bone("aegisdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 7.0, 18.0, 4.0, 13.0, hullf, cut=4.0)              # the hull
    m.round_box(bd, 0, 4.0, 5.0, 11.0, 13.0, 17.0, solid("deck"), cut=3.0)   # the armoured deck
    m.round_box(bd, 0, 8.0, 3.0, 4.0, 17.0, 21.0, solid("deck_dark"), cut=1.4)   # the bridge
    hd = m.bone("head", bd, (0, 9, -16))
    m.round_box(hd, 0, -19.0, 4.0, 4.0, 5.0, 12.0, hullf, cut=1.6)            # the prow
    m.box(hd, -1.4, 8.6, -23.1, 1.4, 10.6, -22.9, solid("eye", glow=True))
    for sx in (-1, 1):
        for i, (y, z) in enumerate(((11.0, -24.0), (7.0, -24.0), (9.5, -20.0))):   # lances bristling forward
            rod(m, hd, (sx * (1.6 + i), y, z + 2), (sx * (3.0 + i * 1.6), y + 0.5, z - 9), 0.8, solid("lance"), extend=0.0)
        for i in range(4):                                                   # flank cannons
            rod(m, bd, (sx * 6.5, 11.0, -10.0 + i * 6.0), (sx * 9.5, 11.0, -11.0 + i * 6.0), 1.6, solid("cannon"),
                extend=0.1)
        cl = m.bone(f"arm_{'left' if sx > 0 else 'right'}", bd, (sx * 4.0, 4.5, -6.0))
        rod(m, cl, (sx * 4.0, 4.5, -6.0), (sx * 5.0, 0.5, -9.0), 1.4, solid("claw"), extend=0.2)
        for d in (-0.6, 0.6):
            spike(m, cl, (sx * 5.0, 0.5, -9.0 + d), (0, -1, -0.4), 0.7, 2.2, solid("claw"), tip=0.2)
    tl = m.bone("tail", bd, (0, 9, 17))
    for sx in (-1, 1):                                                       # twin jets at the stern
        rod(m, tl, (sx * 3.0, 8.0, 16.0), (sx * 3.2, 8.0, 22.0), 3.0, solid("deck_dark"), extend=0.0)
        m.box(tl, sx * 3.2 - 1.0, 7.0, 22.0, sx * 3.2 + 1.0, 9.0, 22.4, solid("jet", glow=True))
    return m
