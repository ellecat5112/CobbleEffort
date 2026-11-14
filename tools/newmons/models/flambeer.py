"""Flambéer, the Spirit Flame Pokémon (Fire/Water), a Liquor Meadows Pokémon (the user's design): a volatile,
overproof spirit elemental floating inside a crystal snifter: a round amber liquid body with a calm face, a clear glass
bowl round it on a short stem and foot, and a crown of cool, flickering blue ethanol flames on its surface.

Shiny: a rosé spirit with green flames.

Front is -z, y is up. 20 units tall; baseScale 0.48 (0.6 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _liquor import eye_on, palette, tiers, translucent
from _route import tone

SHINY = {"amber": (236, 130, 150), "amber_light": (250, 180, 196), "flame_blue": (80, 230, 120),
         "flame_blue_hot": (200, 255, 210)}
P, solid, ramp = palette(SHINY)
SCALE = 0.48
HITBOX = [0.8, 1.2]
KIND = "floater"
K = 5
HEIGHT = 20
LOOK = "an amber spirit elemental in a crystal snifter with a calm face and a crown of cool blue flames"
eyes = eye_on(P, "amber_light", [(-1.3, 9.4), (1.3, 9.4)], 0.8)


def spiritf(x, y, z, face, variant, **k):
    p = P(variant)
    e = eyes(x, y, z, face, variant)
    if e:
        return e, None
    if face == "north" and abs(y - 8.0) < 0.25 and abs(x) < 0.8:
        return p["pupil"], None
    return tone(p["amber_light"] if y > 10.6 else p["amber"], face), None


def flamef(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["flame_blue_hot"] if y < 12.0 and abs(x) < 0.6 else p["flame_blue"]
    return c, c


def build() -> Model:
    m = Model("flambeer")
    top = m.bone("flambeer", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    tiers(m, bd, [(0.0, 0.8, 3.0), (0.8, 3.2, 0.8)], translucent(P, "glass"))          # foot and stem
    tiers(m, bd, [(3.0, 4.6, 3.6), (4.6, 6.6, 5.2), (6.6, 9.4, 5.8), (9.4, 11.6, 5.4), (11.6, 13.2, 4.6)],
          translucent(P, "glass"))                                                        # the snifter bowl
    hd = m.bone("head", bd, (0, 9, 0))
    tiers(m, hd, [(4.0, 5.4, 3.0), (5.4, 11.4, 4.4)], spiritf)                             # the spirit body
    for i, (dx, dz, h) in enumerate(((0, 0, 4.4), (-2.2, -0.8, 3.0), (2.2, -0.8, 3.0), (-1.2, 1.6, 2.6), (1.4, 1.6, 2.8))):
        spike(m, hd, (dx, 11.2, dz), (dx * 0.08, 1, dz * 0.05), 1.6, h, flamef, tip=0.8)  # the crown of blue flames
    return m
