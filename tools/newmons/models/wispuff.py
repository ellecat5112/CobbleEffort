"""Wispuff, the Smoke Puff Pokémon (Flying/Ghost), the Nicodex's Flying type (the user's design): a ghostly,
weightless puff of second-hand smoke, a plume of soft grey-white puffs with a faint, sleepy face and trailing ribbons
of smoke instead of a body. It lingers in rooms long after the smoker has gone.

Shiny: lavender smoke.

Front is -z, y is up. 16 units tall; baseScale 0.55 (0.55 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, chain
from _nico import palette, puff

SHINY = {"smoke": (200, 170, 236, 130), "mist": (232, 210, 250, 120)}
P, solid, ramp = palette(SHINY)
SCALE = 0.55
HITBOX = [0.9, 1.0]
KIND = "floater"
K = 5
HEIGHT = 16
LOOK = "a ghostly plume of soft grey-white smoke puffs with a faint sleepy face and trailing smoke ribbons"


def smokef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and z < -3.0:
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.7 and abs(y - 10.6) < 0.28:
                return (50, 46, 60, 220), None                                # sleepy closed eyes
        if abs(x) < 0.6 and abs(y - 9.0) < 0.5:
            return (60, 52, 70, 200), None                                    # a small "o" mouth
    return p["smoke"], None


def build() -> Model:
    m = Model("wispuff")
    top = m.bone("wispuff", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    hd = m.bone("head", bd, (0, 9, 0))
    puff(m, hd, (0, 10.0, -0.4), 3.4, smokef)                                   # the face puff
    for c, r in (((-2.8, 12.2, 0.6), 2.0), ((2.6, 12.6, 0.4), 2.2), ((0.2, 13.8, 1.4), 2.0)):
        puff(m, hd, c, r, smokef)
    for c, r in (((-1.6, 6.8, 1.0), 2.2), ((1.8, 6.4, 0.8), 1.8)):
        puff(m, bd, c, r, smokef)
    tl = m.bone("tail", bd, (0, 5, 2))
    chain(m, tl, [(0, 5.0, 2.0), (1.4, 3.0, 4.0), (-0.6, 1.6, 6.4), (1.0, 0.8, 9.0)], [2.0, 1.6, 1.0],
          lambda *a, **k: (P(k.get("variant"))["mist"], None))                  # a trailing ribbon
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3, 8, 0))
        chain(m, ar, [(sx * 3.0, 8.0, 0.0), (sx * 5.6, 7.0, 1.0), (sx * 7.0, 5.0, 2.6)], [1.4, 1.0],
              lambda *a, **k: (P(k.get("variant"))["mist"], None))
    return m
