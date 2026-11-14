"""Sommelgeist, the Connoisseur Pokémon (Psychic/Ghost), a Liquor Meadows Pokémon (the user's design): a floating,
spectral wine connoisseur: a pale ghostly head with a thin moustache and glowing eyes, a tattered black tuxedo with a
white shirt front and burgundy bow tie, white gloves, a swirling cape of deep burgundy wine, a ghostly wisp instead of
legs, and the faint outline of the goblet it swirls by telekinesis.

Shiny: a white tuxedo with a golden-wine cape.

Front is -z, y is up. 28 units tall; baseScale 0.7 (1.4 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _liquor import palette, puff, tiers, translucent
from _route import tone

SHINY = {"tux": (232, 230, 226), "burgundy": (200, 150, 50), "burgundy_glass": (220, 170, 60, 170)}
P, solid, ramp = palette(SHINY)
SCALE = 0.7
HITBOX = [1.0, 1.8]
KIND = "floater"
K = 3
HEIGHT = 28
LOOK = "a spectral connoisseur in a tattered tuxedo and burgundy bow tie with a swirling wine cape and a ghostly wisp tail"
CUT = (0, 0, 0, 0)


def tuxf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.2 and y > 12.0:
        return p["white"], None                                               # shirt front
    if face == "north" and abs(x) < 0.3 and 12.0 < y < 16.0 and int(y * 2) % 3 == 0:
        return p["black"], None                                               # studs
    if y < 11.0 and (int(x * 3 + z * 2) % 3 == 0):
        return CUT, None                                                      # tattered hem
    return tone(p["tux"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.55 and abs(y - 22.6) < 0.4:
                return p["violet"], p["violet"]
            if 0.3 < abs(x) < 1.8 and abs(y - 20.8 - 0.25 * abs(x)) < 0.22:
                return p["black"], None                                       # a thin moustache
    return p["ghost_glass"], None


def capef(x, y, z, face, variant, **k):
    p = P(variant)
    if y < 6.0 + 2.0 * abs(((x * 0.7) % 2.0) - 1.0):
        return CUT, None
    return p["burgundy_glass"], None


def build() -> Model:
    m = Model("sommelgeist")
    top = m.bone("sommelgeist", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 3.2, 2.2, 9.0, 18.6, tuxf, cut=0.8)                   # the tattered tuxedo
    m.box(bd, -1.4, 17.4, -2.6, 1.4, 18.6, -2.0, solid("burgundy"))             # bow tie
    tl = m.bone("tail", bd, (0, 9, 0))
    chain(m, tl, [(0, 9.0, 0.4), (0.8, 6.0, 1.4), (-0.6, 3.6, 2.4), (0.6, 1.6, 3.6)], [3.0, 2.2, 1.4],
          translucent(P, "ghost_glass"))                                        # ghostly wisp
    hd = m.bone("head", bd, (0, 19, 0))
    m.round_box(hd, 0, 0, 2.4, 2.2, 18.6, 24.6, headf, cut=0.8)
    cp = m.bone("cape", bd, (0, 18, 2.4))
    m.box(cp, -5.0, 4.0, 2.4, 5.0, 18.6, 2.4, capef, rotation=(-12, 0, 0), pivot=(0.0, 18.6, 2.4))   # wine cape
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3.2, 17, 0))
        rod(m, ar, (sx * 3.2, 17.0, 0.0), (sx * 5.4, 13.0, -2.2), 1.4, solid("tux"), extend=0.3)
        puff(m, ar, (sx * 5.6, 12.4, -2.6), 0.9, solid("white"))                # white gloves
    gb = m.bone("goblet", bd, (5.6, 14, -4))
    tiers(m, gb, [(13.0, 13.4, 1.0), (13.4, 15.0, 0.3), (15.0, 15.8, 1.0), (15.8, 17.6, 1.4)],
          translucent(P, "crystal"), cx=5.6, cz=-4.4)                           # the invisible goblet, faintly
    tiers(m, gb, [(15.4, 16.4, 0.9)], translucent(P, "burgundy_glass"), cx=5.6, cz=-4.4)
    return m
