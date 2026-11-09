"""Mega Miraidon, hand-built from boxes in Cobblemon's style.

Miraidon (official art: a future dragon: a dark purple-blue body traced with glowing yellow and cyan lines, a head
with a glowing visor-like crest and two lightning antennae, round wheel-like hips, clawed limbs and a long tail
ending in a lightning tip) as a mega: its body fins flare into wings of light (glowing yellow and cyan), and its
lightning antennae crackle larger.

Front is -z, y is up. ~42 units tall; baseScale 1.3 (about 3.4 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.3
HITBOX = [2.6, 3.4]
LOOK = ("a dark purple robot dragon traced with glowing yellow and cyan lines, wings of light flaring from its back, "
        "crackling lightning antennae and a long tail with a lightning tip")
KIND = "biped"

BASE = {"purple": (70, 60, 150), "purple_light": (100, 90, 190), "purple_dark": (44, 36, 100), "yellow": (250, 230, 90),
        "cyan": (100, 220, 250), "black": (30, 30, 40), "white": (240, 240, 250)}
SHINY = {"purple": (150, 60, 100), "purple_light": (190, 90, 130), "purple_dark": (100, 36, 70), "yellow": (130, 250, 200),
         "cyan": (255, 170, 230)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def purple(x, y, z, face, variant, **k):
    """Dark purple with glowing yellow lines along it."""
    P = palette(variant)
    if face in ("east", "west", "up") and int(math.floor(y * 0.7 + z * 0.5)) % 7 == 0:
        return P["yellow"], P["yellow"]
    return P["purple_dark"] if face == "down" else (P["purple_light"] if face == "up" else P["purple"])


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("north", "east", "west") and 34 <= y <= 35.5:
        return P["cyan"], P["cyan"]                     # the glowing visor
    return purple(x, y, z, face, variant)


def light(colour):
    def s(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
        P = palette(variant)
        if r > rows - 1 - int(abs(math.sin(c * 0.7)) * 3):
            return (0, 0, 0, 0)                          # a ragged trailing edge
        return P[colour], P[colour]
    return s


def bolt(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["yellow"], P["yellow"]


def white(x, y, z, face, variant, **k):
    return palette(variant)["white"]


def build() -> Model:
    m = Model("miraidon_mega")
    root = m.bone("miraidon_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 18, 0))
    m.box(body, -5, 13, -5, 5, 27, 5, purple)
    for sgn in (1, -1):                                  # round wheel-like hips
        m.round_box(body, sgn * 6, 1, 1.5, 4, 11, 19, purple, cut=1)
    hd = m.bone("head", body, (0, 27, -2))
    chain(m, hd, [(0, 27, -2), (0, 31, -5)], [4], purple)
    m.box(hd, -3, 30, -13, 3, 37, -4, headf)
    for sgn in (1, -1):                                  # lightning antennae
        chain(m, hd, [(sgn * 2, 36.5, -8), (sgn * 5, 41, -6), (sgn * 3, 43, -3), (sgn * 7, 47, -1)], [1, 1, 1], bolt)

    for sgn, side in ((1, "left"), (-1, "right")):
        wb = m.bone(f"wing_{side}", body, (sgn * 5, 25, 3))
        for n, (col, ang, length) in enumerate((("yellow", 30, 18), ("cyan", 5, 22), ("yellow", -20, 16))):
            x0 = sgn * 5
            m.box(wb, x0 if sgn > 0 else x0 - length, 21, 4 + n * 2, x0 + length if sgn > 0 else x0, 27, 4 + n * 2,
                  light(col), rotation=(0, sgn * -20, sgn * ang), pivot=(x0, 24, 4 + n * 2))

    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 5, 25, -2))
        chain(m, arm, [(sgn * 5, 25, -2), (sgn * 8, 20, -4), (sgn * 8, 15, -7)], [3, 3], purple)
        for dx in (-1, 0.5):
            m.box(arm, sgn * 8 + dx, 13, -9, sgn * 8 + dx + 1, 15, -7, white)
    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 6, 12, 1))
        chain(m, leg, [(sgn * 6, 12, 1), (sgn * 6, 6, -1), (sgn * 6, 2, 1)], [4, 3], purple)
        m.box(leg, sgn * 6 - 2.5, 0, -3, sgn * 6 + 2.5, 2, 3, purple)

    tl = m.bone("tail", body, (0, 15, 5))
    chain(m, tl, [(0, 15, 5), (0, 11, 12), (0, 7, 19), (0, 6, 27), (0, 8, 34)], [4, 3, 3, 2], purple)
    chain(m, tl, [(0, 8, 34), (2, 11, 37), (-1, 13, 40), (1, 16, 43)], [1, 1, 1], bolt)
    return m
