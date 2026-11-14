"""Ontherox, the Ice Cube Pokémon (Ice/Rock), a Liquor Meadows Pokémon (the user's design): a hefty golem carved from
crystal-clear glacial ice: a great translucent cube body with a dense frosty core and a stern face, a smaller cube head,
and arms and legs ending in heavy round ice-ball boulders, dripping meltwater.

Shiny: amber ice, as if whisky had frozen round it.

Front is -z, y is up. 26 units tall; baseScale 0.8 (1.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _liquor import palette, puff, translucent
from _route import tone

SHINY = {"ice": (240, 180, 90, 160), "ice_solid": (236, 176, 96), "glass_rim": (250, 220, 150, 170)}
P, solid, ramp = palette(SHINY)
SCALE = 0.8
HITBOX = [1.4, 1.65]
KIND = "biped"
K = 3
HEIGHT = 26
LOOK = "a hefty golem of crystal-clear ice: a translucent cube body with a frosty core, a cube head and ice-ball fists and feet"


def coref(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["ice_solid"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.5) < 0.7 and abs(y - 21.6) < 0.5:
                return (40, 90, 140), (90, 200, 255)                          # glowing eyes deep in the ice
        if abs(y - 19.8) < 0.3 and abs(x) < 1.6:
            return (60, 100, 140), None
    return P(variant)["ice"], None


def build() -> Model:
    m = Model("ontherox")
    top = m.bone("ontherox", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.box(bd, -5.0, 7.0, -4.4, 5.0, 17.0, 4.4, translucent(P, "ice"))          # the great ice cube
    m.box(bd, -2.6, 9.4, -2.2, 2.6, 14.6, 2.2, coref)                          # its dense frosty core
    hd = m.bone("head", bd, (0, 17, 0))
    m.box(hd, -3.2, 17.0, -3.0, 3.2, 23.4, 3.0, headf)
    m.box(hd, -1.6, 18.4, -1.4, 1.6, 22.0, 1.4, coref)
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 5, 15, 0))
        rod(m, ar, (sx * 5.0, 15.0, 0.0), (sx * 7.4, 9.0, -0.6), 2.6, translucent(P, "ice"), extend=0.4)
        puff(m, ar, (sx * 7.8, 7.4, -0.8), 2.6, coref)                          # ice-ball fists
        lb = m.bone(f"leg_{side}", top, (sx * 2.8, 7, 0))
        rod(m, lb, (sx * 2.8, 7.2, 0.0), (sx * 3.2, 3.0, 0.0), 2.6, translucent(P, "ice"), extend=0.4)
        puff(m, lb, (sx * 3.2, 2.0, -0.4), 2.0, coref)                          # ice-ball feet
    puff(m, bd, (3.6, 6.4, -4.0), 0.5, translucent(P, "glass_rim"))             # a meltwater drop
    return m
