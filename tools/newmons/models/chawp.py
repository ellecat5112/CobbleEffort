"""Chawp, the Scrappy Pokémon (Fighting), after @magikdex's Cornera region art (name kept): the pre-evolution of
Sawk, Throh and Kiq. A little scrapper with a huge round quilted head: big determined grey eyes under scowling brows, a
white angular plate across its brow and a bandage on its cheek; a small body in grey shorts like a barrel with black
cuffs (a black chevron on the front), thin legs bent in a fighting stance and stubby mitten fists raised.

Shiny: black shorts with a white chevron and cuffs, greener skin.

Front is -z, y is up. 20 units tall; baseScale 0.48 (0.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _gi import eye_disc, in_tri, near_seg, palette, seamed
from _route import tone

SHINY = {"skin": (178, 210, 196), "skin_shade": (140, 176, 162), "seam": (110, 146, 134),
         "shorts": (46, 46, 52), "black": (238, 238, 232)}
P, solid, ramp = palette(SHINY)
SCALE = 0.48
HITBOX = [0.8, 1.25]
KIND = "biped"
K = 5
HEIGHT = 20
LOOK = ("a little scrapper with a huge round head, big determined eyes, a white plate on its brow, a cheek bandage, "
        "grey barrel shorts with black cuffs and raised mitten fists")

HY = 14.0                                     # the head's centre height


def face(x, y, z, f, p):
    """The front of the head: eyes, brows, the white brow plate, the cheek bandage, a small gritted mouth."""
    if f != "north":
        if f == "up" and abs(x - 0.4) < 0.22:
            return p["seam"]                                              # a seam over the top of the head
        return None
    for sx in (-1, 1):
        e = eye_disc(p, x, y, sx * 2.0, HY + 0.1, 1.45, "eye", ry=1.75)
        if e is not None:
            return e
        if near_seg(x, y, (sx * 0.7, HY + 1.6), (sx * 3.4, HY + 2.6), 0.42):
            return p["mask"]                                              # scowling brows
    if in_tri(x, y, (-1.4, HY + 5.6), (1.2, HY + 5.6), (3.1, HY + 1.5)):
        return p["plate"]                                                 # the white angular brow plate
    if 2.2 < x < 4.3 and HY - 3.4 < y - 0.25 * (x - 3) < HY - 2.2:      # the cheek bandage
        if math.hypot(x - 2.9, y - (HY - 2.7)) < 0.22 or math.hypot(x - 3.6, y - (HY - 2.6)) < 0.22:
            return p["seam"]
        return p["plate"]
    if -0.6 < x < 0.8 and HY - 3.9 < y < HY - 3.1:                      # a small gritted mouth, one tooth showing
        return p["white"] if 0.0 < x < 0.4 and y > HY - 3.5 else p["mouth"]
    return None


def shorts(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and (near_seg(x, y, (0, 7.3), (-1.7, 4.0), 0.42) or near_seg(x, y, (0, 7.3), (1.7, 4.0), 0.42)):
        return tone(p["black"], face), None                                   # the chevron
    return tone(p["shorts"], face), None


def build() -> Model:
    m = Model("chawp")
    top = m.bone("chawp", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    # grey barrel shorts with black cuffs (round in cross-section)
    for (y0, y1, z0, z1) in ((3.5, 7.5, -2, 2), (3, 8, -1.5, 1.5), (4, 7, -2.5, 2.5)):
        m.box(bd, -4, y0, z0, 4, y1, z1, shorts)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 4, sx * 5.4))
        for (y0, y1, z0, z1) in ((3.2, 7.8, -2.2, 2.2), (2.8, 8.2, -1.6, 1.6), (3.8, 7.2, -2.8, 2.8)):
            m.box(bd, x0, y0, z0, x1, y1, z1, solid("black"))
    m.round_box(bd, 0, 0, 2.6, 2.0, 7.5, 10, seamed(P, "skin", [("x", 0)]), cut=0.8)     # a small body
    hd = m.bone("head", bd, (0, 9.5, 0))
    hs = seamed(P, "skin", [("y", HY + 3.4)], extra=face)
    for y0, y1, r in ((HY - 6.0, HY - 5.0, 3.6), (HY - 5.0, HY - 3.6, 4.8), (HY - 3.6, HY + 3.6, 5.6),
                      (HY + 3.6, HY + 5.0, 4.8), (HY + 5.0, HY + 6.0, 3.6)):           # the huge round head
        m.round_box(hd, 0, 0, r, r * 0.94, y0, y1, hs, cut=round(r * 0.36, 1))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # stubby arms, mitten fists up
        a = m.bone(nm, bd, (sx * 2.4, 9.3, 0))
        rod(m, a, (sx * 2.4, 9.3, 0), (sx * 4.6, 8.0, -1.4), 1.6, solid("skin"))
        rod(m, a, (sx * 4.6, 8.0, -1.4), (sx * 4.4, 10.2, -3.6), 1.6, solid("skin"))
        m.round_box(a, sx * 4.4, -4.2, 1.5, 1.3, 9.6, 12.4, seamed(P, "skin", [("y", 11.2)]), cut=0.6)
        m.box(a, sx * 4.4 - (1.9 if sx > 0 else -0.9), 10.2, -4.6, sx * 4.4 - (0.9 if sx > 0 else -1.9), 11.2, -3.6,
              solid("skin"))                                                         # thumbs
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # thin legs out of the cuffs
        lg = m.bone(nm, top, (sx * 5.2, 5.5, 0))
        rod(m, lg, (sx * 5.2, 5.5, 0), (sx * 6.8, 5.0, -0.2), 1.4, solid("skin"))
        rod(m, lg, (sx * 6.8, 5.0, -0.2), (sx * 6.4, 1.4, -0.6), 1.4, solid("skin"))
        m.round_box(lg, sx * 6.4, -1.0, 1.4, 2.0, 0, 1.6, seamed(P, "skin", [("z", -1.6)]), cut=0.6)
    return m
