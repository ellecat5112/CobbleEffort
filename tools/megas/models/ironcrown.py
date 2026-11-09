"""Mega Iron Crown, hand-built from boxes in Cobblemon's style.

Iron Crown (official art: a future Cobalion robot: a teal body with grey joints, a head with two great yellow crest
blades like antlers floating above it, white tufts, four long legs with grey hooves) as a mega: the crest-blades
spread into a crown of floating glowing swords round its head.

Front is -z, y is up. ~44 units tall; baseScale 1.2 (about 3.3 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.2
HITBOX = [2.2, 3.2]
LOOK = ("a teal robot Cobalion with grey joints and white tufts, its crest-blades spread into a crown of floating "
        "glowing golden swords round its head")
KIND = "quadruped"

BASE = {"teal": (50, 170, 180), "teal_light": (90, 206, 212), "teal_dark": (30, 120, 130), "grey": (180, 186, 196),
        "white": (240, 244, 248), "gold": (250, 220, 90), "eye": (255, 120, 60)}
SHINY = {"teal": (190, 190, 200), "teal_light": (220, 220, 230), "teal_dark": (140, 140, 150), "gold": (120, 230, 255)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def teal(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["teal_dark"] if face == "down" else (P["teal_light"] if face == "up" else P["teal"])


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and 30.5 <= y <= 32 and -16 <= z <= -14:
        return P["eye"], P["eye"]
    return teal(x, y, z, face, variant)


def gold(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["gold"], P["gold"]


def grey(x, y, z, face, variant, **k):
    return palette(variant)["grey"]


def white(x, y, z, face, variant, **k):
    return palette(variant)["white"]


def build() -> Model:
    m = Model("ironcrown_mega")
    root = m.bone("ironcrown_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 20, 2))
    m.box(body, -4, 16, -7, 4, 24, 10, teal)
    m.box(body, -4.5, 21, -8, 4.5, 25, -3, white)        # a white tuft at the chest
    hd = m.bone("head", body, (0, 24, -6))
    chain(m, hd, [(0, 23, -6), (0, 28, -9)], [4], teal)
    m.box(hd, -3, 27, -18, 3, 33, -9, headf)
    # the crown: golden swords floating in a ring above and around the head
    for n in range(7):
        a = math.radians(-90 + n * 30)
        px, pz = 7 * math.cos(a), -13 + 5 * math.sin(a)
        chain(m, hd, [(px, 34, pz), (px * 1.15, 40, pz), (px * 1.2, 44, pz + 1)], [2, 1.5], gold)
    chain(m, hd, [(0, 33, -14), (0, 38, -16), (0, 42, -15)], [2, 1.5], gold)

    for nm, (lx, lz) in (("leg_front_left", (3, -5)), ("leg_front_right", (-3, -5)),
                         ("leg_back_left", (3, 8)), ("leg_back_right", (-3, 8))):
        leg = m.bone(nm, root, (lx, 17, lz))
        m.box(leg, lx - 1.5, 9, lz - 1.5, lx + 1.5, 17, lz + 1.5, teal)
        m.box(leg, lx - 1, 7, lz - 1, lx + 1, 9, lz + 1, grey)
        m.box(leg, lx - 1, 2, lz - 1, lx + 1, 7, lz + 1, teal)
        m.box(leg, lx - 2, 0, lz - 2, lx + 2, 2, lz + 1.5, grey)
    tl = m.bone("tail", body, (0, 21, 10))
    chain(m, tl, [(0, 21, 10), (0, 19, 15), (0, 15, 18)], [2, 1.5], white)
    return m
