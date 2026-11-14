"""Whissant, the Whistle Chick Pokémon (Grass), the grass starter of the second A. Fakemon trio, after the art of the
A. Fakemon fanpage (the art's own name): a round green chick with a smug, half-lidded eye, holding one leafy wing up
over its little beak as it whistles. Yellow spots dot its crown and pale belly, two small points stand up on its head
and leafy tufts curl from its cheeks and back.

Shiny: rose-pink with lilac spots.

Front is -z, y is up. 18 units tall; baseScale 0.38 (0.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _songbird import P, solid

SCALE = 0.38
HITBOX = [0.7, 1.1]
KIND = "biped"
K = 5
HEIGHT = 18
LOOK = ("a round green chick with a smug half-lidded eye, a leafy wing over its beak as it whistles, yellow spots on its "
        "crown and belly and two small points on its head")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y < 9.0:
        for cx, cy in ((-1.6, 5.0), (1.4, 3.4), (1.8, 7.2)):
            if math.hypot(x - cx, y - cy) < 0.8:
                return p["yellow"], None                                      # belly spots
        return tone(p["green_light"], face), None
    return tone(p["green"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        for cx, cz in ((-1.4, -1.0), (0.4, -1.6), (1.6, 0.4), (-0.6, 1.0)):
            if math.hypot(x - cx, z - cz) < 0.6:
                return p["yellow"], None                                      # crown spots
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.4, y - 13.6
            if abs(dx) < 0.8 and -0.5 < dy < 0.3:
                return (p["green_dark"] if dy > 0.0 else p["pupil"]), None   # smug half-lidded eyes
    return tone(p["green"], face), None


def build() -> Model:
    m = Model("whissant")
    top = m.bone("whissant", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.0, 4.2, 3.8, 1.2, 10.6, bodyf, cut=1.6)
    spike(m, bd, (0, 8.0, 3.6), (0, 0.4, 1), 2.0, 2.4, solid("green_dark"), tip=0.8)        # a leafy tuft on its back

    hd = m.bone("head", bd, (0, 10.5, 0))
    m.round_box(hd, 0, -0.4, 3.6, 3.4, 10.0, 16.0, headf, cut=1.4)
    spike(m, hd, (0, 12.0, -3.6), (0, -0.2, -1), 1.4, 1.8, solid("beak"))      # its little beak
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 15.6, 0.0), (sx * 0.4, 1, 0), 1.4, 2.0, solid("green_dark"))    # points on its head
        spike(m, hd, (sx * 3.4, 12.0, 0.6), (sx * 1, -0.2, 0.4), 1.6, 2.0, solid("green_light"))  # cheek tufts

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.6, 1.4, 0))
        m.round_box(lb, sx * 1.6, -0.6, 1.0, 1.6, 0.0, 1.4, solid("leg"), cut=0.4)
        ar = m.bone(f"arm_{side}", bd, (sx * 3.8, 9, 0))
        tip = (0.8, 12.6, -4.4) if sx > 0 else (-4.6, 4.2, 1.4)                # one wing over its beak
        rod(m, ar, (sx * 3.8, 9.0, 0.0), tip, 3.0, solid("green"), extend=0.4, t2=1.2)
    return m
