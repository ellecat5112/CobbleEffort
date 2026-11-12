"""Magmalodon, the Magma Shark Pokémon (Steel/Fire), CobbleEffort's pseudo-legendary, built from boxes from the user's
design.

A large, powerful land shark standing on beefy legs: a massive head with red brow ridges, glowing eyes and a huge
mouth (a jutting lower jaw lined with fangs, glowing like molten metal inside), smoke pouring from the back of its head
and hanging down its back like dreads, a black body striped with glowing orange lines behind a red chest plate, a tall
grey dorsal fin and orange fins on its shoulders and tail, beefy red-armoured arms and legs wrapped in flames, huge
white claws, and a thick tail with a fireball burning at its tip.

Front is -z, y is up. 40 units tall to its dorsal fin; baseScale 0.96 (2.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod
from _landshark import P, fin, flame, glow, smoke, solid, teeth_band
from _route import tone

SCALE = 0.96
HITBOX = [1.6, 2.4]
KIND = "biped"
K = 3
HEIGHT = 40
LOOK = ("a large, beefy land shark with a huge fanged mouth glowing inside, smoke hanging from its head like dreads, "
        "orange fins, red armour and flames wrapped round its arms and legs")


def torso(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 4.5 and 17 < y < 26:
        return tone(p["red"], face), None                               # the chest plate
    if face in ("east", "west", "south") and abs(math.sin(y * 0.55 + z * 0.3)) < 0.1:
        return p["orange"], p["orange"]                                 # glowing orange lines
    return tone(p["black"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 2.6, y - 31.0
            if (dx / 1.2) ** 2 + (dy / 0.5) ** 2 < 1:
                return p["orange"], p["orange"]                         # glowing slit eyes
    return tone(p["black"], face), None


def mouth(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        return p["flame_mid"], p["flame_mid"]                           # glowing like molten metal inside
    return tone(p["red_dark"], face), None


def claw(x, y, z, face, variant, **k):
    return tone(P(variant)["claw"], face), None


def build() -> Model:
    m = Model("magmalodon")
    top = m.bone("magmalodon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 15, 0))
    m.round_box(bd, 0, 1, 7, 6, 13, 28, torso, cut=2)
    m.box(bd, 0, 27, -2, 0, 40, 9, fin([(-2, 27), (2, 39.5), (6, 38.5), (9, 27)], "zy", "grey", False))   # dorsal fin
    for sx in (-1, 1):                                                       # orange shoulder fins
        m.box(bd, sx * 7, 22, -2, sx * 7, 32, 8, fin([(-2, 26), (8, 31.5), (4, 23)], "zy"),
              rotation=(0, sx * -25, 0), pivot=(sx * 7, 26, -2))
    hd = m.bone("head", bd, (0, 28, -3))
    m.round_box(hd, 0, -6, 6, 5.5, 27, 34, headf, cut=2)                    # massive head
    for sx in (-1, 1):                                                       # red brow ridges
        m.box(hd, sx * 2.6 - 2.2, 31.8, -11.8, sx * 2.6 + 2.2, 33.6, -9, solid("red"))
    m.box(hd, -4.8, 24.5, -11.4, 4.8, 27.2, -3, mouth)                       # inside the huge mouth
    for i in range(8):                                                       # upper fangs
        x = -4.5 + i * 1.3
        m.box(hd, x - 0.5, 25.4, -11.8, x + 0.5, 27.2, -10.8, claw)
    jaw = m.bone("jaw", hd, (0, 26, -3))
    m.round_box(jaw, 0, -7.5, 5.5, 5, 21, 25, solid("grey"), cut=2)          # the jutting lower jaw
    for i in range(7):                                                       # lower fangs
        x = -3.9 + i * 1.3
        m.box(jaw, x - 0.5, 24.6, -12.2, x + 0.5, 26.8, -11.2, claw)
    for i, sx in enumerate((-5.5, -4, -2.4, -0.8, 0.8, 2.4, 4, 5.5)):       # smoke pouring off its head like dreads
        wob = 0.9 * math.sin(i * 1.7)
        spread = 1.0 + 0.5 * (abs(sx) > 3)
        chain(m, hd, [(sx, 34.5, -2), (sx * 1.2 * spread + wob, 31, 2.5), (sx * 1.35 * spread - wob, 26, 6),
                      (sx * 1.45 * spread, 20, 8.5)], [2, 1.8, 1.5], smoke)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                     # beefy arms with flames
        a = m.bone(nm, bd, (sx * 7, 25, 0))
        m.round_box(a, sx * 8.5, 0, 3, 3, 21.5, 27, solid("red"), cut=1)     # shoulder
        rod(m, a, (sx * 9, 22, -0.5), (sx * 10, 15, -3), 3.5, solid("black"))
        m.box(a, sx * 11.6, 14, -6, sx * 11.6, 25, 1, flame("zy", 14, [(-4.5, 7), (-2.5, 10), (-0.5, 8)], 2.6))
        m.round_box(a, sx * 10, -3.6, 2.6, 2.6, 12, 16.5, solid("red"), cut=1)   # fist
        for dx in (-1.2, 0, 1.2):
            rod(m, a, (sx * 10 + dx, 12.5, -6), (sx * 10 + dx, 11, -8), 1, claw)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                     # beefy legs with flames
        lg = m.bone(nm, top, (sx * 4, 15, 1))
        m.round_box(lg, sx * 4.5, 1, 3.2, 3.2, 7, 15.5, solid("red"), cut=1)
        m.box(lg, sx * 4.5 - 2.6, 0, -2.5, sx * 4.5 + 2.6, 7.5, 3.5, solid("grey"))
        m.box(lg, sx * 7.4, 1, -3, sx * 7.4, 13, 5, flame("zy", 1, [(-1.5, 9), (1.0, 11), (3.5, 8)], 2.8))
        for dx in (-1.4, 0, 1.4):
            m.box(lg, sx * 4.5 + dx - 0.5, 0, -3.5, sx * 4.5 + dx + 0.5, 1, -2.5, claw)
    tail = m.bone("tail", bd, (0, 16, 6))
    chain(m, tail, [(0, 16, 6), (0, 13, 12), (0, 11, 18)], [5, 3.5], solid("grey"))
    m.box(tail, 0, 9, 13, 0, 17, 18, fin([(13, 12.5), (17.5, 16.5), (16, 12)], "zy"))                    # orange tail fin
    m.round_box(tail, 0, 19.5, 1.5, 1.5, 10, 13, glow("flame_mid"), cut=0.5)                              # fireball
    m.box(tail, 0, 11.5, 18, 0, 18, 21, flame("zy", 11.5, [(19.5, 6.5)], 3.2))
    return m
