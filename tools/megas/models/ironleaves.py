"""Mega Iron Leaves, hand-built from boxes in Cobblemon's style.

Iron Leaves (official art: a future Virizion robot: a green body with pink accents, a long blade-horn swept forward
from its head, leaf-blades at its shoulders, grey jointed segments and four long thin legs with pink-edged hooves) as
a mega: its blade-horn grows into a crest of glowing swords and its shoulder blades lengthen.

Front is -z, y is up. ~38 units tall; baseScale 1.2 (about 2.85 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.2
HITBOX = [2.2, 2.8]
LOOK = ("a green robot Virizion with pink accents, a crest of glowing sword-horns, long leaf-blades at its shoulders, "
        "grey joints and four long legs with pink-edged hooves")
KIND = "quadruped"

BASE = {"green": (80, 180, 80), "green_light": (120, 214, 110), "green_dark": (50, 130, 56), "pink": (240, 80, 130),
        "grey": (170, 176, 186), "black": (36, 36, 44), "glow": (190, 255, 160), "eye": (250, 220, 60)}
SHINY = {"green": (220, 180, 60), "green_light": (250, 210, 100), "green_dark": (170, 130, 40), "glow": (255, 230, 150)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def green(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["green_dark"] if face == "down" else (P["green_light"] if face == "up" else P["green"])


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and 27.5 <= y <= 29 and -15 <= z <= -13:
        return P["eye"], P["eye"]
    return green(x, y, z, face, variant)


def sword(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
    P = palette(variant)
    return (P["glow"] if face in ("up", "north", "west") else P["green_light"]), P["glow"]


def leaf(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
    P = palette(variant)
    if c == cols - 1:
        return P["pink"]
    return P["green_light"] if r < rows // 2 else P["green"]


def grey(x, y, z, face, variant, **k):
    return palette(variant)["grey"]


def hoof(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["pink"] if face != "down" else P["black"]


def build() -> Model:
    m = Model("ironleaves_mega")
    root = m.bone("ironleaves_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 20, 2))
    m.box(body, -4, 16, -7, 4, 23, 10, green)
    m.box(body, -3, 17, 10, 3, 21, 13, grey)
    for sgn in (1, -1):                                   # long leaf-blades at the shoulders
        m.box(body, sgn * 4, 16, -6, sgn * 4, 28, 4, leaf, rotation=(-35, 0, sgn * -20), pivot=(sgn * 4, 22, -2))

    hd = m.bone("head", body, (0, 23, -6))
    chain(m, hd, [(0, 22, -6), (0, 26, -9)], [3], grey)
    m.box(hd, -2.5, 25, -17, 2.5, 30, -9, headf)
    # the crest of glowing swords: one long forward blade and four sweeping back
    chain(m, hd, [(0, 29.5, -15), (0, 31, -22), (0, 31, -30)], [2, 1.5], sword)
    for sgn in (1, -1):
        for n, (dy, dz) in enumerate(((5, 8), (9, 11))):
            chain(m, hd, [(sgn * 1.5, 29.5, -11), (sgn * (3 + n * 2), 29.5 + dy * 0.6, -11 + dz * 0.5), (sgn * (4 + n * 3), 29.5 + dy, -11 + dz)], [2, 1.5], sword)

    for nm, (lx, lz) in (("leg_front_left", (3, -5)), ("leg_front_right", (-3, -5)),
                         ("leg_back_left", (3, 8)), ("leg_back_right", (-3, 8))):
        leg = m.bone(nm, root, (lx, 17, lz))
        m.box(leg, lx - 1.5, 9, lz - 1.5, lx + 1.5, 17, lz + 1.5, green)
        m.box(leg, lx - 1, 7, lz - 1, lx + 1, 9, lz + 1, grey)
        m.box(leg, lx - 1, 2, lz - 1, lx + 1, 7, lz + 1, green)
        m.box(leg, lx - 1.5, 0, lz - 2, lx + 1.5, 2, lz + 1.5, hoof)
    return m
