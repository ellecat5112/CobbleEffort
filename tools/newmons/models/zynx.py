"""Zynx, the Pouch Pokémon (Fairy/Ice), the Nicodex's Fairy type (the user's design): a sweet, pastel sprite that
lives in a round mint tin: a little pillow-shaped pouch creature with a frosty white body, mint cheeks and sparkling
blue eyes, peeking out of a pastel tin whose lid it wears like a hat.

Shiny: a pink tin and a peach pouch.

Front is -z, y is up. 12 units tall; baseScale 0.4 (0.3 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _nico import disc_z, eye_on, palette
from _route import tone

SHINY = {"mint": (250, 180, 210), "mint_dark": (220, 130, 170), "white": (255, 230, 214)}
P, solid, ramp = palette(SHINY)
SCALE = 0.4
HITBOX = [0.7, 0.55]
KIND = "biped"
K = 6
HEIGHT = 12
LOOK = "a pastel pillow-pouch sprite with mint cheeks and sparkly eyes, peeking out of a round mint tin, its lid a hat"
eyes = eye_on(P, "cyan", [(-1.3, 6.8), (1.3, 6.8)], 0.8)


def pouchf(x, y, z, face, variant, **k):
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    p = P(variant)
    if face == "north" and abs(abs(x) - 2.4) < 0.6 and abs(y - 5.6) < 0.4:
        return p["mint"], None                                                # mint cheeks
    if face == "north" and abs(y - 5.2) < 0.25 and abs(x) < 0.5:
        return p["pupil"], None
    return tone(p["white"], face), None


def tinf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and abs(math.hypot(x, z) - 2.6) < 0.4:
        return p["white"], None                                               # a printed ring on the lid
    if face in ("east", "west", "north", "south") and ((x + z) % 2.0) < 0.4:
        return tone(p["mint_dark"], face), None                               # ridged edge
    return tone(p["mint"], face), None


def build() -> Model:
    m = Model("zynx")
    top = m.bone("zynx", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.round_box(bd, 0, 0, 4.6, 4.6, 0.0, 3.0, tinf, cut=1.6)                    # the tin
    m.round_box(bd, 0, 0, 3.6, 2.6, 2.6, 8.6, pouchf, cut=1.2)                  # the pillow pouch
    hd = m.bone("head", bd, (0, 8, 0))
    m.round_box(hd, 0, 0.6, 4.4, 4.4, 8.4, 9.8, tinf, cut=1.4)                  # the lid, worn as a hat
    for d in ((-0.4, 1, 0.0), (0.5, 1, 0.2)):
        spike(m, hd, (d[0] * 3, 9.6, 0.0), d, 0.8, 1.6, solid("ice"))             # frost sparkles
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3.6, 5, 0))
        m.box(ar, sx * 3.6 - (1.2 if sx < 0 else 0), 4.0, -0.6, sx * 3.6 + (1.2 if sx > 0 else 0), 5.4, 0.6,
              solid("white"))
        lb = m.bone(f"leg_{side}", top, (sx * 2, 1, 0))
        m.box(lb, sx * 2.0 - 0.8, 0.0, -2.0, sx * 2.0 + 0.8, 1.0, -1.0, solid("white"))   # little feet peeking out
    return m
