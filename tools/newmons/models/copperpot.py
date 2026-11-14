"""Copperpot, the Kettle Pokémon (Steel), the first stage of the distillation line (the user's design): a small, round,
riveted copper kettle with a cheerful face, a little spout, a handle arching over its back, a whistling lid with a
knob that puffs steam, and stubby legs.

Shiny: polished silver.

Front is -z, y is up. 11 units tall; baseScale 0.42 (0.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _liquor import eye_on, palette, puff, tiers, translucent
from _route import tone

SHINY = {"copper": (206, 210, 220), "copper_dark": (150, 154, 166), "copper_light": (236, 240, 248)}
P, solid, ramp = palette(SHINY)
SCALE = 0.42
HITBOX = [0.7, 0.65]
KIND = "quadruped"
K = 6
HEIGHT = 11
LOOK = "a small round riveted copper kettle with a cheerful face, a spout, a handle, a whistling lid and stubby legs"
eyes = eye_on(P, "copper_dark", [(-1.2, 5.6), (1.2, 5.6)], 0.7)


def kettlef(x, y, z, face, variant, **k):
    p = P(variant)
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    if face == "north" and abs(y - 4.4) < 0.22 and abs(x) < 0.8:
        return p["pupil"], None
    if abs(y - 3.0) < 0.2 and (int((x + z) * 2) % 3 == 0):
        return p["copper_dark"], None                                         # rivets
    return tone(p["copper_light"] if face == "up" else p["copper"], face), None


def build() -> Model:
    m = Model("copperpot")
    top = m.bone("copperpot", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    tiers(m, bd, [(1.4, 2.4, 2.8), (2.4, 6.4, 3.6), (6.4, 7.4, 2.8)], kettlef)
    rod(m, bd, (2.6, 4.0, -1.6), (4.6, 6.2, -3.0), 0.9, solid("copper"), extend=0.2)            # the spout
    for a, b in (((-2.0, 7.0, 0.0), (-1.6, 9.2, 0.0)), ((-1.6, 9.2, 0.0), (1.6, 9.2, 0.0)), ((1.6, 9.2, 0.0), (2.0, 7.0, 0.0))):
        rod(m, bd, a, b, 0.6, solid("copper_dark"), extend=0.2)                  # the handle
    hd = m.bone("head", bd, (0, 7, 0))
    tiers(m, hd, [(7.2, 7.8, 2.2), (7.8, 8.4, 0.6)], solid("copper_dark"))       # the whistling lid and knob
    puff(m, hd, (4.8, 7.4, -3.2), 0.7, translucent(P, "steam"))
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -1.6), ("back", 1.6)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 1.8, 1.6, z))
            m.round_box(lb, sx * 1.8, z, 0.6, 0.6, 0.0, 1.8, solid("copper_dark"), cut=0.25)
    return m
