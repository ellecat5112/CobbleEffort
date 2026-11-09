"""Mega Iron Valiant, hand-built from boxes in Cobblemon's style.

Iron Valiant (official art: a future Mega Gardevoir / Mega Gallade hybrid: a white and green body, a green crest swept
up from its head, a red eye, a white chest with a pink fin, long white blade arms edged in pink, a flowing green
gown of blades and white legs) as a mega: its blades lengthen into a flowing cape of glowing pink-edged blades, and
its head crest grows into a tall glowing blade.

Front is -z, y is up. ~40 units tall; baseScale 1.1 (about 2.75 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.1
HITBOX = [1.6, 2.7]
LOOK = ("a white and green robot knight with a tall glowing green crest-blade, a red eye, long white arm-blades edged "
        "in glowing pink and a flowing cape of green blades")
KIND = "biped"

BASE = {"white": (244, 244, 248), "white_dark": (210, 212, 222), "green": (80, 170, 90), "green_light": (120, 206, 120),
        "green_dark": (50, 120, 64), "pink": (250, 100, 170), "red": (230, 40, 70), "black": (40, 40, 50)}
SHINY = {"green": (80, 120, 210), "green_light": (120, 160, 240), "green_dark": (50, 80, 170), "pink": (250, 200, 80)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def white(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["white_dark"] if face == "down" else P["white"]


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and 31.5 <= y <= 33 and 0.6 <= x <= 2.2:
        return P["red"], P["red"]
    return white(x, y, z, face, variant)


def chest(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and abs(x) <= 1 and 20 <= y <= 25:
        return P["pink"], P["pink"]
    return white(x, y, z, face, variant)


def blade(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
    """A long white blade, its edges glowing pink."""
    P = palette(variant)
    if c == 0 or c == cols - 1 or r == rows - 1:
        return P["pink"], P["pink"]
    return P["white"]


def gown(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
    P = palette(variant)
    if c == cols - 1 and r > rows // 3:
        return P["pink"], P["pink"]
    return P["green_light"] if r < rows // 3 else P["green"]


def green(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["green_light"] if face in ("up", "north") else P["green"]


def build() -> Model:
    m = Model("ironvaliant_mega")
    root = m.bone("ironvaliant_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 20, 0))
    m.box(body, -3, 16, -2, 3, 27, 2, chest)
    m.box(body, -2, 13, -1.5, 2, 16, 1.5, white)
    m.round_box(body, 0, 0, 4, 3, 8, 15, green, cut=1)                   # a green gown at the hips
    # the cape: green blades fanning out behind and to the sides
    for n, ang in enumerate((-50, -25, 0, 25, 50)):
        m.box(body, -2.5, 3, 2, 2.5, 26, 2, gown, rotation=(-12, ang, 0), pivot=(0, 26, 2))
    hd = m.bone("head", body, (0, 27, 0))
    m.box(hd, -2.5, 27, -3, 2.5, 34, 2, headf)
    chain(m, hd, [(0, 33, -1), (0, 38, 1), (0, 42, 4), (0, 43, 8)], [3, 2, 2], green)       # the crest-blade
    spike(m, hd, (2, 32, 0), (1, 0.6, 0.4), 2, 5, green)

    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 3.5, 26, 0))
        chain(m, arm, [(sgn * 3.5, 26, 0), (sgn * 5, 21, -1)], [2], white)
        m.box(arm, sgn * 5 - 2, 4, -2, sgn * 5 + 2, 22, -2, blade, rotation=(-10, 0, sgn * 8), pivot=(sgn * 5, 22, -2))

    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 1.5, 13, 0))
        m.box(leg, sgn * 1.5 - 1, 1, -1, sgn * 1.5 + 1, 13, 1, white)
        m.box(leg, sgn * 1.5 - 1, 0, -3, sgn * 1.5 + 1, 1, 1, white)
    return m
