"""Modwing, the Box Mod Pokémon (Electric/Flying), Vapulon evolved (the user's design): bulkier and boxier than
Vapulon, a gunmetal box-mod body with a screen-like glowing face panel, dual battery cells on its flanks with glowing
charge bands, an adjustable airflow ring round its neck, a black drip-tip beak, broad wings and trailing vapour.

Shiny: a rose-gold box mod with pink lights.

Front is -z, y is up. 18 units tall; baseScale 0.5 (0.7 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _nico import palette, puff, ring_pts, translucent, tube_z
from _route import tone

SHINY = {"gunmetal": (210, 150, 130), "cyan": (255, 140, 200), "steel": (240, 210, 200), "steel_dark": (180, 130, 120)}
P, solid, ramp = palette(SHINY)
SCALE = 0.5
HITBOX = [1.0, 1.1]
KIND = "floater"
K = 5
HEIGHT = 18
LOOK = "a boxy gunmetal box-mod bird with a glowing face panel, battery cells on its flanks, an airflow ring and a drip-tip beak"
ANIM = {"wing_flap": 26}


def boxf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.0 and 9.6 < y < 12.4:
        if any(abs(x - sx * 1.0) < 0.45 and abs(y - 11.2) < 0.45 for sx in (-1, 1)):
            return p["cyan"], p["cyan"]                                       # LED eyes on its screen
        return p["black"], None
    return tone(p["gunmetal"], face), None


def cellf(x, y, z, face, variant, **k):
    p = P(variant)
    if abs(((z + 10) % 2.4) - 1.2) < 0.25:
        return p["cyan"], p["cyan"]                                           # charge bands
    return tone(p["steel"], face), None


def build() -> Model:
    m = Model("modwing")
    top = m.bone("modwing", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -2.6, 5.0, -3.6, 2.6, 13.0, 4.4, boxf)                            # the box-mod body
    for sx in (-1, 1):
        tube_z(m, bd, sx * 3.4, 7.6, 1.2, -2.6, 3.8, cellf)                     # dual battery cells
    hd = m.bone("head", bd, (0, 13, -1))
    for a, b in zip(ring_pts((0, 13.6, -0.6), 2.2, 10, plane="xz"), ring_pts((0, 13.6, -0.6), 2.2, 10, plane="xz")[1:]):
        rod(m, hd, a, b, 0.7, solid("steel_dark"), extend=0.3)                  # the airflow ring
    rod(m, hd, (0, 12.0, -3.4), (0, 11.4, -8.0), 1.4, solid("black"), extend=0.2) # the drip-tip beak
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 2.6, 12, 0))
        x0, x1 = sorted((sx * 2.6, sx * 10.0))
        m.box(w, x0, 12.0, -2.2, x1, 12.0, 3.6, lambda *a, **k: ((190, 220, 240, 160), None),
              rotation=(0, 0, sx * 16), pivot=(sx * 2.6, 12.0, 0))
    for c, r in (((0.0, 3.6, 5.4), 1.8), ((1.2, 2.0, 8.0), 1.4), ((-1.0, 1.2, 10.4), 1.2)):
        puff(m, bd, c, r, translucent(P, "mist"))
    return m
