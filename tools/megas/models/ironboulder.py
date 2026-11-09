"""Mega Iron Boulder, hand-built from boxes in Cobblemon's style.

Iron Boulder (official art: a future Terrakion robot: a big round dark-grey torso ringed with orange glowing armour,
a helmet-like head with two cat-ear points and a curved blade-horn on its brow, grey limbs with orange rings, sturdy
legs) as a mega: its blade-horn grows long and glows white-hot, and its armour thickens into a moving fortress with
more glowing orange rings.

Front is -z, y is up. ~34 units tall; baseScale 1.3 (about 2.8 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.3
HITBOX = [2.4, 2.8]
LOOK = ("a sturdy robot Terrakion: a round dark torso ringed with glowing orange armour, a helmeted head with cat-ear "
        "points, a long white-hot blade-horn and grey legs with glowing orange rings")
KIND = "quadruped"

BASE = {"dark": (60, 58, 62), "dark_light": (86, 84, 90), "grey": (170, 172, 178), "grey_dark": (130, 132, 140),
        "orange": (250, 160, 40), "hot": (255, 250, 220), "eye": (255, 180, 60)}
SHINY = {"dark": (60, 70, 100), "dark_light": (86, 96, 130), "orange": (90, 220, 255), "hot": (220, 250, 255)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def torso(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west", "north") and int(math.floor(z if face != "north" else x)) % 7 == 0:
        return P["orange"], P["orange"]                  # glowing armour bands
    return P["dark_light"] if face == "up" else P["dark"]


def grey(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["grey_dark"] if face == "down" else P["grey"]


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and 22.5 <= y <= 24 and 1 <= abs(x) <= 3:
        return P["eye"], P["eye"]
    return P["dark"] if y > 25 else grey(x, y, z, face, variant)


def hot(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["hot"], P["orange"]


def ring(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["orange"], P["orange"]


def build() -> Model:
    m = Model("ironboulder_mega")
    root = m.bone("ironboulder_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 17, 2))
    m.round_box(body, 0, 2, 8, 10, 10, 26, torso, cut=3)
    for sgn in (1, -1):
        m.box(body, sgn * 8.5 - 1, 16, -6, sgn * 8.5 + 1, 19, 10, ring)      # a glowing armour band
    hd = m.bone("head", body, (0, 20, -9))
    m.box(hd, -4.5, 18, -15, 4.5, 27, -7, headf)
    for sgn in (1, -1):                                   # cat-ear points
        spike(m, hd, (sgn * 3, 26.5, -10), (sgn * 0.3, 1, 0.3), 3, 5, grey)
    chain(m, hd, [(0, 25, -14), (0, 28, -19), (0, 33, -21), (0, 38, -20)], [3, 2, 2], hot)   # the white-hot blade-horn

    for nm, (lx, lz) in (("leg_front_left", (6, -5)), ("leg_front_right", (-6, -5)),
                         ("leg_back_left", (6, 9)), ("leg_back_right", (-6, 9))):
        leg = m.bone(nm, root, (lx, 11, lz))
        m.box(leg, lx - 2, 3, lz - 2, lx + 2, 11, lz + 2, grey)
        m.box(leg, lx - 2.5, 4, lz - 2.5, lx + 2.5, 6, lz + 2.5, ring)
        m.box(leg, lx - 2.5, 0, lz - 3, lx + 2.5, 3, lz + 2.5, grey)
    return m
