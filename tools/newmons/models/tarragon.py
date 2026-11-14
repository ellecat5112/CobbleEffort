"""Tarragon, the Resin Wyvern Pokémon (Poison/Dragon), the Nicodex's Poison type (the user's design): a sticky black
tar wyvern whose glossy hide is always dripping. Its wings are thin sheets of stretched tar with drips along the
trailing edge, its eyes glow amber like burning resin, and a long dripping tail drags behind it.

Shiny: amber resin with dark eyes.

Front is -z, y is up. 30 units tall; baseScale 0.8 (1.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _nico import palette
from _route import tone

SHINY = {"tar": (170, 100, 30), "tar_shine": (240, 170, 70), "amber": (60, 30, 20)}
P, solid, ramp = palette(SHINY)
SCALE = 0.8
HITBOX = [1.6, 1.9]
KIND = "quadruped"
K = 3
HEIGHT = 30
LOOK = "a sticky black tar wyvern with glossy dripping hide, drip-edged tar sheet wings and amber glowing eyes"
CUT = (0, 0, 0, 0)


def tarf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" or (math.sin(x * 1.7 + z * 0.9) > 0.86 and face != "down"):
        return tone(p["tar_shine"], face), None                               # glossy highlights
    return p["tar"], None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 21.4) < 0.5 and -14.0 < z < -12.4:
        return p["amber"], p["amber"]                                         # glowing resin eyes
    return tarf(x, y, z, face, variant)


def wingf(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        drip = 14.0 + 1.6 * (abs(math.sin(abs(x) * 1.3)) ** 6) * -1 - 1.2 * (int(abs(x)) % 3 == 0)
        if y < drip - 1.4 + 0.8 * math.sin(abs(x) * 0.7):
            return CUT, None
        return (p["tar_shine"] if (int(abs(x)) % 4 == 0) else p["tar"]), None
    return s


def build() -> Model:
    m = Model("tarragon")
    top = m.bone("tarragon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    m.round_box(bd, 0, 1.0, 4.6, 8.0, 8.4, 17.0, tarf, cut=1.6)
    for z in (-4.0, 0.0, 4.0):
        spike(m, bd, (0, 16.8, z), (0, 1, 0.5), 1.6, 2.6, solid("tar_shine"))
    hd = m.bone("head", bd, (0, 17, -6))
    chain(m, hd, [(0, 15.0, -6.0), (0, 19.6, -9.4), (0, 21.0, -12.0)], [3.4, 3.0], tarf)   # neck
    m.box(hd, -2.4, 19.0, -16.4, 2.4, 23.0, -11.2, headf)                      # head
    m.box(hd, -1.8, 18.6, -19.4, 1.8, 20.8, -16.2, tarf)                       # snout
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.4, 22.6, -12.0), (sx * 0.3, 0.6, 1), 1.2, 3.2, solid("tar_shine"))   # swept horns
        for dz in (-17.6, -15.6):
            spike(m, hd, (sx * 1.2, 18.8, dz), (0, -1, 0), 0.8, 1.6, solid("tar_shine"))       # drips from the jaw
    tl = m.bone("tail", bd, (0, 12, 8))
    chain(m, tl, [(0, 12.0, 8.0), (0, 10.0, 14.0), (0, 7.0, 19.0), (0, 4.4, 23.0)], [3.0, 2.4, 1.8], tarf)
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 4, 16, -2))
        x0, x1 = sorted((sx * 4.0, sx * 17.0))
        m.box(w, x0, 9.0, -2.0, x1, 18.0, -2.0, wingf(sx))                     # tar-sheet wing
        rod(m, w, (sx * 4.0, 16.4, -2.0), (sx * 17.0, 18.0, -2.0), 1.2, solid("tar_shine"), extend=0.4)
        for role, z in (("front", -4.4), ("back", 5.2)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 3.4, 11, z))
            rod(m, lb, (sx * 3.4, 11.0, z), (sx * 3.8, 1.0, z - 0.6), 2.6, tarf, extend=0.6)
            m.box(lb, sx * 3.8 - 1.6, 0.0, z - 2.6, sx * 3.8 + 1.6, 1.4, z + 0.8, solid("tar_shine"))
    return m
