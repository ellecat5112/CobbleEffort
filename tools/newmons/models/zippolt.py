"""Zippolt, the Lighter Pokémon (Steel/Electric), the Nicodex's Steel type (the user's design): a polished chrome
flip-top lighter come to life. Its hinged lid is its head, flipped open over a chimney of windscreen holes cradling a
crackling flame and a flint wheel; little steel legs, and arc-spark eyes on its case.

Shiny: a brushed brass case with a blue flame.

Front is -z, y is up. 16 units tall; baseScale 0.45 (0.45 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _nico import palette
from _route import tone

SHINY = {"steel": (226, 190, 110), "steel_dark": (170, 136, 70), "ember": (80, 160, 255), "ember_hot": (190, 230, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.45
HITBOX = [0.6, 0.85]
KIND = "biped"
K = 5
HEIGHT = 16
LOOK = "a polished chrome flip-top lighter with its lid open over a chimney and flame, spark eyes and little steel legs"
CUT = (0, 0, 0, 0)


def casef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.0) < 0.5 and abs(y - 8.6) < 0.6:
                return p["cyan"], p["cyan"]                                   # arc-spark eyes
        if abs(y - 6.0) < 0.2:
            return p["steel_dark"], None                                      # the lid seam
    if face in ("east", "west") and ((y * 1.0) % 3.0) < 0.3:
        return tone(p["steel_dark"], face), None                              # brushed lines
    return tone(p["steel"], face), None


def chimneyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south", "east", "west"):
        u = x if face in ("north", "south") else z
        if (int((u + 4) * 1.6) % 2 == 0) and int((y - 10) * 1.6) % 2 == 0:
            return CUT, None                                                  # windscreen holes
    return tone(p["steel"], face), None


def flamef(x, y, z, face, variant, **k):
    p = P(variant)
    w = 1.4 - (y - 13.0) * 0.32
    if abs(x if face in ("north", "south") else z) > w:
        return CUT, None
    c = p["ember_hot"] if y < 14.0 else p["ember"]
    return c, c


def build() -> Model:
    m = Model("zippolt")
    top = m.bone("zippolt", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.box(bd, -3.0, 2.0, -1.8, 3.0, 10.0, 1.8, casef)                          # the case
    m.box(bd, -2.2, 10.0, -1.2, 1.6, 13.0, 1.2, chimneyf)                       # the chimney
    m.box(bd, 1.6, 10.4, -0.6, 2.8, 11.6, 0.6, solid("steel_dark"))             # the flint wheel
    m.box(bd, 0.0, 12.8, -1.4, 0.0, 17.2, 1.4, flamef)                          # the flame (crossed planes)
    m.box(bd, -1.4, 12.8, 0.0, 1.4, 17.2, 0.0, flamef)
    hd = m.bone("head", bd, (3, 10, 0))
    m.box(hd, 3.0, 10.0, -1.8, 4.2, 15.0, 1.8, casef, rotation=(0, 0, -12), pivot=(3.0, 10.0, 0.0))   # the open lid
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3, 7, 0))
        rod(m, ar, (sx * 3.0, 7.0, 0.0), (sx * 4.6, 4.6, -0.6), 1.0, solid("steel_dark"), extend=0.4)
        lb = m.bone(f"leg_{side}", top, (sx * 1.6, 2, 0))
        rod(m, lb, (sx * 1.6, 2.2, 0.0), (sx * 1.8, 0.4, -0.2), 1.0, solid("steel_dark"), extend=0.3)
        m.box(lb, sx * 1.8 - 0.8, 0.0, -1.4, sx * 1.8 + 0.8, 0.6, 0.6, solid("steel_dark"))
    return m
