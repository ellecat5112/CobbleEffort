"""Wigwoof, the Wig Pup Pokémon (Grass), the grass starter, after the art of the A. Fakemon fanpage (the art's own
name): a light green wolf pup with a big blond bowl of hair over its eyes like a wig, orange eyes, a brown nose and
a little fang, and a bushy dark green tail tipped yellow. Small leaves grow on its front legs.

Shiny: slate-blue with silver hair.

Front is -z, y is up. 18 units tall to the top of its hair; baseScale 0.45 (0.5 m).
"""
from __future__ import annotations

from _afake import round_eye
from _boxmodel import Model, rod, spike
from _route import tone
from _wolfpup import P, solid

SCALE = 0.45
HITBOX = [0.9, 1.1]
KIND = "quadruped"
K = 5
HEIGHT = 18
LOOK = ("a light green wolf pup with a big blond bowl of hair like a wig, orange eyes, a brown nose, a little fang and "
        "a bushy dark green tail tipped yellow")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return p["green_light"], None
    return tone(p["green_dark"] if face == "up" and abs(x) < 1.6 else p["green"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = round_eye(x - sx * 1.7, y - 11.4, 1.15, p, "eye", ry=1.35, look=(-sx * 0.15, 0))
            if e:
                return e, None
    return tone(p["green"], face), None


def snoutf(x, y, z, face, variant, **k):
    p = P(variant)
    if (face == "north" and y > 9.4) or (face == "up" and z < -11.6):
        return p["nose"], None
    return tone(p["green_light"], face), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["green_light"] if y < 1.0 else p["green"], face), None


def build() -> Model:
    m = Model("wigwoof")
    top = m.bone("wigwoof", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 1.0, 3.2, 5.0, 4.0, 10.0, bodyf, cut=1.2)

    hd = m.bone("head", bd, (0, 10, -4))
    m.round_box(hd, 0, -7.0, 3.6, 3.4, 7.5, 14.5, headf, cut=1.2)
    m.box(hd, -1.6, 7.8, -12.6, 1.6, 10.6, -10.2, snoutf)                      # snout and brown nose
    spike(m, hd, (-0.8, 8.0, -12.2), (0, -1, -0.1), 1.0, 1.4, solid("white"))  # a little fang
    m.box(hd, -4.4, 13.0, -11.4, 4.4, 16.6, -2.4, solid("yellow"))             # the blond wig
    for x in (-3.4, -1.2, 1.2, 3.4):                                           # its fringe over the eyes
        spike(m, hd, (x, 13.6, -11.0), (0, -1, -0.45), 1.8, 2.2 + (x > 2) * 1.2, solid("yellow_dark"))
    for sx in (-1, 1):
        for z in (-9.0, -5.6):
            spike(m, hd, (sx * 4.2, 13.8, z), (sx * 0.5, -1, 0.1), 1.8, 2.4, solid("yellow_dark"))
    spike(m, hd, (2.6, 15.6, -11.2), (0.5, 0.4, -1), 2.2, 3.0, solid("yellow"), tip=1.0)   # its forward cowlick
    spike(m, hd, (0, 16.0, -3.0), (0, 0.5, 1), 2.4, 2.6, solid("yellow"))

    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -2.6), ("back", 4.4)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 2.0, 5.0, z))
            m.round_box(lb, sx * 2.0, z, 1.4, 1.4, 0.0, 6.0, legf, cut=0.6)
            if role == "front":                                                # a small leaf on each front leg
                spike(m, lb, (sx * 3.2, 3.2, z), (sx * 0.8, 0.3, -0.6), 1.2, 2.0, solid("green_dark"))

    tl = m.bone("tail", bd, (0, 9, 5.5))
    rod(m, tl, (0, 9.0, 5.5), (0, 12.6, 11.6), 4.0, solid("green_dark"), extend=0.6, t2=3.6)
    rod(m, tl, (0, 12.4, 11.2), (0, 14.4, 15.6), 4.4, solid("yellow"), extend=0.4, t2=4.0)
    for sx in (-1, 0, 1):                                                      # the spiky yellow tip
        spike(m, tl, (sx * 1.3, 14.4, 15.4), (sx * 0.4, 0.5, 1), 1.4, 2.2, solid("yellow_dark"))
    return m
