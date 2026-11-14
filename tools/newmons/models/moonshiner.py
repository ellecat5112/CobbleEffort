"""Moonshiner, the Moonshine Pokémon (Dark), Bootlegger evolved, a Liquor Meadows Pokémon (the user's design): a
sneaky, upright raccoon bandit in a wide-brimmed hat and a long tan trench coat, its open lining clinking with little
ceramic jugs, a black bandit mask with eyes shining under the brim, and a big ringed tail.

Shiny: a ginger raccoon in a black coat.

Front is -z, y is up. 28 units tall; baseScale 0.7 (1.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _raccoon import P, SHINY, jug, maskface, ramp, ringtail, solid  # noqa: F401
from _route import tone

SCALE = 0.7
HITBOX = [1.0, 1.8]
KIND = "biped"
K = 3
HEIGHT = 28
LOOK = "an upright raccoon bandit in a wide-brimmed hat and trench coat lined with ceramic jugs, with a ringed tail"


def coatf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 1.2:
        return tone(p["coon_light"], face), None                               # the open front shows its belly
    if face == "north" and abs(abs(x) - 1.6) < 0.3:
        return p["coat_dark"], None                                           # lapels
    return tone(p["coat"], face), None


def build() -> Model:
    m = Model("moonshiner")
    top = m.bone("moonshiner", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 3.8, 2.8, 4.0, 19.0, coatf, cut=1.0)                  # the trench coat
    for sx in (-1, 1):
        for y in (8.0, 12.4):
            jug(m, bd, sx * 2.6, y, -2.8, 0.8)                                  # jugs in the open lining
    hd = m.bone("head", bd, (0, 19, 0))
    m.round_box(hd, 0, -0.6, 2.8, 2.6, 19.0, 24.0, maskface(0.0, 22.0), cut=0.9)
    m.round_box(hd, 0, -3.4, 1.0, 0.9, 19.6, 21.0, solid("coon_light"), cut=0.3)
    m.box(hd, -0.5, 20.6, -4.4, 0.5, 21.2, -4.0, solid("black"))
    m.box(hd, -5.0, 24.0, -5.4, 5.0, 24.6, 4.6, solid("hat"))                   # the wide brim
    m.round_box(hd, 0, -0.4, 2.8, 2.8, 24.4, 27.4, solid("hat"), cut=0.9)
    m.round_box(hd, 0, -0.4, 2.9, 2.9, 24.5, 25.2, solid("black"), cut=0.9)     # hat band
    tl = m.bone("tail", bd, (0, 6, 2.6))
    ringtail(m, tl, (0, 6.0, 2.6), (0, 3.0, 10.4), 2.8)
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3.8, 17.6, 0))
        rod(m, ar, (sx * 3.8, 17.6, 0.0), (sx * 5.0, 11.4, -0.8), 1.8, solid("coat"), extend=0.3)
        m.round_box(ar, sx * 5.0, -1.0, 0.8, 0.8, 9.8, 11.4, solid("coon_dark"), cut=0.3)
        lb = m.bone(f"leg_{side}", top, (sx * 1.6, 4, 0))
        rod(m, lb, (sx * 1.6, 4.4, 0.0), (sx * 1.8, 0.8, -0.2), 1.6, solid("coon_dark"), extend=0.3)
        m.box(lb, sx * 1.8 - 1.0, 0.0, -2.0, sx * 1.8 + 1.0, 1.0, 0.6, solid("coon_dark"))
    return m
