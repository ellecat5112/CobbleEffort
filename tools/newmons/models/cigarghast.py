"""Cigarghast, the Cigar Phantom Pokémon (Ghost/Fire), the Nicodex's Ghost type (the user's design): a phantom
shaped like a thick, rolled cigar: wrapped tobacco-leaf body with a gold-and-red cigar band, a single glowing ember
eye at its lit tip, and wraith arms of curling smoke. It blows perfect smoke rings.

Shiny: a pale Connecticut-leaf wrapper with a silver band and a green ember.

Front is -z, y is up. 18 units tall; baseScale 0.6 (0.8 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain
from _nico import palette, puff, ring_pts, translucent, tube_z
from _route import tone

SHINY = {"tobacco": (214, 180, 120), "tobacco_dark": (176, 140, 84), "gold": (214, 216, 226),
         "ember": (100, 240, 120), "ember_hot": (200, 255, 200)}
P, solid, ramp = palette(SHINY)
SCALE = 0.6
HITBOX = [0.9, 1.1]
KIND = "floater"
K = 5
HEIGHT = 18
LOOK = "a phantom shaped like a thick rolled cigar with a gold-and-red band, one glowing ember eye and smoky wraith arms"


def leaff(x, y, z, face, variant, **k):
    p = P(variant)
    if ((y * 1.1 + x * 0.6) % 2.4) < 0.35:
        return tone(p["tobacco_dark"], face), None                            # the wrapper's spiral seam
    return tone(p["tobacco"], face), None


def bandf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.0:
        return p["red"], None
    return tone(p["gold"], face), None


def emberf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and math.hypot(x, z) < 1.2:
        return p["ember_hot"], p["ember_hot"]                                 # the ember eye
    return p["ember"], p["ember"]


def build() -> Model:
    m = Model("cigarghast")
    top = m.bone("cigarghast", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.round_box(bd, 0, 0, 3.0, 3.0, 2.0, 14.0, leaff, cut=1.0)                 # the rolled cigar body
    m.round_box(bd, 0, 0, 3.2, 3.2, 9.0, 11.0, bandf, cut=1.0)                 # the cigar band
    m.round_box(bd, 0, 0, 2.4, 2.4, 0.6, 2.4, solid("tobacco_dark"), cut=0.8)  # the cut foot
    hd = m.bone("head", bd, (0, 14, 0))
    m.round_box(hd, 0, 0, 2.8, 2.8, 14.0, 15.4, solid("ash"), cut=0.9)         # a ring of ash
    m.round_box(hd, 0, 0, 2.6, 2.6, 15.2, 16.2, emberf, cut=0.9)               # the lit tip / ember eye
    puff(m, hd, (0.4, 18.0, 0.2), 1.2, translucent(P, "smoke"))
    rg = m.bone("ring_smoke", hd, (0, 21, 0))
    pts = ring_pts((0, 21.0, 0), 2.2, 8, plane="xy")
    chain(m, rg, pts, [0.8] * 8, translucent(P, "smoke"))                       # a perfect smoke ring
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3, 10, 0))
        chain(m, ar, [(sx * 3.0, 10.0, 0.0), (sx * 6.0, 9.0, -1.0), (sx * 7.6, 11.0, -2.0), (sx * 7.0, 13.0, -2.6)],
              [1.6, 1.2, 0.8], translucent(P, "smoke"))                         # smoky wraith arms
    return m
