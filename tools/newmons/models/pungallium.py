"""Pungallium, the Stench Bloom Pokémon (Grass/Poison), Shallorn evolved, after the art of the A. Fakemon fanpage (the
name is ours): a green onion body on long thin legs under a great purple allium flower-head, a mass of florets so
pungent that its own eyes stream with tears. It holds its hands to its face and a long orange tongue lolls out in
disgust; leaf tendrils curl from its sides, and a little purple puff of stink drifts beside it.

Shiny: a rose-red body with a golden flower-head.

Front is -z, y is up. 31 units tall; baseScale 0.65 (1.25 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _onion import P, bulb, ramp, solid, teary_eye
from _route import tone

SCALE = 0.65
HITBOX = [1.4, 1.95]
KIND = "biped"
K = 3
HEIGHT = 31
LOOK = ("a green onion body on thin legs under a great purple allium flower-head, streaming eyes, hands to its face, a "
        "long orange tongue and leaf tendrils, a purple puff of stink beside it")
CENTRE = (0.0, 23.0, 0.6)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = teary_eye(p, x - sx * 1.8, y - 14.4, 0.85, closed=True)
            if e:
                return e, None
    return tone(p["bulb"], face), None


def flowerf(x, y, z, face, variant, **k):
    """Purple florets: little four-petalled flowers dotted over the flower-head."""
    p = P(variant)
    a, b = (x, y) if face in ("north", "south") else (z, y) if face in ("east", "west") else (x, z)
    ca, cb = round(a / 2.6) * 2.6, round(b / 2.6) * 2.6
    da, db = a - ca, b - cb
    if math.hypot(da, db) < 0.3:
        return p["purple_light"], None
    if (abs(da) < 0.3 or abs(db) < 0.3) and math.hypot(da, db) < 1.0:
        return p["purple_dark"], None
    return tone(p["purple"], face), None


def build() -> Model:
    m = Model("pungallium")
    top = m.bone("pungallium", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    bulb(m, bd, 13.0, 5.2, 9.0, bodyf)                                         # the green onion body
    rod(m, bd, (0, 12.6, -4.6), (0.4, 6.6, -7.8), 3.6, ramp("orange", "orange_light"), extend=0.3, t2=1.2)   # tongue
    for sx in (-1, 1):
        rod(m, bd, (sx * 4.4, 14.0, 0.0), (sx * 8.6, 17.0, -1.0), 1.4, ramp("green", "green_light"), extend=0.3)  # tendrils
        spike(m, bd, (sx * 8.6, 17.0, -1.0), (sx * 0.4, 1, 0), 1.2, 2.4, solid("green_light"))

    hd = m.bone("head", bd, (0, 17, 0))
    cx, cy, cz = CENTRE
    for dy, r in ((-4.6, 4.2), (-2.4, 6.4), (0.0, 7.4), (2.4, 6.8), (4.6, 5.0), (6.2, 2.8)):   # the flower-head
        m.round_box(hd, cx, cz, r, r, cy + dy - 1.2, cy + dy + 1.2, flowerf, cut=max(1, round(r * 0.35)))
    for c in ((-6.0, 26.0, -2.0), (6.4, 25.0, 1.0), (-2.0, 29.6, -3.0), (3.0, 28.4, -4.4)):
        m.round_box(hd, c[0], c[2], 1.6, 1.6, c[1] - 1.5, c[1] + 1.5, flowerf, cut=0.6)   # floret lumps

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.8, 9, 0))
        rod(m, lb, (sx * 1.8, 9.0, 0.0), (sx * 2.4, 4.0, 0.6), 1.4, solid("green_dark"), extend=0.4)
        rod(m, lb, (sx * 2.4, 4.0, 0.6), (sx * 2.2, 0.8, -0.2), 1.2, solid("green_dark"), extend=0.4)
        m.round_box(lb, sx * 2.2, -1.0, 1.2, 1.8, 0.0, 1.0, solid("green_dark"), cut=0.4)
        ar = m.bone(f"arm_{side}", bd, (sx * 4.4, 12.4, 0))                      # hands to its face
        rod(m, ar, (sx * 4.4, 12.4, 0.0), (sx * 3.6, 13.6, -4.8), 1.2, solid("green"), extend=0.3)
        m.round_box(ar, sx * 3.2, -5.4, 0.9, 0.7, 13.0, 15.0, solid("green"), cut=0.3)

    pf = m.bone("stink", bd, (-8, 22, -2))                                       # a purple puff of stink
    for c in ((-8.4, 21.0, -2.0), (-9.6, 22.4, -1.6), (-7.4, 22.6, -2.2)):
        m.round_box(pf, c[0], c[2], 1.2, 1.2, c[1] - 1.0, c[1] + 1.0, solid("purple_light"), cut=0.4)
    for x in (-1.8, 0.0, 1.8):                                                   # stink lines over its head
        rod(m, pf, (x, 31.2, 0.6), (x + 0.6, 33.6, 0.8), 1.0, lambda *a, variant=None, **k: (P(variant)["stink"], None),
            extend=0.2, t2=0.6)
    return m
