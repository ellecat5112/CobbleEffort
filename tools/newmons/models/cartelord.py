"""Cartelord, the Tobacco Baron Pokémon (Dark/Grass), the Nicodex's Dark type (the user's design): a sinister
scarecrow-like figure made of tied bales of dried tobacco leaf, dressed in a sharp pinstriped suit and a wide-brimmed
fedora, a cigar holder in its grinning stitched mouth, red eyes glinting under the brim, and leaf-fan hands with
hooked fingertips.

Shiny: a white suit and a pale leaf body.

Front is -z, y is up. 30 units tall; baseScale 0.6 (1.2 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _nico import palette
from _route import tone

SHINY = {"suit": (230, 228, 220), "pinstripe": (170, 168, 160), "tobacco": (214, 186, 120),
         "tobacco_dark": (180, 150, 90)}
P, solid, ramp = palette(SHINY)
SCALE = 0.6
HITBOX = [1.0, 1.9]
KIND = "biped"
K = 3
HEIGHT = 30
LOOK = "a sinister tobacco-bale scarecrow in a pinstriped suit and fedora, red eyes under the brim, a cigar holder"


def suitf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south") and abs(x) < 1.0 and y > 14.0:
        return p["white"] if face == "north" else p["suit"], None             # shirt front
    if face == "north" and abs(x) < 0.4 and y > 17.0:
        return p["red"], None                                                 # a red tie
    if face in ("north", "south") and (x % 1.5) < 0.2:
        return p["pinstripe"], None
    if face in ("east", "west") and (z % 1.5) < 0.2:
        return p["pinstripe"], None
    return tone(p["suit"], face), None


def leaff(x, y, z, face, variant, **k):
    p = P(variant)
    if (int(y * 1.4) % 3) == 0:
        return tone(p["tobacco_dark"], face), None                            # bundled leaf
    return tone(p["tobacco"], face), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.5 and abs(y - 24.6) < 0.4:
                return p["red"], p["red"]                                     # glinting red eyes
        if abs(y - 22.6) < 0.25 and abs(x) < 1.8:
            return p["pupil"], None                                           # a stitched grin
        if abs(y - 22.6) < 0.7 and abs(x) < 1.8 and (int(x * 2.5) % 2 == 0):
            return p["pupil"], None
    return leaff(x, y, z, face, variant)


def build() -> Model:
    m = Model("cartelord")
    top = m.bone("cartelord", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 3.6, 2.4, 11.0, 21.0, suitf, cut=0.8)                 # the suit jacket
    hd = m.bone("head", bd, (0, 21, 0))
    m.round_box(hd, 0, 0, 2.6, 2.6, 20.6, 26.4, facef, cut=0.8)                 # the leaf-bale head
    m.box(hd, -5.0, 26.0, -5.0, 5.0, 26.6, 5.0, solid("suit"))                  # the fedora brim
    m.round_box(hd, 0, 0, 2.8, 2.8, 26.4, 29.4, solid("suit"), cut=0.8)         # the crown
    m.round_box(hd, 0, 0, 2.9, 2.9, 26.4, 27.4, solid("red"), cut=0.8)          # hat band
    rod(m, hd, (1.0, 22.6, -2.4), (3.4, 23.4, -6.4), 0.6, solid("black"), extend=0.2)   # cigar holder
    m.box(hd, 3.0, 23.0, -7.2, 4.0, 24.0, -6.2, solid("ember"))
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3.6, 20, 0))
        rod(m, ar, (sx * 3.6, 20.0, 0.0), (sx * 5.0, 13.4, -0.6), 2.0, suitf, extend=0.4)
        for d in ((-0.4, -1, -0.3), (0.0, -1, -0.5), (0.4, -1, -0.3)):        # leaf-fan hands, hooked tips
            spike(m, ar, (sx * 5.0, 13.0, -0.6), (sx * 0.3 + d[0], d[1], d[2]), 1.0, 3.0, leaff, tip=0.6)
        lb = m.bone(f"leg_{side}", top, (sx * 1.6, 11, 0))
        rod(m, lb, (sx * 1.6, 11.4, 0.0), (sx * 1.8, 1.0, 0.0), 2.0, suitf, extend=0.4)
        m.box(lb, sx * 1.8 - 1.2, 0.0, -2.4, sx * 1.8 + 1.2, 1.2, 1.0, solid("black"))   # shoes
        spike(m, lb, (sx * 1.8, 6.0, 1.0), (sx * 0.6, -0.2, 1), 0.8, 1.6, leaff)          # leaf poking out
    return m
