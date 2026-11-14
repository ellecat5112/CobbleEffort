"""Hypnodose, the Patch Pokémon (Psychic), the Nicodex's Psychic type (the user's design): a calm, round adhesive
patch that drifts in the air, its face a slowly turning hypnotic spiral of soothing purple, with a pale skin-tone
rim, a peeling edge tab and little floating dots of slow release around it.

Shiny: a teal spiral on a mint patch.

Front is -z, y is up. 14 units tall; baseScale 0.5 (0.45 m). A floater; the spiral is a `ring` bone (it turns).
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _nico import disc_z, palette, puff, translucent

SHINY = {"purple": (60, 170, 170), "purple_light": (140, 230, 220), "skin": (200, 240, 220), "skin_dark": (150, 210, 190)}
P, solid, ramp = palette(SHINY)
SCALE = 0.5
HITBOX = [0.9, 0.9]
KIND = "floater"
K = 6
HEIGHT = 14
LOOK = "a floating round adhesive patch with a slowly turning purple hypnotic spiral and a peeling edge tab"


def patchf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        return p["skin"], None
    return p["skin_dark"], None


def spiralf(x, y, z, face, variant, **k):
    p = P(variant)
    dx, dy = x, y - 8.0
    r = math.hypot(dx, dy)
    if r > 4.4:
        return (0, 0, 0, 0), None
    a = math.atan2(dy, dx)
    band = (r * 1.1 - a / math.pi) % 2.0
    c = p["purple"] if band < 1.0 else p["purple_light"]
    return c, (c if band < 1.0 else None)


def build() -> Model:
    m = Model("hypnodose")
    top = m.bone("hypnodose", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    disc_z(m, bd, 0, 8.0, 6.0, -0.6, 0.6, patchf)                               # the round patch
    m.box(bd, 3.6, 2.2, -1.4, 5.6, 4.2, -0.6, solid("skin_dark"), rotation=(0, 0, 45), pivot=(4.6, 3.2, -1.0))  # peeling tab
    rg = m.bone("ring_spiral", bd, (0, 8, -1))
    m.box(rg, -4.5, 3.5, -1.2, 4.5, 12.5, -0.6, spiralf)                        # the turning spiral
    hd = m.bone("head", bd, (0, 8, 0))
    for c in ((-7.6, 10.6, -0.4), (7.4, 5.0, 0.4), (5.8, 14.6, 0.0), (-6.4, 2.6, 0.2)):
        puff(m, hd, c, 0.6, translucent(P, "violet"))                           # floating dots of release
    return m
