"""Taxitower, the Primordial Pillar Pokémon (Rock/Poison), a fossil Pokémon after the Prototaxites idea the user
brought: as tall as the tallest real Prototaxites (8 m).

A colossal tapering obelisk of banded slate and hardened fungal tissue: glowing mycelium threads in its cracks,
petrified shelf-fungus plates sticking out all the way up like armour, heavy buttress roots anchoring its base, two
glowing spore eyes in a hollow low on its trunk, and a crown that splits open like a chimney, glowing gold inside,
venting a translucent cloud of golden spores.

Front is -z, y is up. 56 units tall to its spore cloud; baseScale 2.3 (8.0 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod
from _fossil import STONE, STONE_SHINY, mycelium_stone
from _route import pal, tone

SCALE = 2.3
HITBOX = [1.04, 3.04]
KIND = "quadruped"
K = 2
HEIGHT = 56
LOOK = ("a colossal tapering obelisk of banded slate and fungal tissue with glowing mycelium, petrified shelf-fungus "
        "armour, buttress roots and a crown split open like a chimney venting a cloud of golden spores")

TRUNK = [(5, 14, 7, 6.5), (14, 24, 6, 5.5), (24, 34, 5, 4.5), (34, 42, 4.5, 4)]      # (y0, y1, rx, rz)


def trunk(x, y, z, face, variant, **k):
    p = pal(STONE, STONE_SHINY, variant)
    if face == "north" and (x / 3.0) ** 2 + ((y - 10.5) / 2.2) ** 2 < 1:
        for sx in (-1, 1):
            if ((x - sx * 1.3) / 0.7) ** 2 + ((y - 10.5) / 0.8) ** 2 < 1:
                return p["eye"], p["eye"]
        return (28, 24, 26), None
    c, g = mycelium_stone(x, y, z, face, variant)
    if g is None and face not in ("up", "down") and int(y * 0.5) % 2:
        c = mix(c, p["slate"], 0.45)                                       # banded slate
    return c, g


def crown(x, y, z, face, variant, **k):
    p = pal(STONE, STONE_SHINY, variant)
    if face == "up" and math.hypot(x, z) < 2.6:
        return p["spore"], p["spore"]                                      # glowing gold inside the chimney
    return trunk(x, y, z, face, variant)


def shelf(x, y, z, face, variant, **k):
    p = pal(STONE, STONE_SHINY, variant)
    if face == "up" and int(math.hypot(x, z) * 1.5) % 2:
        return p["shelf_dark"], None
    return tone(p["shelf"], face), None


def spores(x, y, z, face, variant, **k):
    p = pal(STONE, STONE_SHINY, variant)
    return p["spore"] + (95,), p["spore"]


def rootf(x, y, z, face, variant, **k):
    return tone(pal(STONE, STONE_SHINY, variant)["root"], face), None


def build() -> Model:
    m = Model("taxitower")
    top = m.bone("taxitower", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 7.5, 7, 0, 6, trunk, cut=3)                     # its base
    for y0, y1, rx, rz in TRUNK:
        m.round_box(bd, 0, 0, rx, rz, y0, y1, trunk, cut=2)
    cap = m.bone("cap", bd, (0, 42, 0))
    for sx, sz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):                    # the split-open chimney crown
        x0, x1 = sorted((sx * 0.6, sx * 4))
        z0, z1 = sorted((sz * 0.6, sz * 3.6))
        m.box(cap, x0, 42, z0, x1, 47 + (sx + sz + 2) * 0.5, z1, crown)
    m.box(cap, -3, 41.5, -3, 3, 42.5, 3, crown)                            # its glowing floor
    for (cx, cy, cz, r) in ((0, 50, 0, 3), (1.5, 53, -1, 2.5), (-1.2, 54.5, 1, 2)):   # the golden spore cloud
        m.box(cap, cx - r, cy - r * 0.8, cz - r, cx + r, cy + r * 0.8, cz + r, spores)
    plates = [(7, 9, 0, 1), (-7, 16, 2, -1), (6.5, 20, -2, 1), (-5.5, 27, -1, -1), (5, 31, 2, 1), (-4.8, 37, 0, -1),
              (0, 18, -6.5, 0), (0, 29, 5.2, 0)]
    for px, py, pz, sx in plates:                                          # petrified shelf-fungus armour
        if sx:
            x0, x1 = sorted((px, px + sx * 3.5))
            m.box(bd, x0, py, pz - 2.5, x1, py + 1.2, pz + 2.5, shelf)
        else:
            sz = -1 if pz < 0 else 1
            z0, z1 = sorted((pz, pz + sz * 3.5))
            m.box(bd, -2.5, py, z0, 2.5, py + 1.2, z1, shelf)
    for i in range(6):                                                     # buttress roots
        a = i * math.pi / 3 + math.pi / 6
        dx, dz = math.sin(a), math.cos(a)
        rod(m, bd, (dx * 5.5, 7, dz * 5.5), (dx * 12, 0.5, dz * 12), 3, rootf)
    return m
