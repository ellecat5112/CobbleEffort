"""Subohmega, the Sub-Ohm Pokémon (Electric/Steel), Modwing evolved (the user's design): a heavy, industrial-grade
mechanical falcon of brushed stainless steel: a broad chest window with glowing cherry-red resistance coils, a sharp
hooked steel beak and amber visor eyes, great wings of overlapping steel feather plates, a fanned steel tail and heavy
talons, venting electrified vapour.

Shiny: a black-steel falcon with blue coils.

Front is -z, y is up. 30 units tall; baseScale 0.85 (1.6 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _liquor import helix
from _nico import palette, puff, translucent
from _route import tone

SHINY = {"steel": (70, 74, 84), "steel_dark": (40, 42, 50), "red": (80, 170, 255), "ember_hot": (190, 230, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.85
HITBOX = [1.6, 1.85]
KIND = "floater"
K = 3
HEIGHT = 30
LOOK = "a heavy brushed-steel mechanical falcon with glowing cherry-red coils in its chest, steel feather wings and talons"
ANIM = {"wing_flap": 18}
CUT = (0, 0, 0, 0)


def plate(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "east", "west") and ((x * 0.8 + z * 0.8 + y * 0.4) % 2.0) < 0.18:
        return p["steel_dark"], None                                          # brushed panel seams
    return tone(p["steel"], face), None


def coilf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["ember_hot"] if (int(y * 2) % 3 == 0) else p["red"]
    return c, c


def wingf(x, y, z, face, variant, **k):
    p = P(variant)
    ax = abs(x)
    tip = 22.0 - (ax - 3.0) * 0.55
    if y > tip or y < 13.0 - (ax - 3.0) * 0.35 + 1.4 * (int(ax) % 2):
        return CUT, None                                                      # stepped feather tips
    return (p["steel"] if int(ax) % 2 else p["steel_dark"]), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(y - 25.2) < 0.45 and z < -3.0:
        return p["amber"], p["amber"]                                         # the visor
    return plate(x, y, z, face, variant)


def build() -> Model:
    m = Model("subohmega")
    top = m.bone("subohmega", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0.6, 4.6, 6.0, 10.0, 21.0, plate, cut=1.6)              # the steel body
    m.box(bd, -2.6, 12.0, -5.8, 2.6, 18.6, -5.2, solid("black"))                # the chest window
    helix(m, bd, (0, 0, -5.6), 1.2, 12.6, 18.0, 3.0, 0.7, coilf)                # glowing resistance coils
    hd = m.bone("head", bd, (0, 21, -3))
    m.round_box(hd, 0, -3.0, 2.8, 2.8, 21.0, 27.6, headf, cut=0.9)
    spike(m, hd, (0, 24.2, -5.6), (0, -0.5, -1), 1.6, 3.0, solid("steel_dark"), tip=0.7)   # the hooked beak
    tl = m.bone("tail", bd, (0, 12, 6))
    for i in range(5):
        a = math.radians(-40 + i * 20)
        rod(m, tl, (0, 12.0, 6.0), (math.sin(a) * 4.0, 9.0, 6.0 + math.cos(a) * 7.0), 1.6, plate, extend=0.3, t2=0.6)
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 4.4, 19, 0))
        x0, x1 = sorted((sx * 4.4, sx * 17.0))
        m.box(w, x0, 10.0, 0.0, x1, 22.0, 0.0, wingf, rotation=(0, sx * 12, 0), pivot=(sx * 4.4, 19.0, 0.0))
        rod(m, w, (sx * 4.4, 19.6, 0.0), (sx * 16.6, 21.6, 0.0), 1.4, plate, extend=0.3)
        lb = m.bone(f"leg_{side}", top, (sx * 2, 11, 0))
        rod(m, lb, (sx * 2.0, 11.0, 0.0), (sx * 2.2, 6.0, -0.4), 1.6, solid("steel_dark"), extend=0.3)
        for d in ((0, -1, -1), (sx * 0.6, -1, -0.6), (0, -1, 1)):
            spike(m, lb, (sx * 2.2, 6.0, -0.4), d, 0.6, 2.0, solid("black"))     # talons
    for c, r in (((3.0, 9.0, 8.0), 1.8), ((-2.4, 7.0, 10.6), 1.4)):
        puff(m, bd, c, r, translucent(P, "mist"))
    return m
