"""Shared parts for Stumblepup and Tavern Hound (the user's design): Saint Bernard-style dogs, white with chestnut
patches, rosy cheeks, droopy ears, a wooden keg on the collar and a wagging tail. `dog(m, s)` builds one at scale s.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _liquor import palette, puff
from _route import tone

SHINY = {"bernard": (60, 60, 66), "bernard_dark": (36, 36, 40), "oak": (200, 160, 70), "oak_dark": (150, 110, 40)}
P, solid, ramp = palette(SHINY)


def furf(x, y, z, face, variant, **k):
    p = P(variant)
    if face != "down" and (math.sin(x * 0.9 + 1.0) + math.cos(z * 0.6 + y * 0.3)) > 0.9:
        return tone(p["bernard"], face), None                                 # chestnut patches
    return tone(p["white"], face), None


def headf_of(s, adult):
    def headf(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if abs(x - sx * 1.5 * s) < 0.5 * s and abs(y - 9.6 * s) < (0.25 if adult else 0.55) * s:
                    return p["pupil"], None                                   # eyes (droopier on the adult)
                if abs(x - sx * 2.3 * s) < 0.6 * s and abs(y - 8.4 * s) < 0.4 * s:
                    return p["rosy"], None                                    # rosy cheeks
            if abs(x) > 0.6 * s and abs(y - 10.4 * s) < 1.2 * s:
                return tone(p["bernard"], face), None                         # mask round the eyes
        return tone(p["white"], face), None
    return headf


def kegf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and (abs(x) > 0.0) and False:
        return p["iron"], None
    return tone(p["oak"], face), None


def dog(m: Model, s: float, adult: bool):
    top = m.bone(m.name, None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6 * s, 0))
    m.round_box(bd, 0, 0.6 * s, 3.0 * s, 5.4 * s, 4.2 * s, 9.6 * s, furf, cut=max(0.6, s))
    hd = m.bone("head", bd, (0, 9 * s, -5 * s))
    m.round_box(hd, 0, -6.4 * s, 2.8 * s, 2.6 * s, 7.0 * s, 12.2 * s, headf_of(s, adult), cut=max(0.5, 0.9 * s))
    m.round_box(hd, 0, -9.2 * s, 1.6 * s, 1.2 * s, 7.0 * s, 9.4 * s, solid("white"), cut=max(0.4, 0.5 * s))   # muzzle
    m.box(hd, -0.6 * s, 8.6 * s, -10.6 * s, 0.6 * s, 9.4 * s, -10.2 * s, solid("pupil"))                    # nose
    if adult:
        for sx in (-1, 1):
            m.round_box(hd, sx * 1.0 * s, -9.0 * s, 0.9 * s, 0.9 * s, 6.2 * s, 7.6 * s, solid("white"), cut=0.4)  # jowls
    for sx in (-1, 1):
        m.box(hd, sx * 2.8 * s - (0.7 * s if sx > 0 else 0), 7.4 * s, -7.4 * s, sx * 2.8 * s + (0.7 * s if sx < 0 else 0),
              11.4 * s, -5.0 * s, solid("bernard_dark"))                                                          # droopy ears
    m.box(bd, -2.2 * s, 8.0 * s, -5.2 * s, 2.2 * s, 9.0 * s, -4.2 * s, solid("red"))                          # collar
    kr = 1.5 * s if not adult else 2.0 * s
    kz = -5.6 * s
    m.box(bd, -kr * 1.2, 5.0 * s, kz - kr, kr * 1.2, 5.0 * s + kr * 2, kz + kr * 0.6, kegf)                    # the keg
    for dx in (-kr * 0.6, kr * 0.6):
        m.box(bd, dx - 0.3 * s, 5.0 * s - 0.05, kz - kr - 0.05, dx + 0.3 * s, 5.0 * s + kr * 2 + 0.05, kz + kr * 0.6 + 0.05,
              solid("iron"))                                                                                  # its hoops
    tl = m.bone("tail", bd, (0, 8.4 * s, 5.4 * s))
    rod(m, tl, (0, 8.4 * s, 5.2 * s), (0, 11.0 * s, 8.4 * s), 1.2 * s, furf, extend=0.3)
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -3.4 * s), ("back", 3.6 * s)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 1.8 * s, 4.6 * s, z))
            m.round_box(lb, sx * 1.8 * s, z, 0.9 * s, 1.0 * s, 0.0, 5.0 * s, solid("white"), cut=max(0.3, 0.3 * s))
    return m
