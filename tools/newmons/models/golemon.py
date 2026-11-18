"""Golemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
ancient stone golem: a hunched giant of olive-yellow stone blocks bound with steel bands and bolts, a small masked
head with a riveted iron visor, two horn-like stones on its shoulders, huge block fists and smoke drifting from its
back. Adult stage, 15 blocks tall.

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fbm, metal, riveted, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a hunched olive-yellow stone golem bound with steel bands, a masked head with an iron visor and huge block fists"
BASE = {"stone": (190, 180, 80), "stone_dark": (120, 110, 40), "stone_light": (230, 220, 140), "steel": (170, 174, 186),
        "steel_dark": (80, 84, 96), "visor": (60, 60, 66), "eye": (250, 80, 40), "smoke": (120, 110, 100, 150)}
SHINY = {"stone": (150, 150, 170), "stone_dark": (80, 80, 100), "stone_light": (210, 210, 230)}


def P(v):
    return pal(BASE, SHINY, v)


STONE0 = skin(P, "stone", dark="stone_dark", light="stone_light")
STEEL = metal(P, "steel", dark="steel_dark")


def stonef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((y * 0.5) % 4.0 - 2.0) < 0.15 or abs((x * 0.5 + z * 0.5) % 4.0 - 2.0) < 0.15:
        return tone(p["stone_dark"], face), None
    if fbm(x * 0.4, y * 0.4, z * 0.4, seed=4) > 0.7:
        return tone(p["stone_dark"], face), None
    return STONE0(x, y, z, face, variant, box=box, **k)


def smokef(x, y, z, face, variant, box=None, **k):
    c = P(variant)["smoke"]
    return c, None


def build():
    m = Model("golemon")
    top = m.bone("golemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 1.0, 9.0, 7.0, 10.0, 26.0, stonef, cut=2)
    for j in range(3):
        m.round_box(bd, 0, 1.0, 9.4, 7.4, 13.0 + j * 4.6, 14.2 + j * 4.6, STEEL, cut=2)       # steel bands
    hd = m.bone("head", bd, (0, 24, -6))
    m.round_box(hd, 0, -8.0, 3.4, 2.4, 20.0, 26.0, stonef, cut=1)
    m.round_box(hd, 0, -10.0, 3.0, 0.6, 21.0, 25.0, riveted(P, "visor", "steel_dark"), cut=0)
    m.box(hd, -2.0, 23.0, -10.8, 2.0, 23.8, -10.6, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, bd, (sx * 6.0, 26.0, 0), (sx * 0.3, 1, -0.2), 3.0, 7.0, stonef, tip=1.4)    # horn-like stones
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 9.0, 22.0, 0))
        rod(m, ab, (sx * 9.0, 22.0, 0), (sx * 14.0, 12.0, -4.0), 5, stonef, extend=0.6)
        m.round_box(ab, sx * 14.0, -6.0, 4.4, 5.0, 2.0, 10.0, stonef, cut=1)                  # block fists
        m.round_box(ab, sx * 14.0, -5.0, 4.6, 5.2, 9.0, 10.4, STEEL, cut=1)
    for j in range(3):                                                                         # smoke from its back
        m.round_box(bd, 3.0 + j, 8.0 + j * 1.6, 2.0 + j * 0.6, 2.0 + j * 0.6, 28.0 + j * 4.0, 31.0 + j * 4.0, smokef,
                    cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 12.0, 0))
        rod(m, lg, (sx * 5.0, 12.0, 0), (sx * 6.0, 3.0, 0), 5, stonef, extend=0.6)
        m.round_box(lg, sx * 6.0, -1.0, 3.6, 4.4, 0.0, 3.6, stonef, cut=1)
    return m
