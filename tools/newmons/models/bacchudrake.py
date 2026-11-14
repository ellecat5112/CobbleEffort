"""Bacchudrake, the Revelry Pokémon (Dragon/Fairy), the Liquor Meadows' legendary (the user's design): a festive,
serpentine dragon of rose-gold scales, its long body draped in lush bunches of purple grapes and golden ivy leaves,
flowing ribbons of sparkling rosé trailing from its back, a mane of vine tendrils, golden horns and a joyous face.

Shiny: green grapes on a champagne-gold body.

Front is -z, y is up. ~40 units tall; baseScale 1.0 (2.8 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _liquor import palette, puff, translucent
from _route import tone

SHINY = {"rose_solid": (236, 214, 150), "grape": (150, 200, 80), "grape_dark": (100, 150, 50), "grape_light": (196, 236, 130),
         "rose": (250, 230, 160, 140)}
P, solid, ramp = palette(SHINY)
SCALE = 1.0
HITBOX = [2.2, 2.6]
KIND = "floater"
K = 3
HEIGHT = 40
LOOK = ("a festive serpentine rose-gold dragon draped in purple grape bunches and golden ivy, trailing ribbons of "
        "sparkling rosé")


def scalef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return p["cream"], None
    if face == "up" and (int(x * 1.3 + z * 1.3) % 4 == 0):
        return tone(p["gold"], face), None
    return tone(p["rose_solid"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 33.4) < 0.6 and -17.2 < z < -15.2:
        return p["grape_light"], p["grape_light"]                             # bright, joyous eyes
    return scalef(x, y, z, face, variant)


def ribbonf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["rose"]
    sparkle = (int(x * 3 + y * 5 + z * 7) % 11 == 0)
    return (c, (255, 240, 250)) if sparkle else (c, None)


def grapes(m, bone, c, s=1.0):
    for dy, dx, dz in ((0, 0, 0), (-0.9, 0.55, 0), (-0.9, -0.55, 0), (-1.8, 0, 0), (-0.45, 0, 0.6), (-1.3, 0.3, 0.5)):
        puff(m, bone, (c[0] + dx * s, c[1] + dy * s, c[2] + dz * s), 0.65 * s, solid("grape" if dy > -1 else "grape_dark"))
    spike(m, bone, (c[0], c[1] + 0.4 * s, c[2]), (0.4, 1, 0), 0.4 * s, 1.2 * s, solid("green"))


def build() -> Model:
    m = Model("bacchudrake")
    top = m.bone("bacchudrake", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    body = [(0, 26.0, -8.0), (0, 20.0, -2.0), (-3.0, 16.0, 5.0), (0, 13.0, 12.0)]
    chain(m, bd, body, [5.0, 5.0, 4.6], scalef)
    tl = m.bone("tail", bd, (0, 13, 12))
    chain(m, tl, [(0, 13.0, 12.0), (4.0, 11.0, 18.0), (2.0, 8.0, 24.0), (-2.0, 7.0, 28.0)], [4.0, 3.0, 2.2], scalef)
    for c in ((2.6, 22.0, -4.0), (-3.6, 18.4, 3.0), (2.4, 14.6, 9.0), (4.2, 11.8, 17.0)):
        grapes(m, bd, c, 1.2)                                                   # bunches of grapes draped on it
    for i, (a, b) in enumerate((((0, 23.0, -4.0), (5.0, 26.0, 4.0)), ((0, 18.0, 2.0), (-5.0, 21.0, 10.0)),
                                ((0, 15.0, 8.0), (6.0, 17.0, 16.0)))):
        rp = m.bone(f"ribbon_{i}", bd, a)
        rod(m, rp, a, b, 2.4, ribbonf, extend=0.6, t2=0.0)                       # ribbons of sparkling rosé
    for z in (-6.0, -1.0, 4.0, 9.0):
        spike(m, bd, (0, 24.0 - (z + 6) * 0.5, z), (0.4, 1, 0.3), 1.6, 1.6, solid("ivy"))   # golden ivy leaves
    hd = m.bone("head", bd, (0, 28, -9))
    chain(m, hd, [(0, 26.0, -8.0), (0, 31.0, -12.0)], [4.4], scalef)
    m.box(hd, -3.0, 30.4, -18.0, 3.0, 36.0, -11.4, headf)
    m.box(hd, -2.2, 29.6, -23.0, 2.2, 33.0, -17.6, scalef)
    jw = m.bone("jaw", hd, (0, 30, -18))
    m.box(jw, -2.0, 28.2, -22.4, 2.0, 29.6, -17.6, solid("cream"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 35.8, -12.6), (sx * 0.35, 0.7, 1), 1.6, 6.0, solid("gold"), tip=0.8)          # golden horns
        for i, y in enumerate((34.0, 32.0)):
            chain(m, hd, [(sx * 3.0, y, -11.0), (sx * 5.0, y + 1.0, -9.6), (sx * 5.8, y - 0.6, -8.0)], [0.7, 0.6],
                  solid("green"))                                               # a mane of vine tendrils
        grapes(m, hd, (sx * 3.6, 30.4, -12.4), 0.9)
    for sx, side in ((-1, "left"), (1, "right")):
        fn = m.bone(f"arm_{side}", bd, (sx * 2.4, 21, -3))
        x0, x1 = sorted((sx * 2.4, sx * 10.0))
        m.box(fn, x0, 16.0, -3.0, x1, 23.0, -3.0, translucent(P, "rose"), rotation=(0, sx * 25, 0),
              pivot=(sx * 2.4, 21.0, -3.0))                                    # rosé fins
    return m
