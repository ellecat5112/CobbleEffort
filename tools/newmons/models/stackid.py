"""Stackid, the Cairn Pokémon (Rock; the user's art, artist not named, name kept): a little cairn of stones, each with
a face of its own: a broad grey bottom stone with two slit eyes, a stubby pebble hand and pebble feet, a grumpy brown
stone with a V-browed glare and a frown, an olive stone with two slits, and two small pebbles on top.

Front is -z, y is up. 19 units tall; baseScale 0.45 (0.55 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _cairn import P, angry, pebble, slit, stone

SCALE = 0.45
HITBOX = [0.8, 1.1]
KIND = "biped"
K = 6
HEIGHT = 19
LOOK = ("a little cairn of stones with faces: a grey bottom stone with slit eyes and pebble hands and feet, a grumpy "
        "brown stone with a frown, an olive stone with slits, and two pebbles on top")


def bottom_face(x, y, z, face, p):
    if face == "north":
        for sx in (-1, 1):
            c = slit(p, x - sx * 1.5, y - 4.6, 0.45, 1.2)
            if c is not None:
                return c
    return None


def middle_face(x, y, z, face, p):
    if face == "north":
        for sx in (-1, 1):
            c = angry(p, x - sx * 1.5, y - 9.6, 1.0, 0.9, sx)
            if c is not None:
                return c
        if abs(y - (8.5 - 0.12 * x * x)) < 0.3 and abs(x) < 1.6:      # a frown
            return p["eye"]
    return None


def olive_face(x, y, z, face, p):
    if face == "north":
        for sx in (-1, 1):
            c = slit(p, x - sx * 1.1, y - 12.9, 0.4, 0.8)
            if c is not None:
                return c
    return None


def build() -> Model:
    m = Model("stackid")
    top = m.bone("stackid", None, (0, 0, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 2, 0))
        pebble(m, lg, (sx * 2.6, 0, -0.6), 1.6, 2.0, 2.2, stone("grey_dark", seed=sx))
    bd = m.bone("body", top, (0, 2, 0))
    pebble(m, bd, (0, 1.6, 0), 5.4, 4.4, 5.8, stone("grey", extra=bottom_face))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 5.2, 4.5, 0))
        pebble(m, a, (sx * 6.6, 3.4, -0.4), 1.5, 1.4, 2.4, stone("grey", seed=2 + sx))
    hd = m.bone("head", bd, (0, 7.2, 0))
    pebble(m, hd, (0.3, 7.2, -0.2), 4.2, 3.6, 4.4, stone("brown", extra=middle_face, seed=1))
    pebble(m, hd, (-0.4, 11.4, 0.2), 3.3, 2.8, 3.2, stone("olive", extra=olive_face, seed=3))
    pebble(m, hd, (0.3, 14.4, 0.1), 2.2, 1.9, 2.4, stone("grey", seed=4))
    pebble(m, hd, (-0.2, 16.6, 0.2), 1.5, 1.3, 2.0, stone("grey_dark", seed=5))
    return m
