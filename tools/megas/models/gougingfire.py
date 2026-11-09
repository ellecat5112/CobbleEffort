"""Mega Gouging Fire, hand-built from boxes in Cobblemon's style.

Gouging Fire (official art: an ancient Entei: a stocky brown four-legged beast with shaggy fur, black anklets, a red
face mask with white fangs, a grey smoke-plume mane, and a huge golden crest of curved spikes striped red and green)
as a mega: its golden crest becomes a blazing crown whose tips glow like fire, glowing magma cracks run through its
fur and its smoke mane billows larger.

Front is -z, y is up. ~42 units tall; baseScale 1.5 (about 3.9 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.5
HITBOX = [3.0, 3.8]
LOOK = ("a stocky brown beast with glowing magma cracks in its fur, black anklets, a red face mask with white fangs, "
        "a billowing grey smoke mane and a huge golden crest of curved spikes with glowing fiery tips")
KIND = "quadruped"

BASE = {
    "brown": (140, 86, 46), "brown_light": (170, 112, 64), "brown_dark": (104, 60, 32), "magma": (255, 120, 40),
    "black": (34, 30, 30), "red": (200, 40, 36), "gold": (236, 200, 80), "gold_dark": (200, 160, 50), "stripe_r": (190, 50, 40),
    "stripe_g": (60, 130, 60), "fire": (255, 200, 70), "smoke": (196, 196, 200), "smoke_dark": (160, 160, 168),
    "fang": (250, 250, 246), "eye": (250, 220, 70),
}
SHINY = {"brown": (180, 160, 120), "brown_light": (210, 190, 150), "brown_dark": (140, 120, 90), "gold": (200, 210, 230),
         "gold_dark": (160, 170, 200), "magma": (120, 200, 255), "fire": (170, 230, 255), "red": (60, 90, 170)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def fur(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west", "up") and (int(math.floor(z * 0.8 + y)) % 9 == 0):
        return P["magma"], P["magma"]                   # glowing magma cracks
    return P["brown_dark"] if face == "down" else (P["brown_light"] if face == "up" else P["brown"])


def mask(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west", "north") and 25.5 <= y <= 27 and (face != "north" or abs(abs(x) - 2.5) < 1):
        return P["eye"], P["eye"]
    return P["red"]


def gold(x, y, z, face, variant, r=0, rows=1, **k):
    """A crest spike: gold striped red and green, glowing fiery at the tip."""
    P = palette(variant)
    if r <= 1 and face != "down":
        return P["fire"], P["fire"]
    if r == rows - 3:
        return P["stripe_r"]                           # one red and one green band near the base
    if r == rows - 2:
        return P["stripe_g"]
    return P["gold"] if face in ("up", "north", "west") else P["gold_dark"]


def smoke(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["smoke"] if face in ("up", "north") else P["smoke_dark"]


def black(x, y, z, face, variant, **k):
    return palette(variant)["black"]


def fang(x, y, z, face, variant, **k):
    return palette(variant)["fang"]


def build() -> Model:
    m = Model("gougingfire_mega")
    root = m.bone("gougingfire_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 16, 2))
    m.box(body, -7, 10, -9, 7, 22, 13, fur)
    m.box(body, -8, 14, -11, 8, 24, -2, fur)              # shaggy shoulders
    # billowing smoke mane down the back
    for z0, y0, r in ((0, 25, 5), (6, 25, 6), (12, 23, 5), (17, 20, 4)):
        m.round_box(body, 0, z0, r, r - 1, y0 - 2, y0 + 2, smoke, cut=2)

    hd = m.bone("head", body, (0, 22, -10))
    m.box(hd, -5, 20, -21, 5, 29, -11, fur)
    m.box(hd, -4.5, 22, -22, 4.5, 28, -19, mask)
    m.box(hd, -3, 18, -24, 3, 22, -19, mask)
    for sgn in (1, -1):
        m.box(hd, sgn * 2 - 0.5, 16, -23, sgn * 2 + 0.5, 18, -22, fang)
    # the crown: curved golden spikes rising and sweeping back, glowing at the tips
    for ang, h in ((-60, 12), (-35, 16), (-12, 19), (12, 19), (35, 16), (60, 12)):
        a = math.radians(ang)
        base = (4.5 * math.sin(a), 28.5, -15 - 2 * math.cos(a))
        mid = (base[0] + math.sin(a) * 4, base[1] + h * 0.55, base[2] + 3)
        tip = (mid[0] + math.sin(a) * 3, mid[1] + h * 0.35, mid[2] + 7)
        chain(m, hd, [base, mid, tip], [4, 3], gold)
    for sgn in (1, -1):
        chain(m, hd, [(sgn * 5, 24, -14), (sgn * 10, 26, -12), (sgn * 13, 30, -8)], [3, 2], gold)

    for nm, (lx, lz) in (("leg_front_left", (5.5, -6)), ("leg_front_right", (-5.5, -6)),
                         ("leg_back_left", (5.5, 10)), ("leg_back_right", (-5.5, 10))):
        leg = m.bone(nm, root, (lx, 12, lz))
        m.box(leg, lx - 2.5, 2, lz - 2.5, lx + 2.5, 12, lz + 2.5, fur)
        m.box(leg, lx - 3, 3, lz - 3, lx + 3, 5, lz + 3, black)      # anklets
        m.box(leg, lx - 3, 0, lz - 3.5, lx + 3, 2, lz + 2.5, fur)
        for dx in (-2, 0, 2):
            m.box(leg, lx + dx - 0.5, 0, lz - 5, lx + dx + 0.5, 1.5, lz - 3.5, fang)

    tl = m.bone("tail", body, (0, 19, 13))
    for sgn in (0, 1, -1):
        chain(m, tl, [(sgn * 2, 19, 13), (sgn * 4, 23, 18), (sgn * 6, 25, 22)], [3, 2], smoke)
    return m
