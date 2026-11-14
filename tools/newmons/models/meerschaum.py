"""Meerschaum, the Pipe Carving Pokémon (Rock/Fairy), the Nicodex's Rock type (the user's design): a creamy-white
stone gargoyle carved like an ornate meerschaum pipe. Its smooth ivory stone takes on a warm amber-honey patina where
it is handled most (its paws, horns, face and pipe-bowl back), with carved filigree curls and soft bat-like wings.

Shiny: a rose-quartz carving with a gold patina.

Front is -z, y is up. 22 units tall; baseScale 0.65 (0.9 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _nico import palette
from _route import tone
from _boxmodel import mix

SHINY = {"ivory": (246, 206, 214), "ivory_shade": (224, 176, 186), "amber": (232, 196, 90)}
P, solid, ramp = palette(SHINY)
SCALE = 0.65
HITBOX = [1.0, 1.35]
KIND = "biped"
K = 4
HEIGHT = 22
LOOK = "a creamy ivory stone gargoyle carved like an ornate meerschaum pipe, with an amber patina, a pipe-bowl back and wings"
CUT = (0, 0, 0, 0)


def stonef(x, y, z, face, variant, **k):
    """Ivory with the amber patina deepening toward the extremities (handled most)."""
    p = P(variant)
    reach = min(1.0, max(0.0, (abs(x) - 3.0) / 5.0) + max(0.0, (y - 17.0) / 5.0) + max(0.0, (2.0 - y) / 3.0))
    c = mix(p["ivory"], p["amber"], reach * 0.75)
    if face in ("north", "south") and math.sin(x * 2.2) * math.sin(y * 1.8) > 0.8:
        c = mix(c, p["ivory_shade"], 0.6)                                     # carved filigree curls
    return tone(c, face), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.3) < 0.6 and abs(y - 17.4) < 0.5:
                return p["pink"], p["pink"]                                    # soft glowing eyes
    return stonef(x, y, z, face, variant)


def wingf(x, y, z, face, variant, **k):
    ax = abs(x)
    edge = 13.0 + 2.6 * math.cos((ax - 4.0) * 0.9)
    if y > 20.0 - (ax - 4.0) * 0.4 or y < edge - 4.0:
        return CUT, None
    return stonef(x, y, z, face, variant)


def build() -> Model:
    m = Model("meerschaum")
    top = m.bone("meerschaum", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 3.8, 3.2, 6.0, 14.6, stonef, cut=1.2)
    m.round_box(bd, 0, 3.6, 2.6, 2.6, 10.0, 15.6, solid("amber"), cut=0.8)      # pipe-bowl back
    m.round_box(bd, 0, 3.6, 1.8, 1.8, 15.2, 15.8, solid("tobacco_dark"), cut=0.6)
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, -0.6, 3.0, 2.8, 14.4, 19.6, facef, cut=1.0)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 19.2, 0.0), (sx * 0.5, 1, 0.6), 1.4, 3.4, stonef, tip=0.8)   # curled horns
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 2.6, 14, 2.4))
        x0, x1 = sorted((sx * 2.6, sx * 11.0))
        m.box(w, x0, 9.0, 2.6, x1, 20.0, 2.6, wingf)
        ar = m.bone(f"arm_{side}", bd, (sx * 3.8, 13, 0))
        rod(m, ar, (sx * 3.8, 13.0, 0.0), (sx * 5.0, 8.4, -1.4), 1.8, stonef, extend=0.4)
        lb = m.bone(f"leg_{side}", top, (sx * 2, 6, 0))
        rod(m, lb, (sx * 2.0, 6.4, 0.0), (sx * 2.4, 0.8, -0.6), 2.4, stonef, extend=0.4)
        m.box(lb, sx * 2.4 - 1.4, 0.0, -2.6, sx * 2.4 + 1.4, 1.2, 0.6, stonef)
    tl = m.bone("tail", bd, (0, 7, 3))
    rod(m, tl, (0, 7.0, 3.0), (0, 2.4, 8.4), 1.2, stonef, extend=0.4)
    spike(m, tl, (0, 2.4, 8.4), (0, -0.2, 1), 1.6, 1.6, solid("amber"))
    return m
