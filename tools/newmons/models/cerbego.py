"""Cerbego, the Hellhound Pokémon (Fire/Ghost), Blaxer evolved, after the art of the A. Fakemon fanpage (the art's own
name): a huge lion-like fire dog with a red body, a great mane of flames, thick yellow legs with orange paws and purple
claws, flame horns, black-rimmed furious eyes and a roaring, fanged mouth. Purple ghost-fire wreathes it: two
translucent phantom heads flare beside its own, as if it were three-headed, and purple wisps drift over its back.

Shiny: charcoal grey with spectral green ghost-fire.

Front is -z, y is up. 30 units tall; baseScale 0.98 (1.85 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _firepup import P, flame, fur, ghost, solid, wisp
from _route import tone

SCALE = 0.98
HITBOX = [2.0, 1.9]
KIND = "quadruped"
K = 3
HEIGHT = 30
LOOK = ("a huge lion-like fire dog with a mane of flames, flame horns, a roaring fanged mouth and two translucent purple "
        "phantom heads flaring beside its own, purple wisps drifting over its back")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.8, y - 19.4
            d = math.hypot(dx, dy)
            if d < 0.55:
                return p["pupil"], None
            if d < 1.0:
                return (p["white"] if dy < 0.3 else p["pupil"]), None         # black-rimmed furious eyes
        if abs(x) < 0.7 and 17.0 < y < 17.8:
            return p["nose"], None
        if (x / 2.6) ** 2 + ((y - 14.8) / 1.6) ** 2 < 1:
            if abs(y - 14.8) > 1.0 and int((x + 2.6) / 0.65) % 2 == 0:
                return p["white"], None                                       # fangs
            return p["mouth"], None                                           # the roaring mouth
    return tone(p["red"], face), None


def phantom(m, bone, cx, cy, cz, sx):
    """A translucent purple phantom dog head made of ghost-fire."""
    m.round_box(bone, cx, cz, 2.6, 3.0, cy - 3.0, cy + 3.0, ghost, cut=1.0)
    m.box(bone, cx - 1.4, cy - 2.6, cz - 5.0, cx + 1.4, cy - 0.4, cz - 2.8, ghost)
    for d in ((sx * 0.4, 1, 0.2), (sx * 0.8, 0.7, 0.6)):
        spike(m, bone, (cx, cy + 2.6, cz + 0.6), d, 1.6, 3.0, wisp, tip=0.8)


def build() -> Model:
    m = Model("cerbego")
    top = m.bone("cerbego", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 2.0, 6.0, 10.0, 10.0, 22.0, fur("red", "white", 12.0), cut=2.4)
    m.round_box(bd, 0, -6.0, 7.0, 4.0, 10.0, 25.0, solid("red"), cut=2.0)       # the mane
    for i in range(10):                                                          # its mane of flames
        a = math.pi * (i / 9.0) - math.pi / 2
        spike(m, bd, (6.4 * math.sin(a), 18.0 + 6.0 * math.cos(a), -6.0), (math.sin(a), math.cos(a) * 0.9 + 0.3, 0.2),
              2.6, 4.0, flame, tip=1.2)
    for z in (0.0, 5.0, 10.0):
        spike(m, bd, (0, 22.0, z), (0, 1, 0.4), 2.4, 3.4, flame, tip=1.0)

    hd = m.bone("head", bd, (0, 18, -10))
    m.round_box(hd, 0, -11.4, 4.4, 3.6, 13.0, 22.0, headf, cut=1.4)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 21.6, -10.4), (sx * 0.3, 1, 0.3), 2.6, 5.0, flame, tip=1.2)   # flame horns

    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -6.0), ("back", 9.0)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 4.2, 11, z))
            m.round_box(lb, sx * 4.2, z, 2.2, 2.4, 1.6, 12.0, solid("yellow"), cut=0.8)
            m.round_box(lb, sx * 4.2, z - 0.6, 2.6, 2.8, 0.0, 2.4, solid("orange"), cut=0.8)
            for dx in (-1.4, 0.0, 1.4):
                spike(m, lb, (sx * 4.2 + dx, 0.8, z - 3.0), (0, -0.3, -1), 1.0, 1.8, solid("claw"))
        g = m.bone(f"ghost_{side}", bd, (sx * 6.0, 20, -8))                      # phantom heads beside its own
        phantom(m, g, sx * 10.6, 20.0, -8.0, sx)

    w = m.bone("ghost_wisps", bd, (0, 26, 2))
    for c in ((-3.0, 27.0, -1.0), (1.0, 29.0, 2.0), (4.0, 27.6, 5.0), (-1.0, 28.4, 7.0)):
        spike(m, w, c, (0, 1, 0.2), 1.6, 2.6, wisp, tip=0.8)                     # drifting wisps

    tl = m.bone("tail", bd, (0, 20, 12))
    for d, h in (((0, 1, 0.6), 7.0), ((-0.6, 0.8, 0.6), 5.0), ((0.6, 0.8, 0.6), 5.0), ((0, 0.4, 1), 5.0)):
        spike(m, tl, (0, 20.0, 11.6), d, 3.4, h, flame, tip=1.4)                # a plume of flame
    return m
