"""Nicodrake, the Alkaloid Pokémon (Dragon/Poison), the Nicodex's Dragon type and its legendary (the user's design):
a majestic, serpentine dragon formed from swirling, iridescent tobacco smoke, its long body wreathed in drifting
vapour, with golden ash scales, two swept golden horns, glowing amber eyes, a mane of tobacco leaves and smoky fins.

Shiny: a deep violet body with silver ash.

Front is -z, y is up. ~40 units tall; baseScale 1.0 (2.6 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _nico import palette, puff, translucent
from _route import tone

SHINY = {"teal": (110, 70, 170), "teal_dark": (70, 40, 120), "gold": (216, 218, 230), "gold_dark": (160, 160, 176),
         "teal_mist": (170, 120, 230, 140)}
P, solid, ramp = palette(SHINY)
SCALE = 1.0
HITBOX = [2.2, 2.6]
KIND = "floater"
K = 3
HEIGHT = 40
LOOK = ("a majestic serpentine dragon of swirling iridescent smoke with golden ash scales, golden horns, glowing amber "
        "eyes and a tobacco-leaf mane")


def scalef(x, y, z, face, variant, **k):
    """Iridescent smoke: teal shifting toward violet along the body, with golden ash scales on top."""
    p = P(variant)
    t = 0.5 + 0.5 * math.sin(z * 0.22 + y * 0.15)
    c = tuple(int(a + (b - a) * t) for a, b in zip(p["teal"], p["purple"]))
    if face == "up" and (int(x * 1.3 + z * 1.3) % 3 == 0):
        return tone(p["gold"], face), None
    if face == "down":
        return p["gold_dark"], None
    return tone(c, face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 33.6) < 0.6 and -17.0 < z < -15.0:
        return p["amber"], p["amber"]
    return scalef(x, y, z, face, variant)


def build() -> Model:
    m = Model("nicodrake")
    top = m.bone("nicodrake", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    body = [(0, 26.0, -8.0), (0, 20.0, -2.0), (3.0, 16.0, 5.0), (0, 13.0, 12.0)]
    chain(m, bd, body, [5.0, 5.0, 4.6], scalef)
    tl = m.bone("tail", bd, (0, 13, 12))
    chain(m, tl, [(0, 13.0, 12.0), (-4.0, 11.0, 18.0), (-2.0, 8.0, 24.0), (2.0, 7.0, 28.0)], [4.0, 3.0, 2.2], scalef)
    for c, r in (((-2.0, 5.6, 30.0), 2.2), ((3.0, 9.0, 21.0), 2.6), ((-4.0, 15.0, 8.0), 3.0), ((4.0, 21.0, 0.0), 2.6)):
        puff(m, bd, c, r, translucent(P, "teal_mist"))                          # drifting vapour
    hd = m.bone("head", bd, (0, 28, -9))
    chain(m, hd, [(0, 26.0, -8.0), (0, 31.0, -12.0)], [4.4], scalef)            # upper neck
    m.box(hd, -3.0, 30.4, -18.0, 3.0, 36.0, -11.4, headf)                       # head
    m.box(hd, -2.2, 29.6, -23.0, 2.2, 33.0, -17.6, scalef)                      # snout
    hd2 = m.bone("jaw", hd, (0, 30, -18))
    m.box(hd2, -2.0, 28.2, -22.4, 2.0, 29.6, -17.6, solid("gold_dark"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 35.8, -12.6), (sx * 0.35, 0.7, 1), 1.6, 6.0, solid("gold"), tip=0.8)   # swept horns
        spike(m, hd, (sx * 2.2, 31.0, -21.6), (sx * 1, -0.2, -0.4), 0.6, 4.4, solid("gold"))           # whiskers
        for i, y in enumerate((34.0, 32.0, 30.0)):                                                  # leaf mane
            spike(m, hd, (sx * 3.0, y, -11.0), (sx * 1, 0.3, 0.8), 1.6, 4.0 - i * 0.6, solid("tobacco_light"))
    for sx, side in ((-1, "left"), (1, "right")):                               # smoky fins
        fn = m.bone(f"arm_{side}", bd, (sx * 2.4, 21, -3))
        x0, x1 = sorted((sx * 2.4, sx * 11.0))
        m.box(fn, x0, 15.0, -3.0, x1, 23.0, -3.0, translucent(P, "teal_mist"),
              rotation=(0, sx * 25, 0), pivot=(sx * 2.4, 21.0, -3.0))
    return m
