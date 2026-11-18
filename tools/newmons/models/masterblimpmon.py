"""Master Blimpmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the great airship: a long riveted silver airship hull with a drill nose, rows of portholes, a deck of twin cannons and
a lookout turret, violet tailfins and side fins, blue jet engines, gun turrets under its belly and a small mechanical
arm. 25 blocks long.

Front is -z, y is up. 24 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(25, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a long riveted silver airship with a drill nose, portholes, deck cannons, violet tailfins, blue jet engines and belly turrets"
BASE = {"silver": (200, 206, 216), "silver_dark": (100, 106, 120), "silver_light": (240, 244, 250), "violet": (80, 70, 160),
        "violet_dark": (36, 30, 90), "blue": (60, 110, 220), "black": (30, 30, 36), "orange": (240, 140, 40), "glass": (120, 200, 240)}
SHINY = {"silver": (220, 190, 110), "silver_dark": (140, 110, 40), "silver_light": (255, 240, 180)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = riveted(P, "silver", "silver_dark", light="silver_light")


def hullf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 12.0) < 0.8 and (z % 3.0) < 1.2:
        return tone(p["glass"], face), None
    return HULL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("masterblimpmon")
    top = m.bone("masterblimpmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(10):
        r = 6.0 * math.sin(math.pi * (0.12 + 0.8 * (i + 0.5) / 10)) + 0.6
        slab_z(m, bd, 0, 12.0, -16.0 + i * 3.4, -12.6 + i * 3.4, r, r * 0.9, hullf)
    spike(m, bd, (0, 12.0, -16.0), (0, 0, -1), 3.4, 9.0, metal(P, "silver", dark="silver_dark"), tip=0.8)     # drill nose
    for j in range(3):                                                               # deck cannons + turret
        rod(m, bd, (-1.6 + j * 1.6, 18.0, -2.0 + j * 2.0), (-1.6 + j * 1.6, 18.6, -10.0 + j * 2.0), 1,
            metal(P, "silver", dark="silver_dark"), extend=0, t2=1)
    m.round_box(bd, 0, 4.0, 2.0, 2.0, 17.0, 20.0, armour(P, "silver", "silver_dark"), cut=1)
    m.round_box(bd, 0, 4.0, 1.2, 1.2, 20.0, 21.0, solid(P, "orange"), cut=0)
    for side in (1, -1):                                                             # fins + jet engines
        x0, x1 = sorted((side * 4.0, side * 10.0))
        m.box(bd, x0, 11.4, 4.0, x1, 12.4, 10.0, armour(P, "violet", "violet_dark"))
        m.round_box(bd, side * 7.0, 2.0, 1.8, 3.0, 5.0, 8.0, metal(P, "blue", dark="violet_dark"), cut=1)
        x0, x1 = sorted((side * 0.4, side * 5.0))
        m.box(bd, x0, 14.0, 14.0, x1, 15.0, 18.0, armour(P, "violet", "violet_dark"), rotation=(0, 0, side * -40),
              pivot=(side * 0.4, 14.0, 16.0))
    m.box(bd, -0.5, 16.0, 13.0, 0.5, 22.0, 18.0, armour(P, "violet", "violet_dark"))
    for j in range(3):                                                               # belly turrets
        m.round_box(bd, 0, -6.0 + j * 6.0, 1.4, 1.4, 5.0, 6.6, metal(P, "silver", dark="silver_dark"), cut=0)
        rod(m, bd, (0, 5.4, -6.0 + j * 6.0), (0, 4.6, -9.0 + j * 6.0), 1, solid(P, "black"), extend=0, t2=1)
    return m
