"""Curedrake, the Curing Leaf Pokémon (Grass/Poison), Nicotiny evolved (the user's design): its leaves have matured to
a rich golden-amber and curled inward like drying tobacco bundles: a pendulous body of curled leaf layers, two broad
cured-leaf wings, sleepy half-closed eyes, hooked feet on top for hanging upside down from branches, and a drop of its
fermenting sap glowing at its tip.

Shiny: pale silver-green leaves.

Front is -z, y is up. 20 units tall; baseScale 0.5 (0.9 m). A floater.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _nico import palette, puff
from _route import tone

SHINY = {"tobacco": (176, 196, 150), "tobacco_dark": (120, 146, 104), "tobacco_light": (214, 230, 190),
         "amber": (190, 230, 120)}
P, solid, ramp = palette(SHINY)
SCALE = 0.5
HITBOX = [1.0, 1.2]
KIND = "floater"
K = 4
HEIGHT = 20
LOOK = "a pendulous bundle of curled golden-amber cured leaves with leaf wings, sleepy eyes and hooked feet on top"
CUT = (0, 0, 0, 0)


def bundlef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.7 and abs(y - 10.4) < 0.25:
                return p["pupil"], None                                       # sleepy half-closed eyes
    u = x if face in ("north", "south") else z
    curl = (y * 1.2 + math.sin(u * 0.9) * 1.4) % 2.4
    if curl < 0.35:
        return tone(p["tobacco_dark"], face), None                            # the curled leaf edges
    return tone(p["amber"] if curl > 1.6 else p["tobacco_light"], face), None


def wingf(x, y, z, face, variant, **k):
    p = P(variant)
    ax = abs(x)
    half = 4.2 * math.sin(math.pi * min(1.0, max(0.0, (ax - 2.6) / 8.4)))      # a leaf outline
    if abs(y - 11.0) > half:
        return CUT, None
    if abs(y - 11.0) < 0.25:
        return p["tobacco_dark"], None                                        # the midrib
    return (p["amber"] if (int(ax) % 3 == 0) else p["tobacco_light"]), None


def build() -> Model:
    m = Model("curedrake")
    top = m.bone("curedrake", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for y0, r in ((3.0, 1.2), (4.6, 2.2), (6.4, 3.0), (8.4, 3.4), (10.6, 3.2), (12.8, 2.6), (14.8, 1.8)):
        m.round_box(bd, 0, 0, r, r, y0, y0 + 2.2, bundlef, cut=max(0.5, round(r * 0.35, 1)))
    hd = m.bone("head", bd, (0, 10, 0))
    puff(m, hd, (0, 2.2, 0), 0.8, lambda *a, **k: (P(k.get("variant"))["leaf_light"], P(k.get("variant"))["leaf_light"]))
    for sx in (-1, 1):
        rod(m, bd, (sx * 0.8, 16.6, 0.0), (sx * 1.0, 19.0, 0.0), 0.8, solid("tobacco_dark"), extend=0.2)   # legs
        spike(m, bd, (sx * 1.0, 19.0, 0.0), (sx * 0.2, 0.2, -1), 0.6, 1.4, solid("pupil"))                # hooked feet
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 2.6, 12, 0))
        x0, x1 = sorted((sx * 2.6, sx * 11.0))
        m.box(w, x0, 6.8, 0.0, x1, 15.2, 0.0, wingf, rotation=(0, sx * 14, 0), pivot=(sx * 2.6, 12.0, 0.0))
    return m
