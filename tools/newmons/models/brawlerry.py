"""Brawlerry, the Brawler Pokémon (Fighting), a Liquor Meadows Pokémon (the user's design): a rowdy, barrel-chested
bear brawler: brown fur, a broad chest banded like a barrel with iron hoops, frothy white beer foam piled on its
shoulders and head, rosy cheeks, and heavy wooden-stave gauntlets bound with iron on its forearms.

Shiny: a stout-black bear with cream foam.

Front is -z, y is up. 28 units tall; baseScale 0.75 (1.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _liquor import palette, puff
from _route import tone

SHINY = {"fur": (54, 40, 34), "fur_dark": (34, 24, 20), "fur_light": (96, 72, 58), "foam": (236, 212, 160),
         "foam_shade": (206, 180, 130)}
P, solid, ramp = palette(SHINY)
SCALE = 0.75
HITBOX = [1.4, 1.85]
KIND = "biped"
K = 3
HEIGHT = 28
LOOK = "a rowdy bear brawler with a barrel-hooped chest, frothy foam on its shoulders and wooden-stave gauntlets"


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if abs(y - 10.4) < 0.5 or abs(y - 16.0) < 0.5:
            return p["iron"], None                                            # barrel hoops
        return tone(p["oak_light"] if int(x + 10) % 2 else p["oak"], face), None   # staves
    return tone(p["fur"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.6) < 0.5 and abs(y - 22.2) < 0.5:
                return p["pupil"], None
            if abs(x - sx * 2.4) < 0.7 and abs(y - 20.6) < 0.4:
                return p["rosy"], None
    return tone(p["fur"], face), None


def gauntletf(x, y, z, face, variant, **k):
    p = P(variant)
    if abs((y % 3.0) - 1.5) < 0.3:
        return p["iron"], None
    return tone(p["oak"], face), None


def build() -> Model:
    m = Model("brawlerry")
    top = m.bone("brawlerry", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0, 5.4, 4.0, 8.0, 18.4, chestf, cut=1.6)                 # the barrel chest
    m.round_box(bd, 0, 0, 4.6, 3.6, 6.4, 8.4, solid("fur_dark"), cut=1.2)
    for sx in (-1, 1):
        for c, r in (((sx * 4.4, 18.4, 0.0), 2.0), ((sx * 2.6, 19.4, 1.0), 1.4)):
            puff(m, bd, c, r, solid("foam"))                                     # frothy foam shoulders
    hd = m.bone("head", bd, (0, 18, -0.5))
    m.round_box(hd, 0, -0.6, 3.4, 3.0, 18.6, 24.4, headf, cut=1.0)
    m.round_box(hd, 0, -3.6, 1.6, 1.0, 19.2, 21.2, solid("fur_light"), cut=0.5) # muzzle
    m.box(hd, -0.6, 20.6, -4.8, 0.6, 21.4, -4.4, solid("pupil"))
    for sx in (-1, 1):
        m.round_box(hd, sx * 2.6, -0.4, 1.0, 0.7, 24.0, 25.6, solid("fur"), cut=0.4)   # ears
    puff(m, hd, (0.4, 25.0, 0.4), 1.6, solid("foam"))                           # a dollop of foam on its head
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 5.4, 17, 0))
        rod(m, ar, (sx * 5.4, 17.0, 0.0), (sx * 7.0, 12.4, -0.6), 3.0, solid("fur"), extend=0.4)
        m.round_box(ar, sx * 7.4, -1.0, 2.2, 2.2, 6.4, 12.6, gauntletf, cut=0.8) # stave gauntlets
        m.round_box(ar, sx * 7.4, -1.4, 1.6, 1.6, 5.0, 6.6, solid("fur_dark"), cut=0.5)
        lb = m.bone(f"leg_{side}", top, (sx * 2.6, 8, 0))
        m.round_box(lb, sx * 2.8, 0.0, 2.0, 2.2, 0.0, 8.6, solid("fur_dark"), cut=0.8)
    return m
