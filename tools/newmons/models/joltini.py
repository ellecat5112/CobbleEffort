"""Joltini, the Cocktail Pokémon (Electric/Fairy), a Liquor Meadows Pokémon (the user's design): a sleek V-shaped
martini-glass sprite filled with shimmering neon-yellow citrus liqueur (its face floats in it), a glowing lightning-bolt
lemon twist on its rim and a glowing olive on a pick for an antenna, on a thin stem and round foot.

Shiny: a blue curaçao cocktail with a lime twist.

Front is -z, y is up. 20 units tall; baseScale 0.45 (0.55 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _liquor import eye_on, glow_of, palette, puff, tiers, translucent
from _route import tone

SHINY = {"neon": (80, 190, 255), "neon_glass": (80, 190, 255, 190), "lemon": (150, 230, 70)}
P, solid, ramp = palette(SHINY)
SCALE = 0.45
HITBOX = [0.9, 1.1]
KIND = "floater"
K = 5
HEIGHT = 20
LOOK = "a V-shaped martini glass full of glowing neon-yellow liqueur with a lightning-bolt lemon twist and an olive antenna"
eyes = eye_on(P, "lemon", [(-1.6, 14.0), (1.6, 14.0)], 0.9)


def liqf(x, y, z, face, variant, **k):
    p = P(variant)
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    if face == "north" and abs(y - 12.4) < 0.3 and abs(x) < 1.0:
        return p["pupil"], None
    c = p["neon"]
    return c, (c if face == "up" else None)


def boltf(x, y, z, face, variant, **k):
    p = P(variant)
    u = x - 5.0
    if abs(u - (0.6 if (y % 2.4) < 1.2 else -0.6) * 1.0) > 0.9:
        return (0, 0, 0, 0), None
    return p["lemon"], p["lemon"]


def build() -> Model:
    m = Model("joltini")
    top = m.bone("joltini", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    tiers(m, bd, [(0.0, 0.6, 3.2), (0.6, 6.0, 0.6)], translucent(P, "glass"))         # foot and stem
    profile = [(6.0 + i * 1.2, 7.2 + i * 1.2, 0.8 + i * 0.75) for i in range(10)]
    tiers(m, bd, profile, translucent(P, "glass"))                                    # the V of the glass
    hd = m.bone("head", bd, (0, 12, 0))
    tiers(m, hd, [(7.2 + i * 1.2, 8.4 + i * 1.2, 0.4 + i * 0.75) for i in range(1, 8)], liqf)   # the liqueur
    m.box(hd, 5.0, 12.6, -0.5, 5.0, 19.0, 0.5, boltf)                                 # the lemon twist bolt
    m.box(hd, 4.2, 12.6, 0.0, 5.8, 19.0, 0.0, boltf)
    rod(m, hd, (-2.0, 13.0, 1.0), (-4.2, 21.0, 0.0), 0.5, solid("silver"), extend=0.2)   # the pick
    puff(m, hd, (-4.2, 21.4, 0.0), 1.1, glow_of(P, "olive"))                          # the glowing olive
    puff(m, hd, (-4.2, 21.4, -0.9), 0.4, glow_of(P, "pimento"))
    return m
