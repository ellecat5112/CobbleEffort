"""Meadbee, the Mead Pokémon (Bug/Fairy), a Liquor Meadows Pokémon (the user's design): a plump, fuzzy golden-amber
bumblebee with dark brown stripes, big friendly eyes, little antennae, translucent honeycomb wings, and a tiny clay
amphora of fermented wildflower nectar hugged in its arms.

Shiny: a pale cream bee with rose stripes.

Front is -z, y is up. 15 units tall; baseScale 0.4 (0.35 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _liquor import eye_on, palette, puff, tiers
from _route import tone

SHINY = {"honey": (250, 236, 200), "honey_dark": (220, 200, 160), "bee_brown": (200, 90, 120)}
P, solid, ramp = palette(SHINY)
SCALE = 0.4
HITBOX = [0.8, 0.85]
KIND = "floater"
K = 6
HEIGHT = 15
LOOK = "a plump golden-amber bumblebee with honeycomb wings hugging a tiny clay amphora of nectar"
ANIM = {"wing_flap": 34}
eyes = eye_on(P, "bee_brown", [(-1.4, 10.8), (1.4, 10.8)], 1.0)
CUT = (0, 0, 0, 0)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if ((z + 20) % 3.0) < 1.2 and z > -2.0:
        return tone(p["bee_brown"], face), None
    return tone(p["honey"], face), None


def headf(x, y, z, face, variant, **k):
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    p = P(variant)
    if face == "north" and abs(y - 9.2) < 0.25 and abs(x) < 0.7:
        return p["bee_brown"], None
    return tone(p["honey"], face), None


def combf(x, y, z, face, variant, **k):
    p = P(variant)
    q = x * 1.6
    r = z * 1.6 + (0.5 if int(math.floor(q)) % 2 else 0.0)
    if min(abs(q - round(q)), abs(r - round(r))) < 0.12:
        return p["honey_dark"][:3] + (200,), None                            # hexagonal cell walls
    return p["comb"], None


def build() -> Model:
    m = Model("meadbee")
    top = m.bone("meadbee", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 1.4, 3.6, 4.6, 3.4, 10.0, bodyf, cut=1.4)             # the plump striped body
    spike(m, bd, (0, 5.4, 5.8), (0, -0.3, 1), 1.0, 1.6, solid("bee_brown"))     # the stinger
    hd = m.bone("head", bd, (0, 10, -2))
    m.round_box(hd, 0, -2.6, 3.0, 2.6, 7.6, 13.0, headf, cut=1.0)
    for sx in (-1, 1):
        chain(m, hd, [(sx * 1.0, 12.8, -3.0), (sx * 1.8, 14.6, -3.6), (sx * 2.6, 15.2, -3.4)], [0.5, 0.5],
              solid("bee_brown"))
        puff(m, hd, (sx * 2.7, 15.2, -3.4), 0.6, solid("bee_brown"))
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 2, 10, 1))
        x0, x1 = sorted((sx * 2.0, sx * 8.6))
        m.box(w, x0, 10.0, -1.0, x1, 10.0, 4.0, combf, rotation=(0, 0, sx * 24), pivot=(sx * 2.0, 10.0, 1.0))
        ar = m.bone(f"arm_{side}", bd, (sx * 2.6, 7, -2))
        rod(m, ar, (sx * 2.6, 7.0, -2.2), (sx * 1.2, 5.6, -4.4), 0.8, solid("bee_brown"), extend=0.2)
    ap = m.bone("amphora", bd, (0, 5, -4.6))
    tiers(m, ap, [(3.0, 3.6, 0.6), (3.6, 6.0, 1.3), (6.0, 6.8, 0.6), (6.8, 7.2, 0.8)], solid("clay"), cx=0.0, cz=-4.8)
    for sx in (-1, 1):
        rod(m, ap, (sx * 0.6, 6.8, -4.8), (sx * 1.4, 6.0, -4.8), 0.4, solid("clay_dark"), extend=0.1)
    return m
