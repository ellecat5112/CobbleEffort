"""Elastigoose, the Rubber Goose Pokémon (Water/Flying), hand-built from boxes from the user's design.

Squeakling stretched into a goose: a long, long glossy yellow rubber neck reaching up and forward, a round head with a
huge orange bill honking wide open over a purple tongue, a black tuft, eyes squeezed shut mid-honk, a plump body with
broad white wings (grey underneath) and a white tail, and long orange legs with webbed feet.

Front is -z, y is up. 32 units tall to its bill; baseScale 0.75 (1.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix
from _route import pal, tone

SCALE = 0.75
HITBOX = [0.9, 1.5]
KIND = "biped"
K = 4
HEIGHT = 32
LOOK = ("a goose of glossy yellow rubber with a long, long neck, a huge orange bill honking wide open over a purple "
        "tongue, broad white wings and long orange legs with webbed feet")

BASE = {"yellow": (252, 214, 40), "yellow_dark": (226, 170, 20), "bill": (248, 130, 40), "bill_in": (120, 66, 40),
        "tongue": (150, 70, 120), "white": (246, 246, 250), "grey": (176, 174, 190), "black": (30, 28, 30),
        "shine": (255, 250, 210)}
SHINY = {"yellow": (255, 150, 190), "yellow_dark": (220, 100, 150), "shine": (255, 235, 245)}


def P(variant):
    return pal(BASE, SHINY, variant)


def rubber(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "up") and (x * 0.8 + y * 0.6) % 6.0 < 0.5:
        return p["shine"], None
    return tone(p["yellow"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 27.4) < 0.25 and abs(z + 9.5) < 0.9:
        return p["black"], None                                           # eyes squeezed shut, honking
    return rubber(x, y, z, face, variant)


def feathers(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["grey"] if face == "down" or y < 10.5 else p["white"], face), None


def bill(inner):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == inner:
            return p["bill_in"], None
        return tone(p["bill"], face), None
    return s


def tongue(x, y, z, face, variant, **k):
    return tone(P(variant)["tongue"], face), None


def orange(x, y, z, face, variant, **k):
    return tone(P(variant)["bill"], face), None


def black(x, y, z, face, variant, **k):
    return P(variant)["black"], None


def build() -> Model:
    m = Model("elastigoose")
    top = m.bone("elastigoose", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11, 0))
    m.round_box(bd, 0, 2, 4.5, 6, 8, 16, rubber, cut=2)                     # plump rubber body
    m.box(bd, -2.5, 12, 7, 2.5, 15, 10, feathers)                            # white tail
    chain(m, bd, [(0, 14.5, -2), (0, 18, -4), (0, 22, -6.5), (0, 25.5, -8.5)], [2.5, 2.2, 2], rubber)   # the long neck
    hd = m.bone("head", bd, (0, 25.5, -8.5))
    m.round_box(hd, 0, -9.3, 2.5, 2.5, 25, 30, headf, cut=1)
    chain(m, hd, [(0, 29.8, -9.3), (0.8, 31.6, -8.4), (2.2, 32, -7.4)], [0.8, 0.7], black)        # tuft
    jaw = m.bone("jaw", hd, (0, 27, -11))
    m.box(hd, -2.2, 28, -16, 2.2, 29, -11, bill("down"), rotation=(-30, 0, 0), pivot=(0, 28.5, -11))   # upper bill, flung open
    m.box(jaw, -2, 25.5, -15, 2, 26.5, -11, bill("up"), rotation=(12, 0, 0), pivot=(0, 26, -11))       # lower bill
    m.box(jaw, -1.2, 26.4, -13.8, 1.2, 27.2, -11.2, tongue, rotation=(12, 0, 0), pivot=(0, 26, -11))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 4.5, 15, 1))
        x0, x1 = sorted((sx * 4, sx * 5.5))
        m.box(w, x0, 9.5, -2, x1, 16, 9, feathers)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2, 9, 1))
        m.box(lg, sx * 2 - 0.5, 1, 0.5, sx * 2 + 0.5, 9.5, 1.5, orange)
        m.box(lg, sx * 2 - 1.8, 0, -3, sx * 2 + 1.8, 1, 1.5, orange)          # webbed foot
    return m
