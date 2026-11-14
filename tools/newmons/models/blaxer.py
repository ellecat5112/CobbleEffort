"""Blaxer, the Boxer Hound Pokémon (Fire), Flachiko evolved, after the art of the A. Fakemon fanpage (the art's own
name): a bounding boxer dog with red-and-white flame-patched fur, long yellow legs with red-brown paws, a yellow face
with a short flat muzzle, droopy flame-tipped ears, a white tuft of hair, a lilac spiked collar and a flame for a tail.

Shiny: charcoal grey with pale flames and a green collar.

Front is -z, y is up. 22 units tall; baseScale 0.72 (1.0 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _firepup import P, flame, ramp, solid
from _route import tone

SCALE = 0.72
HITBOX = [1.2, 1.4]
KIND = "quadruped"
K = 4
HEIGHT = 22
LOOK = ("a bounding boxer dog with red-and-white fur, long yellow legs, a yellow face with a flat muzzle, droopy "
        "flame-tipped ears, a white tuft, a lilac spiked collar and a flame tail")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down" or (face != "up" and y < 10.4):
        return tone(p["white"], face), None
    if face in ("east", "west", "up") and abs(((z + 6) % 4.4) - 2.2) < 0.4:
        return p["white"], None                                               # pale flame-crack patches
    return tone(p["red"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.5, y - 16.6
            if abs(dx) < 0.6 and abs(dy) < 0.5:
                return (p["pupil"] if dx * sx < 0.05 else p["white"]), None
        return tone(p["yellow"], face), None
    if face == "up":
        return tone(p["red"], face), None
    return tone(p["yellow"] if y < 16.0 else p["red"], face), None


def build() -> Model:
    m = Model("blaxer")
    top = m.bone("blaxer", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11, 0))
    m.round_box(bd, 0, 1.0, 3.4, 7.0, 8.4, 15.0, bodyf, cut=1.4)
    m.round_box(bd, 0, -6.0, 3.8, 1.2, 12.0, 13.6, solid("lilac"), cut=1.0)     # the spiked collar
    for sx in (-1, 0, 1):
        spike(m, bd, (sx * 3.0, 12.8, -7.0), (sx * 0.8, 0, -0.6), 1.0, 1.6, solid("lilac"))

    hd = m.bone("head", bd, (0, 14, -7))
    m.round_box(hd, 0, -9.6, 3.4, 3.0, 12.4, 19.2, headf, cut=1.2)
    m.box(hd, -2.0, 12.6, -13.6, 2.0, 15.2, -12.2, solid("yellow"))              # the flat muzzle
    m.box(hd, -0.8, 14.4, -13.8, 0.8, 15.4, -13.4, solid("nose"))
    for sx in (-1, 1):
        rod(m, hd, (sx * 2.6, 18.4, -9.0), (sx * 5.4, 16.6, -7.0), 2.4, ramp("red", "orange"), extend=0.4, t2=1.0)
        spike(m, hd, (sx * 5.2, 16.8, -7.0), (sx * 0.6, -0.6, 0.3), 1.6, 2.0, flame)          # flame-tipped ears
    for d in ((0, 1, 0.3), (-0.4, 1, 0.2), (0.4, 1, 0.2)):
        spike(m, hd, (d[0] * 2, 19.0, -9.6), d, 1.6, 2.6, solid("white"))       # its white tuft

    for sx, side in ((-1, "left"), (1, "right")):
        for role, z, reach in (("front", -4.4, -1.6), ("back", 5.6, 1.6)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 2.6, 10, z))
            rod(m, lb, (sx * 2.6, 10.0, z), (sx * 2.8, 4.6, z + reach), 2.2, solid("yellow"), extend=0.5)
            rod(m, lb, (sx * 2.8, 4.6, z + reach), (sx * 2.8, 1.0, z), 1.8, solid("yellow"), extend=0.5)
            m.round_box(lb, sx * 2.8, z - 0.4, 1.3, 1.6, 0.0, 1.6, solid("paw"), cut=0.5)

    tl = m.bone("tail", bd, (0, 14, 7.6))
    for d, h in (((0, 1, 0.5), 4.4), ((-0.5, 0.8, 0.6), 3.0), ((0.5, 0.8, 0.6), 3.0)):
        spike(m, tl, (0, 14.0, 7.6), d, 2.4, h, flame, tip=1.0)
    return m
