"""Brenkey, the Straw Monkey Pokémon (Water), the water starter of the second A. Fakemon trio, after the art of the A.
Fakemon fanpage (the art's own name): a squat little blue monkey with a big round head, an orange heart-shaped face
with a cream muzzle and a bored, half-lidded stare, a white chest tuft, orange hands and feet, a bamboo straw it blows
water through, and a long dark blue tail curled into a spiral.

Shiny: teal-green with a golden face.

Front is -z, y is up. 19 units tall; baseScale 0.42 (0.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _splashmonkey import P, solid

SCALE = 0.42
HITBOX = [0.8, 1.2]
KIND = "biped"
K = 5
HEIGHT = 19
LOOK = ("a squat little blue monkey with a big round head, an orange heart-shaped face, a bored stare, a white chest "
        "tuft, a bamboo straw and a spiral tail")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.4, y - 14.4
            if abs(dx) < 0.8 and -0.5 < dy < 0.3:
                return (p["blue_dark"] if dy > 0.0 else p["pupil"] if abs(dx) < 0.35 else p["white"]), None
        if y < 12.6 and abs(x) < 2.0:
            return p["cream"], None                                           # cream muzzle
        if any(math.hypot(x - sx * 1.4, y - 14.2) < 2.1 for sx in (-1, 1)) or (y < 13.4 and abs(x) < 2.6):
            return p["orange_light"], None                                    # the heart-shaped face
    return tone(p["blue"], face), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.6 and y > 6.6:
        return p["white"], None
    return tone(p["blue"], face), None


def build() -> Model:
    m = Model("brenkey")
    top = m.bone("brenkey", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.4, 3.4, 2.8, 4.0, 10.6, bodyf, cut=1.2)
    spike(m, bd, (0.4, 9.2, -2.6), (0.4, -1, -0.4), 1.4, 1.8, solid("white"))

    hd = m.bone("head", bd, (0, 10.5, 0))
    m.round_box(hd, 0, 0.0, 4.4, 4.0, 10.0, 18.6, headf, cut=1.6)
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.6, 0.4, 1.0, 1.2, 13.0, 15.6, solid("orange"), cut=0.4)    # ears
    m.box(hd, -1.0, 11.0, -4.6, 1.0, 12.4, -3.8, solid("orange"))             # pursed lips

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.8, 5, 0.4))
        rod(m, lb, (sx * 1.8, 5.0, 0.4), (sx * 2.2, 1.6, -0.4), 1.8, solid("blue_dark"), extend=0.4)
        m.round_box(lb, sx * 2.2, -0.8, 1.2, 1.8, 0.0, 1.6, solid("cream"), cut=0.5)
        ar = m.bone(f"arm_{side}", bd, (sx * 3.4, 9.6, 0))
        hand = (sx * 4.6, 12.6, -1.6) if sx > 0 else (-2.2, 11.0, -4.6)
        rod(m, ar, (sx * 3.4, 9.6, 0.0), hand, 1.6, solid("blue"), extend=0.4)
        m.round_box(ar, hand[0], hand[2], 1.0, 1.0, hand[1] - 0.8, hand[1] + 0.8, solid("orange"), cut=0.4)
    ar = "arm_left"                                                            # the bamboo straw
    rod(m, ar, (-0.6, 11.6, -4.8), (-6.6, 14.2, -6.4), 1.2, solid("bamboo"), extend=0.3)
    m.box(ar, -4.4, 12.4, -6.2, -3.6, 13.6, -5.0, solid("bamboo_dark"))
    for d in ((-0.4, 1, -0.4), (-0.8, 0.6, 0.3)):
        spike(m, ar, (-4.6, 13.2, -5.8), d, 1.0, 2.0, solid("leaf"))

    tl = m.bone("tail", bd, (0, 5, 2.6))
    pts = [(0, 5.0, 2.6), (0, 4.0, 6.0)]
    for i in range(14):                                                        # the curled tail
        a = i * 0.62
        r = 3.4 - i * 0.2
        pts.append((0, 7.0 - r * math.cos(a), 9.6 + r * math.sin(a)))
    for a, b in zip(pts, pts[1:]):
        rod(m, tl, a, b, 1.2, solid("blue_dark"), extend=0.4)
    return m
