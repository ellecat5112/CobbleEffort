"""Hopsprout, the Hop Cone Pokémon (Grass), a Liquor Meadows Pokémon (the user's design): a cheerful cone-shaped green
sprite made of overlapping aromatic hop bracts, round eyes and a smile on its lowest bracts, leafy little arms, stubby
feet and a curling bine tendril on top.

Shiny: golden hops.

Front is -z, y is up. 15 units tall; baseScale 0.36 (0.35 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _liquor import eye_on, palette
from _route import tone

SHINY = {"hop": (226, 196, 80), "hop_dark": (180, 146, 50), "hop_light": (246, 226, 140)}
P, solid, ramp = palette(SHINY)
SCALE = 0.36
HITBOX = [0.6, 0.9]
KIND = "biped"
K = 6
HEIGHT = 15
LOOK = "a cheerful cone of overlapping green hop bracts with a smiling face, leafy arms and a curling bine on top"
eyes = eye_on(P, "hop_dark", [(-1.2, 5.6), (1.2, 5.6)], 0.8)


def bractf(x, y, z, face, variant, **k):
    """Overlapping bracts: scalloped rows, each lighter at its tip (bottom edge)."""
    p = P(variant)
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    if face == "north" and abs(y - 4.1) < 0.28 and abs(x) < 1.0 + 0.0 and abs(x) > 0.2:
        return p["pupil"], None                                               # a smile
    u = x if face in ("north", "south") else z
    row = (y - 2.0) % 1.8
    scallop = 0.5 + 0.5 * math.cos(u * 2.4 + (int((y - 2.0) // 1.8) % 2) * math.pi)
    if row < 0.35 + 0.25 * scallop:
        return tone(p["hop_light"], face), None
    if row > 1.5:
        return tone(p["hop_dark"], face), None
    return tone(p["hop"], face), None


def build() -> Model:
    m = Model("hopsprout")
    top = m.bone("hopsprout", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    for y0, r in ((2.0, 3.6), (3.8, 3.8), (5.6, 3.4), (7.4, 2.8), (9.2, 2.1), (11.0, 1.4)):   # the cone of bracts
        m.round_box(bd, 0, 0, r, r, y0, y0 + 1.8, bractf, cut=max(0.6, round(r * 0.35, 1)))
    hd = m.bone("head", bd, (0, 12, 0))
    chain(m, hd, [(0, 12.6, 0), (0.6, 14.0, 0.2), (1.6, 14.8, 0.6), (2.2, 14.2, 1.0)], [0.8, 0.7, 0.6],
          solid("hop_dark"))                                                     # the bine tendril
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3.4, 6, 0))
        rod(m, ar, (sx * 3.4, 6.0, 0.0), (sx * 6.2, 7.6, -0.4), 2.2, solid("hop_light"), extend=0.3, t2=0.6)
        lb = m.bone(f"leg_{side}", top, (sx * 1.4, 2, 0))
        m.round_box(lb, sx * 1.4, -0.3, 0.9, 1.1, 0.0, 2.2, solid("hop_dark"), cut=0.4)
    return m
