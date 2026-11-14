"""Absinthia, the Green Fairy Pokémon (Poison/Psychic), a Liquor Meadows Pokémon (the user's design): an eerie,
slender emerald-green fairy wrapped in swirling, cloudy louche mist, with long translucent green wings, glowing emerald
eyes, a flowing wisp of a skirt and a slotted silver absinthe spoon (with a sugar cube) held like a wand.

Shiny: a violet fairy.

Front is -z, y is up. 22 units tall; baseScale 0.5 (0.75 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _liquor import palette, puff, translucent
from _route import tone

SHINY = {"emerald": (150, 90, 210), "emerald_dark": (100, 50, 160), "emerald_light": (200, 150, 240),
         "louche": (220, 196, 240, 120)}
P, solid, ramp = palette(SHINY)
SCALE = 0.5
HITBOX = [0.8, 1.2]
KIND = "floater"
K = 4
HEIGHT = 22
LOOK = "a slender emerald-green fairy wrapped in cloudy louche mist with green wings, glowing eyes and a slotted silver spoon wand"
CUT = (0, 0, 0, 0)


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.1) < 0.55 and abs(y - 17.4) < 0.45:
                return p["emerald_light"], p["emerald_light"]                 # swirling emerald eyes
    return tone(p["emerald"], face), None


def wingf(x, y, z, face, variant, **k):
    p = P(variant)
    ax = abs(x)
    if y > 20.0 - (ax - 2.0) * 0.3 or y < 9.0 + (ax - 2.0) * 0.5:
        return CUT, None
    return p["emerald_light"][:3] + (130,), None


def spoonf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south") and y > 15.4 and abs((x - 6.6) % 0.9 - 0.45) < 0.18:
        return CUT, None                                                      # the spoon's slots
    return p["silver"], None


def build() -> Model:
    m = Model("absinthia")
    top = m.bone("absinthia", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 1.6, 1.2, 9.0, 15.0, solid("emerald"), cut=0.5)       # slender body
    for y0, r in ((3.0, 2.6), (5.0, 2.2), (7.0, 1.8)):                         # a wisp of a skirt
        m.round_box(bd, 0, 0, r, r, y0, y0 + 2.2, translucent(P, "louche"), cut=0.8)
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, 0, 2.2, 2.0, 15.0, 19.6, headf, cut=0.7)
    for c, r in (((0, 20.4, 0.6), 1.6), ((-1.6, 19.6, 1.2), 1.2), ((1.6, 19.8, 1.0), 1.2)):
        puff(m, hd, c, r, solid("emerald_dark"))                               # swept hair
    for c, r in (((-3.6, 12.0, 1.0), 1.6), ((3.4, 9.0, -0.8), 1.4), ((-2.4, 6.0, -1.2), 1.4), ((2.8, 15.4, 1.6), 1.2)):
        puff(m, bd, c, r, translucent(P, "louche"))                            # swirling louche mist
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 1.2, 14, 1.2))
        x0, x1 = sorted((sx * 1.2, sx * 9.0))
        m.box(w, x0, 8.0, 1.2, x1, 21.0, 1.2, wingf, rotation=(0, sx * 18, 0), pivot=(sx * 1.2, 14.0, 1.2))
    ar = m.bone("arm_right", bd, (1.6, 14, 0))
    rod(m, ar, (1.6, 14.0, 0.0), (5.0, 12.0, -1.6), 0.9, solid("emerald"), extend=0.3)
    rod(m, ar, (5.2, 11.0, -1.8), (6.6, 15.0, -1.8), 0.6, solid("silver"), extend=0.2)   # the spoon's handle
    m.box(ar, 5.6, 15.0, -1.8, 7.6, 17.4, -1.8, spoonf)                        # its slotted bowl
    m.box(ar, 6.0, 17.4, -2.4, 7.2, 18.6, -1.2, solid("white"))                # a sugar cube
    al = m.bone("arm_left", bd, (-1.6, 14, 0))
    rod(m, al, (-1.6, 14.0, 0.0), (-4.0, 11.0, -0.6), 0.9, solid("emerald"), extend=0.3)
    return m
