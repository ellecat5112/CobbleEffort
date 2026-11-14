"""Nicotiny, the Seedling Pokémon (Grass), the Nicodex's Grass type (the user's design): a tiny, dewy Nicotiana
seedling, a round green bud with dewdrop eyes, two broad sticky leaves glistening with toxic dew and a sprout on top,
standing on little root feet.

Shiny: golden-yellow leaves.

Front is -z, y is up. 14 units tall; baseScale 0.34 (0.3 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _nico import eye_on, palette
from _route import along, tone

SHINY = {"leaf": (220, 196, 80), "leaf_dark": (180, 150, 50), "leaf_light": (246, 226, 140)}
P, solid, ramp = palette(SHINY)
SCALE = 0.34
HITBOX = [0.6, 0.85]
KIND = "biped"
K = 6
HEIGHT = 14
LOOK = "a tiny green seedling bud with dewdrop eyes, two broad sticky dew-glistening leaves and a sprout, on root feet"
eyes = eye_on(P, "cyan", [(-1.0, 6.2), (1.0, 6.2)], 0.75)


def budf(x, y, z, face, variant, **k):
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    return tone(P(variant)["leaf"], face), None


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = along(z, box)
    if face in ("up", "down") and (math.sin(t * 19 + x * 3) > 0.92):
        return p["white"], None                                               # sticky dew drops
    return tone(p["leaf_light"] if t > 0.7 else p["leaf"], face), None


def build() -> Model:
    m = Model("nicotiny")
    top = m.bone("nicotiny", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0, 2.8, 2.6, 2.4, 8.4, budf, cut=1.0)
    hd = m.bone("head", bd, (0, 8, 0))
    for d in ((0.0, 1, 0.1), (-0.5, 1, 0.2), (0.5, 1, -0.1)):
        spike(m, hd, (0, 8.2, 0), d, 1.2, 3.0 + abs(d[0]) * -2, solid("leaf_light"))     # the sprout on top
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 2.2, 6.6, 0))                       # two broad sticky leaves
        rod(m, ar, (sx * 2.2, 6.6, 0.0), (sx * 7.4, 10.4, -0.6), 4.2, leaff, extend=0.4, t2=0.7)
        lb = m.bone(f"leg_{side}", top, (sx * 1.2, 2.6, 0))
        rod(m, lb, (sx * 1.2, 2.6, 0.0), (sx * 1.8, 0.6, -0.4), 1.0, solid("tan"), extend=0.3)
        spike(m, lb, (sx * 1.8, 0.6, -0.4), (sx * 0.6, -0.3, -1), 0.9, 1.6, solid("tan"))     # little roots
    return m
