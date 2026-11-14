"""Chawchamp, the Chewer Pokémon (Fighting), the Nicodex's Fighting type (the user's design): a squat, burly bullfrog
brawler with one cheek always swollen with a wad of chaw, a spittoon-brass championship belt, taped fists and a
battered cowboy-brown hide.

Shiny: a sandy hide with a silver belt.

Front is -z, y is up. 20 units tall; baseScale 0.6 (0.75 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _nico import eye_on, palette
from _route import tone

SHINY = {"olive": (210, 176, 110), "olive_dark": (170, 136, 80), "brass": (206, 208, 220), "gold_dark": (150, 150, 168)}
P, solid, ramp = palette(SHINY)
SCALE = 0.6
HITBOX = [1.1, 1.25]
KIND = "biped"
K = 4
HEIGHT = 20
LOOK = "a squat bullfrog brawler with one swollen cheek full of chaw, a brass championship belt and taped fists"
eyes = eye_on(P, "amber", [(-2.4, 16.6), (2.4, 16.6)], 1.1, face="up")


def hidef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y < 10.6:
        return tone(p["tan"], face), None                                     # pale belly
    if face == "up" and ((x * 3 + z * 2) % 5) < 0.8:
        return tone(p["olive_dark"], face), None                              # warts
    return tone(p["olive"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(y - 13.4) < 0.4 and abs(x) < 3.2:
        return p["tobacco_dark"], None                                        # a wide frog mouth
    return tone(p["olive"], face), None


def eyef(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "up"):
        dx, dy = x - (2.4 if x > 0 else -2.4), y - 16.6
        if dx * dx + dy * dy < 0.36:
            return p["pupil"], None
        return p["amber"], None
    return tone(p["olive"], face), None


def beltf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.8:
        return p["gold"], None                                                # the buckle
    return tone(p["brass"], face), None


def build() -> Model:
    m = Model("chawchamp")
    top = m.bone("chawchamp", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0, 5.2, 4.4, 4.0, 12.2, hidef, cut=1.6)
    m.round_box(bd, 0, 0, 5.4, 4.6, 6.4, 8.0, beltf, cut=1.6)                   # championship belt
    hd = m.bone("head", bd, (0, 12, 0))
    m.round_box(hd, 0, -0.6, 4.6, 3.8, 12.0, 16.4, headf, cut=1.4)
    m.round_box(hd, 3.8, -1.6, 1.8, 1.8, 12.4, 15.4, solid("olive"), cut=0.6)   # the swollen cheek
    for sx in (-1, 1):
        m.box(hd, sx * 2.4 - 1.2, 15.6, -2.2, sx * 2.4 + 1.2, 17.8, 0.2, eyef)   # bulging eyes on top
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 5, 11, 0))
        rod(m, ar, (sx * 5.0, 11.0, 0.0), (sx * 6.6, 7.0, -2.4), 2.2, solid("olive"), extend=0.4)
        m.round_box(ar, sx * 6.8, -3.2, 1.8, 1.8, 4.4, 7.6, solid("white"), cut=0.6)   # taped fists
        lb = m.bone(f"leg_{side}", top, (sx * 3, 5, 0))
        rod(m, lb, (sx * 3.0, 5.4, 0.6), (sx * 4.2, 0.6, -0.2), 2.6, solid("olive"), extend=0.4)
        m.box(lb, sx * 4.2 - 1.8, 0.0, -3.4, sx * 4.2 + 1.8, 1.0, 1.0, solid("olive_dark"))   # webbed feet
    return m
