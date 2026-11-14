"""Splakey, the Splash Monkey Pokémon (Water), Brenkey evolved, after the art of the A. Fakemon fanpage (the art's own
name): a lean, dripping-wet blue monkey striking a pose with both arms flung up and orange palms open, a dark blue
headband with a white tuft, an orange face with white goggle-rings round its fierce eyes and a pouting muzzle, white
fur tufts at its shoulders and chest, dark blue shorts and orange feet.

Shiny: teal-green with a golden face.

Front is -z, y is up. 31 units tall to its raised hands; baseScale 0.58 (1.1 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _splashmonkey import P, solid

SCALE = 0.58
HITBOX = [1.0, 1.95]
KIND = "biped"
K = 4
HEIGHT = 31
LOOK = ("a lean wet blue monkey with arms flung up, orange palms, a dark headband with a white tuft, an orange face with "
        "white goggle-rings, white fur tufts and dark blue shorts")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.3, y - 23.4)
            if d < 0.55:
                return (p["pupil"] if abs(x - sx * 1.3) < 0.25 else p["white"]), None
            if d < 1.1:
                return p["white"], None                                       # goggle-rings round its eyes
        return tone(p["orange_light"], face), None
    return tone(p["blue_light"], face), None


def build() -> Model:
    m = Model("splakey")
    top = m.bone("splakey", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0.2, 2.8, 2.2, 12.0, 20.0, solid("blue"), cut=1.0)
    m.round_box(bd, 0, 0.2, 3.0, 2.4, 9.6, 13.0, solid("blue_dark"), cut=1.0)   # dark blue shorts
    for d in ((-1, 0.3, -0.5), (1, 0.3, -0.5), (0, -1, -0.6)):                   # white fur tufts
        spike(m, bd, (d[0] * 2.2, 18.6 if d[0] else 17.0, -1.8), d, 1.6, 2.0, solid("white"))

    hd = m.bone("head", bd, (0, 20, 0))
    m.round_box(hd, 0, 0.0, 3.4, 3.0, 20.0, 26.2, headf, cut=1.2)
    m.box(hd, -1.2, 20.4, -4.0, 1.2, 22.4, -2.8, solid("orange"))              # pouting muzzle
    m.round_box(hd, 0, 0.2, 3.6, 3.2, 24.8, 26.6, solid("blue_dark"), cut=1.2)  # the headband
    for d in ((0, 1, 0.3), (-0.4, 1, 0.6), (0.4, 1, 0.6)):
        spike(m, hd, (d[0] * 2, 26.4, 0.4), d, 1.4, 2.2, solid("white"))
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.6, 0.2, 0.9, 1.3, 22.0, 24.6, solid("white"), cut=0.4)    # ears

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.6, 11, 0.2))
        rod(m, lb, (sx * 1.6, 11.0, 0.2), (sx * 2.6, 6.0, -1.6), 2.2, solid("blue_dark"), extend=0.5)
        rod(m, lb, (sx * 2.6, 6.0, -1.6), (sx * 2.4, 1.2, 0.2), 1.8, solid("blue_light"), extend=0.5)
        m.round_box(lb, sx * 2.4, -0.8, 1.3, 2.0, 0.0, 1.6, solid("orange"), cut=0.5)
        ar = m.bone(f"arm_{side}", bd, (sx * 3.0, 19, 0))                        # arms flung up
        rod(m, ar, (sx * 3.0, 19.0, 0.0), (sx * 6.6, 24.0, -0.4), 1.8, solid("blue_light"), extend=0.5)
        rod(m, ar, (sx * 6.6, 24.0, -0.4), (sx * 8.2, 28.4, -0.8), 1.6, solid("white"), extend=0.5)
        x0, x1 = sorted((sx * 7.0, sx * 9.6))
        m.box(ar, x0, 28.0, -1.4, x1, 31.4, -0.4, solid("orange"))             # open orange palms
        spike(m, ar, (sx * 5.4, 22.0, 0.6), (sx * 0.2, -1, 0.2), 1.0, 1.8, solid("white"))   # drips
    return m
