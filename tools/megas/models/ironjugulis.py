"""Mega Iron Jugulis, hand-built from boxes in Cobblemon's style.

Iron Jugulis (official art: a future Hydreigon robot: a black body on a long neck with a blue-visored head, two arms
ending in pink spiky "heads" with blue sensor lights, long black spider-leg wings, a pink-and-blue segmented tail) as a
mega: its pink spike rings grow and glow, its wings sharpen into blades and its visor and sensors glow.

Front is -z, y is up. ~40 units tall; baseScale 1.0 (about 2.5 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.0
HITBOX = [2.6, 2.6]
LOOK = ("a black robot Hydreigon with a glowing blue visor, glowing pink spike rings round its arm-heads, long black "
        "blade wings and a pink-and-blue segmented tail")
KIND = "floater"

BASE = {"black": (36, 36, 50), "black_light": (66, 66, 86), "pink": (240, 80, 170), "pink_light": (255, 140, 210),
        "blue": (70, 140, 230), "glow": (120, 220, 255)}
SHINY = {"pink": (250, 190, 60), "pink_light": (255, 230, 120), "blue": (230, 80, 90), "glow": (255, 120, 120)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def black(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["black_light"] if face == "up" else P["black"]


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("north", "east", "west") and 33.5 <= y <= 35 and z < -10:
        return P["glow"], P["glow"]
    return black(x, y, z, face, variant)


def pink(x, y, z, face, variant, **k):
    P = palette(variant)
    return (P["pink_light"] if face in ("up", "north") else P["pink"]), P["pink"]


def orb(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north":
        return P["glow"], P["glow"]
    return P["blue"]


def tailf(x, y, z, face, variant, r=0, **k):
    P = palette(variant)
    return P["pink"] if int(math.floor(z)) % 4 < 2 else P["blue"]


def build() -> Model:
    m = Model("ironjugulis_mega")
    root = m.bone("ironjugulis_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 20, 0))
    m.round_box(body, 0, 0, 5, 4, 14, 24, black, cut=2)
    hd = m.bone("head", body, (0, 24, -2))
    chain(m, hd, [(0, 23, -2), (0, 29, -6), (0, 33, -9)], [3, 3], black)
    m.box(hd, -3, 31, -15, 3, 37, -8, headf)
    for ang in (-40, 0, 40):
        a = math.radians(ang)
        spike(m, hd, (2 * math.sin(a), 36.5, -11), (math.sin(a) * 0.6, 1, 0.5), 2, 5, pink)

    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 5, 22, 0))
        chain(m, arm, [(sgn * 5, 22, 0), (sgn * 10, 19, -3), (sgn * 13, 16, -7)], [3, 2], black)
        m.box(arm, sgn * 13 - 2.5, 13.5, -10, sgn * 13 + 2.5, 18.5, -5, orb)
        for n in range(8):                                # the glowing spike ring
            a = 2 * math.pi * n / 8
            d = (math.cos(a), math.sin(a), -0.15)
            spike(m, arm, (sgn * 13 + 2 * math.cos(a), 16 + 2 * math.sin(a), -7.5), d, 2, 5, pink)

    for sgn, side in ((1, "left"), (-1, "right")):
        wb = m.bone(f"wing_{side}", body, (sgn * 4, 23, 2))
        for n, (dy, length) in enumerate(((6, 22), (2, 26), (-3, 20))):
            chain(m, wb, [(sgn * 4, 23, 2), (sgn * 12, 23 + dy + 4, 4), (sgn * (8 + length), 23 + dy, 6)], [2, 1.5], black)

    tl = m.bone("tail", body, (0, 14, 2))
    chain(m, tl, [(0, 14, 2), (0, 9, 4), (0, 5, 8), (0, 3, 13), (0, 3, 18)], [4, 3, 3, 2], tailf)
    return m
