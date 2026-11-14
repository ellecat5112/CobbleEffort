"""Flachiko, the Ember Pup Pokémon (Fire), the fire starter of the second A. Fakemon trio, after the art of the A.
Fakemon fanpage (the art's own name): a grumpy little red-and-white pup with a round head, a yellow face mask, pointed
ears, a scowl, a fluffy white ruff licked with flame, short legs with dark paws and a flame for a tail.

Shiny: charcoal grey with pale flames.

Front is -z, y is up. 16 units tall; baseScale 0.42 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _firepup import P, flame, fur, solid
from _route import tone

SCALE = 0.42
HITBOX = [0.75, 1.0]
KIND = "quadruped"
K = 5
HEIGHT = 16
LOOK = ("a grumpy red-and-white pup with a round head, a yellow face mask, pointed ears, a white flame-licked ruff, "
        "dark paws and a flame tail")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.4, y - 11.0
            if dy > 0.35 - dx * sx * 0.4 and abs(dx) < 0.9 and dy < 0.9:
                return p["red_dark"], None                                    # a scowling brow
            if abs(dx) < 0.55 and abs(dy) < 0.45:
                return (p["pupil"] if dx * sx < 0.1 else p["white"]), None
        if abs(x) < 0.6 and 9.0 < y < 9.8:
            return p["nose"], None
        if y < 10.4 + max(0.0, 1.6 - abs(x) * 0.9):
            return tone(p["yellow"], face), None                              # the yellow face mask
    if y < 10.0 and face in ("east", "west"):
        return tone(p["white"], face), None
    return tone(p["red"], face), None


def build() -> Model:
    m = Model("flachiko")
    top = m.bone("flachiko", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 1.5, 2.8, 4.2, 3.6, 9.0, fur("red", "white", 6.6), cut=1.2)
    for d in ((-1, 0.2, -0.4), (1, 0.2, -0.4), (0, -0.4, -1), (-0.6, -0.4, -1), (0.6, -0.4, -1)):   # white ruff
        spike(m, bd, (d[0] * 2.2, 8.6, -2.4), d, 1.8, 2.0, solid("white"))

    hd = m.bone("head", bd, (0, 9, -2.5))
    m.round_box(hd, 0, -3.4, 3.6, 3.0, 7.6, 14.0, headf, cut=1.2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.2, 13.4, -3.4), (sx * 0.35, 1, 0.1), 2.2, 3.0, solid("red"), tip=1.0)   # ears
        m.box(hd, sx * 2.2 - 0.5, 13.8, -4.4, sx * 2.2 + 0.5, 15.0, -4.2, solid("yellow"))           # ear insides

    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -1.4), ("back", 4.4)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 1.8, 4, z))
            m.round_box(lb, sx * 1.8, z, 1.2, 1.2, 1.0, 4.6, solid("white"), cut=0.5)
            m.round_box(lb, sx * 1.8, z - 0.2, 1.3, 1.4, 0.0, 1.2, solid("paw"), cut=0.5)

    tl = m.bone("tail", bd, (0, 8, 5.6))
    for d, h in (((0, 1, 0.6), 4.0), ((-0.4, 0.8, 0.8), 3.0), ((0.4, 0.8, 0.8), 3.0)):
        spike(m, tl, (0, 8.0, 5.4), d, 2.2, h, flame, tip=1.0)                # its flame tail
    return m
