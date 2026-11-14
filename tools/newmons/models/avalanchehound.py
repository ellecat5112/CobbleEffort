"""Avalanche Hound, the Rescue Pokémon (Normal/Fighting), Kegguard evolved (the user's design): a massive, heroic
mountain dog, white with chestnut patches and a mask, with two heavy iron-banded oak barrels strapped across its broad
shoulders like cannon pods, their bungs glowing with warm tonic, a red rescue harness and a thick snowy ruff.

Shiny: black and white with golden barrels.

Front is -z, y is up. 34 units tall; baseScale 0.95 (2.0 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _hound import P, SHINY, dog, ramp, solid  # noqa: F401
from _liquor import puff, tube_z
from _route import tone

SCALE = 0.95
HITBOX = [1.8, 1.9]
KIND = "quadruped"
K = 3
HEIGHT = 34
LOOK = "a massive heroic mountain dog with two iron-banded oak barrels strapped on its shoulders like cannon pods"


def barrelf(x, y, z, face, variant, **k):
    p = P(variant)
    if abs(z + 6.0) < 0.6 or abs(z - 2.0) < 0.6:
        return p["iron"], None                                                # iron bands
    if face == "north" and abs(y - 27.8) < 0.9 and abs(abs(x) - 4.2) < 0.9:
        return p["amber_light"], p["amber_light"]                             # the glowing tonic bung
    return tone(p["oak"] if int((y + 20) * 0.9) % 2 else p["oak_light"], face), None


def build() -> Model:
    m = dog(Model("avalanchehound"), 2.6, True)
    for sx in (-1, 1):
        tube_z(m, "body", sx * 4.2, 27.8, 2.6, -9.0, 4.0, barrelf)                # the shoulder barrels
    for z in (-7.4, 1.6):
        m.box("body", -7.9, 24.0, z, 7.9, 25.4, z + 1.2, solid("red"))                # the rescue harness straps
    for x, y in ((-4.0, 20.0), (0.0, 19.0), (4.0, 20.0), (-2.2, 22.6), (2.2, 22.6)):
        puff(m, "body", (x, y, -12.6), 2.2, solid("white"))                       # a thick snowy ruff
    return m
