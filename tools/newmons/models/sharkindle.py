"""Sharkindle, the Land Shark Pokémon (Steel/Fire), CobbleEffort's pseudo-legendary, built from boxes from the user's
design.

A red and black land shark on four stubby legs: a pointed black snout with a toothy grin and sharp yellow eyes, red
cheeks and flanks, a dark-grey striped dorsal fin, glowing orange fins at its shoulders and a row of glowing orange
spots on its head, a grey tail fin, and black legs with grey claws.

Front is -z, y is up. 15 units tall to its fin; baseScale 0.72 (0.7 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, mix
from _landshark import P, fin, solid, teeth_band
from _route import tone

SCALE = 0.72
HITBOX = [0.7, 0.6]
KIND = "quadruped"
K = 5
HEIGHT = 15
LOOK = ("a red and black land shark on four stubby legs with a toothy grin, sharp yellow eyes, a striped grey dorsal "
        "fin and glowing orange shoulder fins")

TEETH = teeth_band(7.4, 6.4, 0.7)


def head(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and abs(z + 6.8) < 1.0 and abs(y - 9.6) < 0.7:   # sharp yellow eyes
        if abs(z + 6.8) < 0.35 and abs(y - 9.6) < 0.45:
            return (20, 18, 20), None
        return p["eye"], p["eye"]
    if face in ("east", "west", "north"):
        u = z if face != "north" else x
        if 6.3 < y < 7.6:
            return (p["tooth"] if TEETH(u, y) else (60, 14, 20)), None   # the toothy grin
    if face == "up" and abs(x) < 1.2 and any(abs(z - zc) < 0.4 for zc in (-4.5, -3.3, -2.1)):
        return p["orange"], p["orange"]                                 # glowing orange spots
    if y < 7.6 or (face in ("east", "west") and y < 9.0 and z > -6):
        return tone(p["red"], face), None
    return tone(p["black"], face), None


def body(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down" or y < 6.5:
        return tone(p["red"], face), None
    if face in ("east", "west") and y < 8.5:
        return tone(p["red"], face), None
    return tone(p["grey"] if y > 10 else p["black"], face), None


DORSAL = fin([(-1.5, 10.5), (1.0, 15), (3.0, 14.6), (4.5, 10.5)], "zy", "grey", False)


def dorsal(x, y, z, face, variant, **k):
    c, g = DORSAL(x, y, z, face, variant)
    if len(c) == 4 and c[3] == 0:
        return c, g
    p = P(variant)
    return (p["grey_light"] if int(z * 1.2) % 2 else p["grey"]), None


def build() -> Model:
    m = Model("sharkindle")
    top = m.bone("sharkindle", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 1.5, 4, 5, 4, 11, body, cut=2)                     # torso
    hd = m.bone("head", bd, (0, 8, -3))
    m.round_box(hd, 0, -5.5, 3.5, 3, 5.5, 11, head, cut=1)                 # head
    m.round_box(hd, 0, -9, 2.5, 1.5, 6.2, 10, head, cut=1)                 # pointed snout
    m.box(bd, 0, 10.5, -1.5, 0, 15, 4.5, dorsal)                           # the striped dorsal fin
    for sx in (-1, 1):                                                      # glowing orange shoulder fins
        m.box(bd, sx * 4, 4, -3, sx * 4, 8, 2, fin([(-3, 7.5), (2, 6.5), (1.5, 4)], "zy"),
              rotation=(0, 0, sx * -30), pivot=(sx * 4, 7, 0))
    tail = m.bone("tail", bd, (0, 7.5, 6))
    chain(m, tail, [(0, 7.5, 6), (0, 8, 9.5), (0, 8.5, 12)], [3, 2], body)
    m.box(tail, 0, 5, 11, 0, 13, 16, fin([(11.5, 8.5), (15.5, 12.8), (14.0, 8.6), (15.5, 5.2)], "zy", "grey", False))
    for nm, (lx, lz) in (("leg_front_left", (-2.6, -2)), ("leg_front_right", (2.6, -2)),
                         ("leg_back_left", (-2.6, 4)), ("leg_back_right", (2.6, 4))):
        lg = m.bone(nm, top, (lx, 4.5, lz))
        m.box(lg, lx - 1.2, 1, lz - 1.2, lx + 1.2, 5, lz + 1.2, solid("black"))
        m.box(lg, lx - 1.4, 0, lz - 1.8, lx + 1.4, 1, lz + 1.2, solid("grey_light"))
    return m
