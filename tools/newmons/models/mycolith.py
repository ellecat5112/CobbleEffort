"""Mycolith, the Ancient Spire Pokémon (Rock/Poison), a fossil Pokémon after the Prototaxites idea the user brought.

A stout, weathered stone pillar like a petrified tree stump: concentric rings on its flat top, bark-like bands down
its sides, glowing purple and amber mycelial threads pulsing through the cracks, a few small shelf fungi, two glowing
spore-like eyes peering out of a dark hollow near its base, and root tendrils it shuffles about on.

Front is -z, y is up. 18 units tall; baseScale 0.98 (1.1 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _fossil import STONE, STONE_SHINY, mycelium_stone
from _route import pal, tone

SCALE = 0.98
HITBOX = [0.9, 1.1]
KIND = "quadruped"
K = 4
LOOK = ("a stout weathered stone pillar like a petrified stump with rings on its flat top, glowing purple and amber "
        "mycelium in its cracks, glowing spore eyes in a hollow near its base and root tendrils")


def pillar(x, y, z, face, variant, **k):
    p = pal(STONE, STONE_SHINY, variant)
    if face == "north" and (x / 2.6) ** 2 + ((y - 6.8) / 1.9) ** 2 < 1:  # the hollow near its base
        for sx in (-1, 1):
            if ((x - sx * 1.1) / 0.6) ** 2 + ((y - 6.8) / 0.7) ** 2 < 1:
                return p["eye"], p["eye"]                              # glowing spore eyes
        return (28, 24, 26), None
    return mycelium_stone(x, y, z, face, variant, rings=(0, 0))


def shelf(x, y, z, face, variant, **k):
    p = pal(STONE, STONE_SHINY, variant)
    return tone(p["shelf"] if face != "down" else p["shelf_dark"], face), None


def rootf(x, y, z, face, variant, **k):
    return tone(pal(STONE, STONE_SHINY, variant)["root"], face), None


def build() -> Model:
    m = Model("mycolith")
    top = m.bone("mycolith", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0, 4.5, 4.5, 2.5, 15, pillar, cut=2)
    m.round_box(bd, 0, 0, 4, 4, 15, 17.5, pillar, cut=1)                  # the ringed top
    for sx, y0, z0 in ((1, 11, -1), (-1, 9, 1), (1, 6.5, 2)):             # little shelf fungi
        x0, x1 = sorted((sx * 4, sx * 6))
        m.box(bd, x0, y0, z0 - 1.5, x1, y0 + 1, z0 + 1.5, shelf)
    roots = [("leg_front_left", -3, -3), ("leg_front_right", 3, -3), ("leg_back_left", -3, 3), ("leg_back_right", 3, 3)]
    for nm, rx, rz in roots:
        lg = m.bone(nm, top, (rx, 3, rz))
        rod(m, lg, (rx, 3.5, rz), (rx * 1.9, 0.3, rz * 1.9), 1.5, rootf)
    return m
