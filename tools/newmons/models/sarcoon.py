"""Sarcoon, the Sarcophagus Pokémon (Water/Bug), hand-built from boxes from the user's design.

A cocoon shaped like a pharaoh's sarcophagus with a bug's lines: a domed head striped like a royal headcloth in blue and
pale blue, a black visor face with two big round glowing eyes, a golden cobra rearing from its brow and a golden false
beard, and below it a body bound in gold and blue bands that tapers to a point, with a ridge of gold down the back like
folded wing cases.

Front is -z, y is up. 25 units tall; baseScale 0.64 (1.0 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain
from _pharaoh import P, gold, gold_bands, nemes, ring_eye, visor

SCALE = 0.64
HITBOX = [0.8, 1.0]
KIND = "quadruped"
K = 4
LOOK = ("a cocoon shaped like a pharaoh's sarcophagus: a blue-striped domed head with a black visor, glowing eyes, a "
        "golden cobra on the brow and a golden beard, over a body bound in gold and blue bands")

BODY = [(0, 2, 2.5, 2), (2, 5, 3.5, 3), (5, 9, 4.5, 3.5), (9, 13, 5, 4)]     # (y0, y1, rx, rz)


def headf(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = ring_eye(x - sx * 2.1, y - 17.5, 1.5, variant)
            if e:
                return e
        if visor(x, y - 17.2, 4.5, 2.7):
            return pal["black"], None
    return nemes(x, y, z, face, variant, axis="y" if face in ("north", "south", "east", "west") else "x", period=1.3)


def bodyf(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north" and abs(x) < 1.6:                     # crossed gold bands down the front
        return gold(x, y, z, face, variant)
    if (y % 2.6) < 1.1:
        return gold_bands(x, y, z, face, variant)
    return (pal["blue"] if face != "down" else pal["blue_pale"]), None


def build() -> Model:
    m = Model("sarcoon")
    top = m.bone("sarcoon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for y0, y1, rx, rz in BODY:
        m.round_box(bd, 0, 0, rx, rz, y0, y1, bodyf, cut=1)
    m.box(bd, -1, 4, 3.5, 1, 13, 4.5, gold)                   # a gold ridge down the back
    hd = m.bone("head", bd, (0, 13, 0))
    m.round_box(hd, 0, -0.5, 6, 5, 13, 21, headf, cut=2)      # the domed, striped head
    m.round_box(hd, 0, -0.5, 4.5, 3.5, 21, 23, headf, cut=1)
    m.box(hd, -1, 11.5, -5.8, 1, 14, -4.8, gold)              # the false beard
    chain(m, hd, [(0, 20.5, -5.6), (0, 23, -6.4), (0, 24.5, -5.2)], [1.5, 1.2], gold)   # the cobra on its brow
    m.box(hd, -1.5, 23.5, -6.2, 1.5, 25, -4.7, gold)          # the cobra's hood
    return m
