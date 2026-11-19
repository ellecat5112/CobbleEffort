"""Disc Rotom (Electric/Ice), after the user's Rotom doodle sheet (artist not named): Rotom inside a portable CD
player. A round grey player with a shining disc in its tray and its teal lid flipped up; on the lid are Rotom's
pink lens eyes and a W-shaped grin. Pale blue plasma chills the air round it.

Front is -z, y is up. 18 units tall; about 0.7 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _rotomform import bolt_plane, disc_z, palette, rotom_eye, solid
from _route import tone

P = palette({"aura": (110, 200, 250), "aura_light": (220, 245, 255), "iris": (240, 120, 200), "teal": (40, 140, 170),
             "teal_light": (90, 190, 210)})
HEIGHT = 18
SCALE = round(0.7 * 16 / HEIGHT, 3)
HITBOX = [0.9, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = "a round portable CD player with its teal lid up, pink lens eyes and a W-shaped grin on the lid"


def lid(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = rotom_eye(x - 2.2 * sx, y - 11.6, 1.5, p)
            if e:
                return e
        if 7.6 <= y <= 9.2 and abs(x) <= 2.2:              # a W-shaped grin
            u = abs(x) % 1.1
            if abs((y - 7.6) - abs(u - 0.55) * 2.6) < 0.45:
                return p["black"], None
        return (p["teal_light"] if math.hypot(x, y - 10) > 5.6 else p["orange"]), None
    return tone(p["teal"], face), None


def tray(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        d = math.hypot(x, z + 0.5)
        if d < 0.8:
            return p["black"], None
        if d < 4.8:
            return ((p["white"] if (math.atan2(z, x) * 2) % 3 < 0.8 else p["grey_light"]), p["aura_light"])
    return tone(p["grey"], face), None


def build() -> Model:
    m = Model("rotom_disc")
    top = m.bone("rotom_disc", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, -0.5, 6.2, 6.2, 0, 3.4, tray, cut=1.9)                         # the player and its disc
    hd = m.bone("head", bd, (0, 3, 5))
    disc_z(m, hd, 0, 10, 4, 6, 6.6, lid)                                              # the flipped-up lid
    for x, y, z, w, h, pl, fl in [(-10, 4, -2, 4, 6, "xy", False), (7, 9, -1, 4, 6, "xy", True)]:
        bolt_plane(m, bd, x, y, z, w, h, P, plane=pl, flip=fl)
    return m
