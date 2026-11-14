"""Caskade, the Cask Pokémon (Water/Grass), a Liquor Meadows Pokémon (the user's design): a sturdy, slow quadruped
tortoise whose shell is a banded oak barrel lying along its back, bound with iron hoops, with a bung on top, overgrown
with creeping grapevines (leaves and bunches of purple grapes) and moss; a mossy green head and stout legs.

Shiny: a pale ash-wood cask with white grapes.

Front is -z, y is up. 18 units tall; baseScale 0.85 (1.1 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _liquor import palette, puff
from _route import tone

SHINY = {"oak": (210, 186, 150), "oak_dark": (170, 146, 110), "oak_light": (232, 214, 182), "grape": (190, 210, 110),
         "grape_dark": (150, 170, 70)}
P, solid, ramp = palette(SHINY)
SCALE = 0.85
HITBOX = [1.7, 1.2]
KIND = "quadruped"
K = 3
HEIGHT = 18
LOOK = "a sturdy tortoise whose shell is a banded oak barrel overgrown with grapevines and moss"


def caskf(x, y, z, face, variant, **k):
    p = P(variant)
    if abs(z - 4.6) < 0.6 or abs(z + 4.6) < 0.6:
        return p["iron"], None                                                # iron hoops
    if face == "up" and abs(x) < 0.8 and abs(z) < 0.8:
        return p["oak_dark"], None                                            # the bung
    if face == "up" and math.sin(x * 2.0 + z * 0.5) > 0.6:
        return tone(p["moss"], face), None                                    # moss
    stave = int((x + 20) * 0.9) % 2 if face == "up" else int((y + 20) * 0.9) % 2
    return tone(p["oak"] if stave else p["oak_light"], face), None


def skinf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(y - 8.2) < 0.4 and abs(z + 11.6) < 0.6 and face != "north":
        return p["pupil"], None
    return tone(p["moss"], face), None


def build() -> Model:
    m = Model("caskade")
    top = m.bone("caskade", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for z0, z1, r in ((-8.0, -5.0, 5.4), (-5.0, 5.0, 6.4), (5.0, 8.0, 5.4)):  # the barrel, bulging in the middle
        m.box(bd, -r, 13.0 - r * 1.2, z0, r, 13.0, z1, caskf)
        m.box(bd, -r + 1.4, 13.0 - r * 1.2 - 0.0, z0, r - 1.4, 13.8, z1, caskf)
    m.box(bd, -7.4, 5.0, -6.0, 7.4, 6.0, 6.0, solid("oak_dark"))                 # the plastron
    for i in range(7):                                                          # creeping grapevines
        a = i / 6
        x = -5.0 + 10.0 * a
        z = -4.0 + 8.0 * math.sin(a * 5.0)
        spike(m, bd, (x, 13.4, z), (0.3, 1, 0.2), 1.6, 1.2, solid("green"))
    for c in ((6.8, 11.0, -2.6), (-6.8, 10.6, 2.4), (6.6, 10.4, 3.6), (1.6, 15.0, -2.0)):
        for dy, dx, dz in ((0.0, 0.0, 0.0), (-0.9, 0.0, 0.55), (-0.9, 0.0, -0.55), (-1.8, 0.0, 0.0)):
            puff(m, bd, (c[0] + dx, c[1] + dy, c[2] + dz), 0.6, solid("grape"))  # bunches of grapes hanging off it
    hd = m.bone("head", bd, (0, 8, -8))
    rod(m, hd, (0, 8.0, -7.6), (0, 8.4, -10.4), 2.6, skinf, extend=0.4)
    m.round_box(hd, 0, -11.6, 2.0, 2.0, 6.8, 10.4, skinf, cut=0.6)
    tl = m.bone("tail", bd, (0, 7, 8))
    rod(m, tl, (0, 7.0, 7.6), (0, 6.0, 10.0), 1.2, solid("moss"), extend=0.2)
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -5.0), ("back", 5.0)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 5, 5, z))
            m.round_box(lb, sx * 5.4, z, 1.8, 1.8, 0.0, 6.0, solid("moss"), cut=0.6)
    return m
