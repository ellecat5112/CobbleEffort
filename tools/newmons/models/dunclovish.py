"""Dunclovish, the Fish Fossil Pokémon (Water/Steel; the art the user shared, name kept): the Fossilized Fish as it
really was, an armoured placoderm: a great blue-grey armour plate over its head and shoulders, mottled dark, with a
heavy jaw and a small round eye, then a long pale-blue body curving back to silver-white fins and a forked tail.

Shiny: bronze armour on a sea-green body.

Front is -z, y is up. 16 units tall; baseScale 1.0 (2.0 m long). Swims.
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _purefossil import body_along, eye_at, palette, toned
from _route import tone

BASE = {"armour": (126, 156, 196), "armour_dark": (66, 90, 130), "body": (150, 196, 228), "body_dark": (110, 160, 200),
        "fin": (232, 238, 244), "fin_dark": (190, 200, 214), "eye": (40, 40, 50), "pupil": (20, 20, 24),
        "white": (250, 250, 250), "jaw": (90, 110, 140)}
SHINY = {"armour": (196, 150, 90), "armour_dark": (140, 96, 50), "body": (130, 210, 180), "body_dark": (90, 170, 140)}
P, solid, ramp = palette(BASE, SHINY)
SCALE = 1.0
HITBOX = [1.4, 1.0]
KIND = "floater"
K = 3
HEIGHT = 16
LOOK = ("an armoured placoderm fish: a great mottled blue-grey plate over its head and shoulders, a heavy jaw, a long "
        "pale-blue body and silver-white fins")


def armour(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        e = eye_at(p, z + 7.8, y - 10.4, 0.7)
        if e:
            return e, None
        if abs(y - 8.2) < 0.4 and z < -6:
            return tone(p["jaw"], face), None                           # the line of its heavy jaw
    if math.sin(x * 1.3 + z * 0.9) + math.cos(y * 1.1 - z * 0.7) > 1.1:
        return tone(p["armour_dark"], face), None                       # dark mottling
    return tone(p["armour"], face), None


def body(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["body"] if y > 8.6 else p["body_dark"], face), None


def build() -> Model:
    m = Model("dunclovish")
    top = m.bone("dunclovish", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    hd = m.bone("head", bd, (0, 9.5, -4))
    body_along(m, hd, [(-9.5, -5.0, 9.8, 3.4, 3.6), (-5.0, 0.0, 10.0, 3.8, 3.8)], armour)   # the armour plate
    body_along(m, bd, [(0.0, 5.0, 9.6, 3.0, 3.0), (5.0, 9.0, 9.0, 2.4, 2.4)], body)
    spike(m, bd, (0, 12.8, 2.0), (0, 1, 0.8), 1.2, 3.0, solid("fin"), tip=0.5)          # dorsal fin
    for sx in (-1, 1):                                                                  # pectoral fins
        spike(m, bd, (sx * 3.0, 8.0, -1.0), (sx, -0.5, 0.8), 1.4, 4.0, solid("fin"), tip=0.6)
    tl = m.bone("tail", bd, (0, 9, 9))
    chain(m, tl, [(0, 9.0, 9.0), (0, 9.6, 12.4), (0, 10.6, 15.0)], [3.2, 2.2], body)
    for d in ((0, 1, 0.7), (0, -0.6, 0.9)):                                            # the forked tail
        spike(m, tl, (0, 10.6, 15.0), d, 1.6, 4.4, solid("fin_dark"), tip=0.6)
    return m
