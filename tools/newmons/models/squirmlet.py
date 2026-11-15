"""Squirmlet, the Velvet Worm Pokémon (Bug; after the art of the user's friend on r/fakemon, signed "sno", shared with
permission; our name): a tiny chubby grey worm on stubby orange-toed legs, an orange ring across its back, an orange hood
with a big round eye disc on each side, a blue face and a short cyan snout drooping like a hose.

Front is -z, y is up. 10 units tall; baseScale 0.5 (0.3 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _velvet import P, eye_disc, jelly, solid, toes
from _route import tone

SCALE = 0.5
HITBOX = [0.9, 0.7]
KIND = "quadruped"
K = 8
HEIGHT = 10
LOOK = ("a tiny chubby grey worm on stubby orange-toed legs, an orange back ring, an orange hood with big round eye discs, "
        "a blue face and a short cyan snout drooping like a hose")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return tone(p["grey_dark"], face), None
    if 1.0 < z < 2.6:
        return tone(p["orange"], face), None                          # the orange ring
    return tone(p["grey"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye_disc(p, z + 2.2, y - 6.8, 1.35)
        if c is not None:
            return c, None
    if face == "north" and y < 6.6 and abs(x) < 1.8:
        return tone(p["blue"], face), None                            # the blue face
    if face == "down":
        return tone(p["blue_dark"], face), None
    return tone(p["orange"] if y > 5.6 else p["blue"], face), None


def build() -> Model:
    m = Model("squirmlet")
    top = m.bone("squirmlet", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 1))
    m.round_box(bd, 0, 1.6, 2.6, 2.8, 1.2, 5.2, bodyf, cut=1.0)        # the chubby body
    m.round_box(bd, 0, 4.4, 1.6, 1.4, 1.8, 4.2, bodyf, cut=0.6)        # its stubby tail end
    hd = m.bone("head", bd, (0, 5, -1))
    m.round_box(hd, 0, -1.8, 2.4, 2.2, 4.2, 9.0, headf, cut=0.8)
    m.box(hd, -1.0, 4.4, -4.6, 1.0, 6.0, -3.8, solid("blue"))           # the snout
    rod(m, hd, (0, 5.2, -4.4), (0, 3.4, -6.0), 1.2, jelly, extend=0.2)  # a short cyan hose, drooping
    for leg, (lx, lz) in (("leg_front_left", (1.8, -0.4)), ("leg_front_right", (-1.8, -0.4)),
                          ("leg_back_left", (1.8, 3.4)), ("leg_back_right", (-1.8, 3.4))):
        lg = m.bone(leg, top, (lx, 2, lz))
        m.box(lg, lx - 0.9, 0.5, lz - 0.9, lx + 0.9, 2.2, lz + 0.9, solid("grey"))
        toes(m, lg, lx, 0, lz - 0.4, 2, 0.8, 0.9, 0.8, key="orange")
    return m
