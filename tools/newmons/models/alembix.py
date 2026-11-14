"""Alembix, the Alembic Pokémon (Steel/Water), Copperpot evolved (the user's design): a larger riveted copper pot on
four legs with a domed helmet head, from which a long, gracefully curved swan-neck pipe arches back over its body and
coils down into a cooling tank of water on its back; crystal-clear droplets drip from its spout.

Shiny: polished silver with a teal tank.

Front is -z, y is up. 22 units tall; baseScale 0.7 (1.0 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _liquor import eye_on, helix, palette, puff, tiers, translucent
from _route import tone

SHINY = {"copper": (206, 210, 220), "copper_dark": (150, 154, 166), "copper_light": (236, 240, 248),
         "glass": (150, 230, 220, 120)}
P, solid, ramp = palette(SHINY)
SCALE = 0.7
HITBOX = [1.2, 1.35]
KIND = "quadruped"
K = 3
HEIGHT = 22
LOOK = "a copper pot still on four legs with a domed head, a swan-neck pipe arching back into a coiled cooling tank"


def potf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.55 and abs(y - 12.4) < 0.55:
                return p["cyan"], p["cyan"]                                   # glowing gauge-glass eyes
    if abs(y - 8.4) < 0.3:
        return p["copper_dark"], None
    return tone(p["copper_light"] if face == "up" else p["copper"], face), None


def build() -> Model:
    m = Model("alembix")
    top = m.bone("alembix", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    tiers(m, bd, [(4.0, 5.6, 4.0), (5.6, 10.0, 5.6), (10.0, 12.4, 5.0)], potf, cz=-1.0)
    tiers(m, bd, [(5.0, 11.0, 3.2)], translucent(P, "glass"), cz=6.2)            # the cooling tank on its back
    tiers(m, bd, [(5.6, 9.6, 2.2)], translucent(P, "water"), cz=6.2)
    helix(m, bd, (0, 0, 6.2), 2.6, 5.4, 10.6, 2.5, 0.7, solid("copper_light"))  # the coil in the tank
    hd = m.bone("head", bd, (0, 12, -1))
    tiers(m, hd, [(12.4, 14.4, 3.8), (14.4, 15.6, 2.6), (15.6, 16.4, 1.2)], potf, cz=-1.0)
    chain(m, hd, [(0, 16.2, -1.0), (0, 19.4, 0.4), (0, 20.0, 3.4), (0, 17.6, 6.0), (0, 11.4, 6.2)],
          [1.2, 1.1, 1.0, 0.9], solid("copper"))                                   # the swan-neck pipe
    rod(m, bd, (0, 6.0, -6.2), (0, 5.0, -8.4), 0.8, solid("copper_dark"), extend=0.2)   # spout
    puff(m, bd, (0, 3.6, -8.6), 0.5, translucent(P, "glass_rim"))                # a clear droplet
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -3.6), ("back", 3.4)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 3.4, 5, z))
            m.round_box(lb, sx * 3.4, z, 0.9, 0.9, 0.0, 5.4, solid("copper_dark"), cut=0.3)
    return m
