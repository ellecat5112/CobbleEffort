"""Mega Slither Wing, hand-built from boxes in Cobblemon's style.

Slither Wing (official art: an ancient Volcarona that crawls: a big white fluffy body, three pairs of red wings that
blaze orange and yellow towards their flame-shaped tips with green diamond spots, a red armoured head with a dark
face and a yellow eye, a teal fuzzy tail end, little dark legs) as a mega: six huge blazing wings with glowing tips
and glowing green diamonds, a bigger fluffy collar, a red horned head-crest and taller flame wings.

Front is -z, y is up. ~38 units tall with the wings; baseScale 1.6 (about 3.8 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix, spike

SCALE = 1.6
HITBOX = [3.0, 3.6]
LOOK = "six blazing flame wings with glowing yellow tips and glowing green diamonds, a big white fluffy collar, a red horned head with one yellow eye, a teal tail and little dark legs"
KIND = "quadruped"
ANIM = {"wing_flap": 8, "leg_amp": 16}

BASE = {
    "fluff": (246, 244, 240), "fluff_shade": (220, 218, 214), "fluff_dark": (196, 194, 190),
    "red": (220, 52, 40), "orange": (246, 132, 40), "yellow": (252, 214, 70), "diamond": (120, 220, 90),
    "head": (206, 44, 40), "head_dark": (150, 30, 30), "face": (40, 46, 80), "eye": (252, 210, 50), "pupil": (40, 30, 20),
    "tail": (60, 170, 150), "tail_dark": (40, 130, 116), "leg": (50, 50, 66),
}
SHINY = {"red": (90, 150, 230), "orange": (120, 200, 240), "yellow": (200, 240, 255), "diamond": (250, 160, 220),
         "head": (70, 120, 210), "head_dark": (50, 80, 160), "tail": (230, 140, 190), "tail_dark": (200, 100, 160)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def fluff(x, y, z, face, variant, r=0, rows=1, c=0, **k):
    """White fluff with a tufted lower edge."""
    P = palette(variant)
    if face == "down":
        return P["fluff_dark"]
    if face != "up" and r == rows - 1 and c % 2:
        return (0, 0, 0, 0)
    return P["fluff"] if r < rows // 2 else P["fluff_shade"]


def wing(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, box=None, **k):
    """A flame wing: red at the root blazing to orange and yellow at its flame-shaped (cut) tip; glowing green
    diamonds; the brightest part glows."""
    P = palette(variant)
    t = r / max(1, rows - 1)                           # 0 at the top (tip), 1 at the root
    width = cols * (0.35 + 0.65 * t)                   # the wing narrows to a flame point at the top
    if abs(c - (cols - 1) / 2) > width / 2:
        return (0, 0, 0, 0)
    if (r % 5 == 2) and abs(c - (cols - 1) / 2) < 1.0 and 0.25 < t < 0.85:
        return P["diamond"], P["diamond"]
    if t < 0.22:
        return P["yellow"], P["yellow"]
    if t < 0.5:
        return P["orange"]
    return P["red"]


def head(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north":
        if 9 <= y <= 13 and abs(x) <= 2.6:              # the dark face
            if 10.6 <= y <= 12.4 and abs(x - 1.0) <= 0.9:
                return P["eye"], P["eye"]              # one big yellow eye, off-centre like Slither Wing's
            if 10.6 <= y <= 12.4 and abs(x + 1.4) <= 0.6:
                return P["pupil"]
            return P["face"]
    if face == "down":
        return P["head_dark"]
    return P["head"]


def horn(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["head"] if face in ("up", "north") else P["head_dark"]


def tail(x, y, z, face, variant, r=0, **k):
    P = palette(variant)
    return P["tail_dark"] if face == "down" or r % 3 == 2 else P["tail"]


def leg(x, y, z, face, variant, **k):
    return palette(variant)["leg"]


def build() -> Model:
    m = Model("slitherwing_mega")
    root = m.bone("slitherwing_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 9, 2))
    # the big fluffy body and collar
    m.round_box(body, 0, 2, 9, 11, 3, 15, fluff, cut=3)
    m.round_box(body, 0, -6, 11, 6, 6, 17, fluff, cut=3)            # the collar, bigger than the body
    m.round_box(body, 0, 2, 7, 9, 15, 18, fluff, cut=3)

    # the head: red armour, a dark face with one big eye, a horned crest
    hd = m.bone("head", body, (0, 11, -11))
    m.box(hd, -4, 7, -18, 4, 15, -11, head)
    m.box(hd, -3, 5, -17, 3, 7, -12, head)
    for sgn in (1, -1):
        chain(m, hd, [(sgn * 3, 14, -15), (sgn * 5, 18, -14), (sgn * 6, 21, -11)], [3, 2], horn)
    chain(m, hd, [(0, 14.5, -16), (0, 19, -16), (0, 22, -14)], [3, 2], horn)

    # six flame wings: three each side, rising and spreading
    for sgn, side in ((1, "left"), (-1, "right")):
        wb = m.bone(f"wing_{side}", body, (sgn * 4, 17, 2))
        for n, (zc, h, w, spread) in enumerate(((-3, 22, 10, 18), (3, 26, 12, 30), (9, 20, 10, 44))):
            x0 = sgn * 4
            m.box(wb, x0 - w / 2, 16, zc, x0 + w / 2, 16 + h, zc, wing,
                  rotation=(-10 + n * 12, sgn * (8 + n * 8), sgn * -spread), pivot=(x0, 16, zc))

    # the teal fuzzy tail end
    tl = m.bone("tail", body, (0, 9, 13))
    chain(m, tl, [(0, 9, 13), (0, 8, 19), (0, 6, 24)], [7, 5], tail)

    # little dark legs: three pairs
    for nm, (lx, lz) in (("leg_front_left", (6, -6)), ("leg_front_right", (-6, -6)), ("leg_mid_left", (7, 1)),
                         ("leg_mid_right", (-7, 1)), ("leg_back_left", (6, 8)), ("leg_back_right", (-6, 8))):
        lb = m.bone(nm, root, (lx, 5, lz))
        m.box(lb, lx - 1, 0, lz - 1, lx + 1, 5, lz + 1, leg)
        m.box(lb, lx - 1, 0, lz - 3, lx + 1, 1, lz - 1, leg)
    return m
