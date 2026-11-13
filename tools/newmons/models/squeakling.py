"""Squeakling, the Rubber Duck Pokémon (Water/Flying), a route-one Pokémon, hand-built from boxes from the user's design.

A short, stout rubber ducky: a glossy yellow body (with the shine of rubber), a round head with little black eyes, a
wide flat orange bill, a black feather tuft on top, stubby wings held out, a turned-up tail and orange feet.

Front is -z, y is up. 13 units tall to its tuft; baseScale 0.38 (0.25 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix
from _route import dot_eye, pal, tone

SCALE = 0.38
HITBOX = [1.05, 0.79]
KIND = "biped"
K = 6
LOOK = ("a short, stout glossy yellow rubber ducky with a flat orange bill, little black eyes, a black tuft, stubby "
        "wings and orange feet")

BASE = {"yellow": (252, 214, 40), "yellow_dark": (226, 170, 20), "bill": (248, 130, 40), "bill_dark": (200, 90, 30),
        "black": (30, 28, 30), "shine": (255, 250, 210), "belly": (255, 236, 140)}
SHINY = {"yellow": (255, 150, 190), "yellow_dark": (220, 100, 150), "belly": (255, 210, 225), "shine": (255, 235, 245)}


def rubber(x, y, z, face, variant, shine_at=None, **k):
    p = pal(BASE, SHINY, variant)
    if shine_at and face in ("north", "up", "east") and math.hypot(x - shine_at[0], y - shine_at[1]) < 0.7:
        return p["shine"], None                                     # the shine of rubber
    if face == "north" and y < 4:
        return tone(p["belly"], face), None
    return tone(p["yellow"], face), None


def headf(x, y, z, face, variant, **k):
    if face == "north":
        for sx in (-1, 1):
            e = dot_eye(x - sx * 1.6, y - 10.0, 0.5, 0.6)
            if e:
                return e
    return rubber(x, y, z, face, variant, shine_at=(-1.6, 11.2))


def bill(x, y, z, face, variant, **k):
    p = pal(BASE, SHINY, variant)
    return tone(p["bill"] if face != "down" else p["bill_dark"], face), None


def black(x, y, z, face, variant, **k):
    return pal(BASE, SHINY, variant)["black"], None


def build() -> Model:
    m = Model("squeakling")
    top = m.bone("squeakling", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0.5, 4, 4.5, 1, 6.5, lambda *a, **k: rubber(*a, shine_at=(-2.2, 5.3), **k), cut=2)
    m.box(bd, -1.5, 5, 4, 1.5, 7, 6, rubber)                                  # turned-up tail
    hd = m.bone("head", bd, (0, 6.5, -1))
    m.round_box(hd, 0, -1.5, 3, 3, 6, 12, headf, cut=1)
    m.box(hd, -2, 8, -6.5, 2, 9, -4, bill)                                    # the wide flat bill
    for sx in (-0.6, 0.6):
        chain(m, hd, [(sx, 11.8, -1.5), (sx * 1.8, 13, -0.6), (sx * 2.6, 13.2, 0.6)], [0.7, 0.6], black)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 4, 5, 0.5))
        x0, x1 = sorted((sx * 3.6, sx * 5.4))
        m.box(w, x0, 3, -1, x1, 5.6, 2.5, rubber)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 1.5, 0))
        m.box(lg, sx * 1.6 - 1.2, 0, -2.6, sx * 1.6 + 1.2, 1, 0.6, bill)
    return m
