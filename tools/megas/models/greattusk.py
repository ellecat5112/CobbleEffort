"""Mega Great Tusk, hand-built from boxes in Cobblemon's style.

Great Tusk (official art: an ancient Donphan with dark navy armour plates over a shaggy pale-blue body, a yellow eye,
a fanged mouth under a long armoured trunk, huge ivory tusks curling up and back, crimson spikes along the back and
red fur round its feet) as a mega: heavier armour with glowing crimson seams, a ridge of crimson crystals from head
to tail tip, a second pair of short tusks, and great double-curled main tusks.

Front is -z, y is up. ~34 units tall; baseScale 1.5 (about 3.2 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix, spike

SCALE = 1.5
HITBOX = [3.4, 3.2]
LOOK = "heavy navy armour with glowing crimson seams over shaggy pale-blue fur, crimson crystals from head to tail, red fur cuffs, ivory claws and great double-curled tusks"
KIND = "quadruped"

BASE = {
    "armour": (58, 54, 104), "armour_light": (84, 80, 140), "armour_dark": (40, 36, 76), "seam": (226, 52, 92),
    "fur": (158, 182, 214), "fur_light": (192, 210, 232), "fur_dark": (122, 146, 184),
    "crystal": (220, 44, 92), "crystal_light": (246, 104, 140), "tuft": (214, 70, 90),
    "ivory": (238, 230, 204), "ivory_dark": (210, 198, 166),
    "eye": (250, 210, 40), "pupil": (30, 20, 20), "mouth": (110, 30, 50), "tooth": (252, 252, 244),
}
SHINY = {"armour": (54, 98, 70), "armour_light": (78, 130, 96), "armour_dark": (36, 70, 50), "seam": (250, 190, 60),
         "crystal": (250, 170, 40), "crystal_light": (255, 214, 110), "tuft": (240, 160, 50),
         "fur": (204, 196, 170), "fur_light": (226, 220, 200), "fur_dark": (170, 160, 132)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def armour(x, y, z, face, variant, **k):
    """Armour plates: a lighter top edge per plate row and thin glowing crimson seams between plates."""
    P = palette(variant)
    if face == "down":
        return P["armour_dark"]
    if face == "up":
        if int(math.floor(z)) % 9 == 4 and abs(x) > 3:
            return P["seam"], P["seam"]
        return P["armour_light"] if abs(x) < 2 else P["armour"]
    along = z if face in ("east", "west") else x
    if face in ("east", "west") and int(math.floor(along)) % 9 == 4 and k.get("r", 0) > 0:
        return P["seam"], P["seam"]
    return P["armour_light"] if k.get("r", 9) == 0 else P["armour"]


def fur(x, y, z, face, variant, **k):
    """Shaggy pale-blue fur: a jagged darker fringe at the bottom."""
    P = palette(variant)
    if face == "down":
        return P["fur_dark"]
    rows = k.get("rows", 1)
    r = k.get("r", 0)
    if face != "up" and r >= rows - 2 and (int(x + z) % 3 == 0 or r == rows - 1):
        return P["fur_dark"]
    return P["fur_light"] if r == 0 else P["fur"]


def head_armour(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and -18 <= z <= -14.5 and 15 <= y <= 17.6:
        if abs(z + 16.2) < 0.6:
            return P["pupil"], (40, 30, 10)
        return P["eye"], P["eye"]
    if face in ("east", "west") and -18.5 <= z <= -14 and 17.6 < y <= 18.6:
        return P["armour_dark"]                           # a heavy brow
    return armour(x, y, z, face, variant, **k)


def jaw(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("north", "up") and y > 9.2:
        return P["mouth"]
    return fur(x, y, z, face, variant, **k)


def crystal(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["crystal_light"] if face in ("up", "north", "west") else P["crystal"]


def tuft(x, y, z, face, variant, **k):
    P = palette(variant)
    rows = k.get("rows", 1)
    if face != "up" and k.get("r", 0) == rows - 1 and k.get("c", 0) % 2:
        return (0, 0, 0, 0)
    return P["tuft"]


def ivory(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["ivory_dark"] if face in ("down", "east") else P["ivory"]


def tooth(x, y, z, face, variant, **k):
    return palette(variant)["tooth"]


def build() -> Model:
    m = Model("greattusk_mega")
    root = m.bone("greattusk_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 14, 2))

    # body: shaggy fur underneath, armour shell on top, a hump over the shoulders
    m.box(body, -9, 6, -9, 9, 16, 15, fur)
    m.box(body, -10, 14, -10, 10, 21, 16, armour)
    m.box(body, -8, 21, -8, 8, 24, 10, armour)
    m.box(body, -6, 24, -6, 6, 26, 4, armour)
    # crimson crystals along the back, big in the middle
    for z, h in ((-7, 6), (-2, 9), (3, 10), (8, 8), (13, 6)):
        y = 26 if -6 <= z <= 4 else (24 if z < 10 else 21)
        spike(m, body, (0, y - 0.5, z), (0, 1, 0.6), 4, h, crystal, tip=2)
    for z in (-4, 5, 12):
        for sgn in (1, -1):
            spike(m, body, (sgn * 7, 21 - 0.5 if z < 10 else 20.5, z), (sgn * 0.7, 1, 0.5), 3, 5, crystal, tip=1)

    # head: armoured, with a long trunk curling down, a fanged jaw, eyes on the sides
    head = m.bone("head", body, (0, 16, -9))
    m.box(head, -7, 10, -20, 7, 21, -8, head_armour)
    m.box(head, -5, 8, -25, 5, 16, -19, armour)
    m.box(head, -4, 4, -28, 4, 10, -23, armour)
    m.box(head, -3, 1, -29, 3, 5, -25, armour)
    m.box(head, -6, 6, -18, 6, 10, -9, jaw)
    for x in (-4.5, -2.5, 1.5, 3.5):
        m.box(head, x, 8, -19.5, x + 1, 10, -18.5, tooth)
    for z, h in ((-17, 5), (-12, 6)):
        spike(m, head, (0, 20.5, z), (0, 1, 0.5), 3, h, crystal, tip=1)
    # tusks: great double-curled ivory arcs, and a short second pair
    for sgn in (1, -1):
        pts = [(sgn * 6, 10, -16), (sgn * 9, 6, -21), (sgn * 11, 4, -28), (sgn * 12, 6, -34), (sgn * 12, 11, -38),
               (sgn * 11, 17, -39), (sgn * 10, 22, -37), (sgn * 9, 25, -33), (sgn * 8.5, 25, -29)]
        chain(m, head, pts, [5, 5, 4, 4, 4, 3, 3, 2], ivory)
        chain(m, head, [(sgn * 5, 9, -21), (sgn * 7, 5, -25), (sgn * 8, 4, -29)], [3, 2], ivory)

    # legs: stout, armoured, with red fur cuffs and ivory claws
    for nm, (lx, lz) in (("leg_front_left", (7, -5)), ("leg_front_right", (-7, -5)),
                         ("leg_back_left", (7, 10)), ("leg_back_right", (-7, 10))):
        leg = m.bone(nm, root, (lx, 10, lz))
        m.box(leg, lx - 3, 3, lz - 3, lx + 3, 10, lz + 3, armour)
        m.box(leg, lx - 4, 1, lz - 4, lx + 4, 4, lz + 4, tuft)
        m.box(leg, lx - 3.5, 0, lz - 3.5, lx + 3.5, 1, lz + 3.5, fur)
        for cx in (-2.5, -0.5, 1.5):
            m.box(leg, lx + cx, 0, lz - 5, lx + cx + 1, 2, lz - 3.5, ivory)

    # tail: armoured, tapering, with crystals
    tail = m.bone("tail", body, (0, 16, 15))
    chain(m, tail, [(0, 17, 15), (0, 16, 22), (0, 14, 29), (0, 13, 35)], [8, 6, 4], armour)
    for z in (20, 27, 33):
        spike(m, tail, (0, 20 if z < 25 else 16.5, z), (0, 1, 0.7), 2, 4, crystal)
    return m
