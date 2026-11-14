"""Maltwort, the Mash Pokémon (Grass/Fairy), Hopsprout evolved (the user's design): a bubbling, copper-kettle-shaped
creature with a round riveted copper body, a cheerful face, a spout, sprouting golden barley ears for arms and a
frothy crown of white foam bubbling over its top.

Shiny: a silver kettle with pink foam.

Front is -z, y is up. 20 units tall; baseScale 0.55 (0.8 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _liquor import eye_on, palette, puff, tiers
from _route import tone

SHINY = {"copper": (206, 210, 220), "copper_dark": (150, 154, 166), "copper_light": (236, 240, 248), "foam": (250, 210, 220)}
P, solid, ramp = palette(SHINY)
SCALE = 0.55
HITBOX = [1.0, 1.15]
KIND = "biped"
K = 4
HEIGHT = 20
LOOK = "a bubbling round copper kettle with barley-ear arms, a spout and a frothy crown of white foam"
eyes = eye_on(P, "hop_dark", [(-1.6, 10.6), (1.6, 10.6)], 0.9)


def kettlef(x, y, z, face, variant, **k):
    p = P(variant)
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    if face == "north" and abs(y - 8.8) < 0.3 and abs(x) < 1.2:
        return p["pupil"], None
    if abs(y - 6.0) < 0.3 or abs(y - 13.4) < 0.3:
        return p["copper_dark"], None                                         # riveted seams
    return tone(p["copper_light"] if face == "up" else p["copper"], face), None


def barleyf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["ivy"] if (int(abs(x) * 2 + y * 2) % 2) else p["gold_dark"], face), None


def build() -> Model:
    m = Model("maltwort")
    top = m.bone("maltwort", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    tiers(m, bd, [(2.0, 3.4, 3.6), (3.4, 6.0, 5.2), (6.0, 11.6, 5.8), (11.6, 13.6, 5.0), (13.6, 14.6, 3.6)], kettlef)
    rod(m, bd, (3.6, 8.0, -2.6), (6.6, 11.4, -4.6), 1.4, solid("copper"), extend=0.3)        # the spout
    hd = m.bone("head", bd, (0, 14, 0))
    for c, r in (((0, 15.6, 0), 2.6), ((-2.2, 15.0, 1.0), 1.8), ((2.0, 15.2, -1.0), 1.8), ((0.6, 17.4, 0.4), 1.6),
                 ((-3.4, 14.0, -1.6), 1.2), ((3.4, 13.8, 1.8), 1.1)):
        puff(m, hd, c, r, solid("foam"))                                          # the frothy foam crown
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 5.4, 10, 0))
        rod(m, ar, (sx * 5.4, 10.0, 0.0), (sx * 8.0, 14.6, -0.4), 0.8, solid("hop_dark"), extend=0.2)   # stalk
        for i in range(5):                                                        # the barley ear
            t = 0.45 + i * 0.13
            px, py = sx * (5.4 + 2.6 * t), 10.0 + 4.6 * t
            for d in (-1, 1):
                spike(m, ar, (px, py, -0.4), (sx * 0.5 + d * 0.5, 0.8, 0.0), 0.7, 1.2, barleyf)
        spike(m, ar, (sx * 8.0, 14.6, -0.4), (sx * 0.3, 1, 0), 0.4, 3.0, solid("ivy"))                 # its awn
        lb = m.bone(f"leg_{side}", top, (sx * 2.4, 2.4, 0))
        m.round_box(lb, sx * 2.4, -0.2, 1.1, 1.3, 0.0, 2.6, solid("copper_dark"), cut=0.4)
    return m
