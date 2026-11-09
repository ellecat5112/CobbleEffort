"""Mega Raging Bolt, hand-built from boxes in Cobblemon's style.

Raging Bolt (official art: an ancient Raikou: a long-necked yellow four-legged dragon with black stripes, a white neck
and belly, red-and-blue feet, a teal tail ending in a spiky crystal ball, and a purple storm cloud floating on its
head like a broad hat) as a mega: the cloud swells into a towering thunderhead crackling with glowing lightning, and
the tail's crystal ball grows bigger and glows.

Front is -z, y is up. ~50 units tall; baseScale 1.6 (about 5 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.6
HITBOX = [3.0, 5.0]
LOOK = ("a long-necked yellow dragon striped black with a white neck and belly, red-and-blue feet, a towering purple "
        "thunderhead crackling with glowing lightning on its head, and a big glowing crystal ball on its teal tail")
KIND = "quadruped"

BASE = {
    "yellow": (246, 200, 56), "yellow_light": (255, 222, 100), "yellow_dark": (210, 160, 40), "stripe": (36, 32, 36),
    "white": (244, 244, 246), "white_dark": (210, 210, 218), "red": (220, 50, 50), "blue": (60, 110, 220),
    "cloud": (150, 130, 200), "cloud_light": (186, 170, 226), "cloud_dark": (110, 92, 160), "bolt": (255, 240, 110),
    "teal": (70, 180, 190), "crystal": (150, 240, 250), "eye": (240, 60, 60),
}
SHINY = {"yellow": (240, 140, 60), "yellow_light": (255, 176, 100), "yellow_dark": (200, 110, 40), "cloud": (90, 100, 120),
         "cloud_light": (130, 140, 160), "cloud_dark": (60, 66, 84), "bolt": (140, 230, 255), "crystal": (255, 190, 240)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def yellow(x, y, z, face, variant, **k):
    """Yellow with black tiger stripes down the sides and back."""
    P = palette(variant)
    if face == "down":
        return P["white_dark"]
    if face in ("east", "west", "up") and int(math.floor(z + y * 0.4)) % 6 == 0:
        return P["stripe"]
    return P["yellow_light"] if face == "up" else P["yellow"]


def neck(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("north", "down"):
        return P["white"]                                # the white front of the neck
    return yellow(x, y, z, face, variant)


def head(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and 38.5 <= y <= 40 and -21.5 <= z <= -19.5:
        return P["eye"], P["eye"]
    if face == "north":
        return P["white"]
    return yellow(x, y, z, face, variant)


def cloud(x, y, z, face, variant, **k):
    """The thunderhead: purple puffs with glowing lightning veins."""
    P = palette(variant)
    if face in ("east", "west", "north", "south") and int(math.floor(x * 1.3 - y * 2 + z * 0.7)) % 11 == 0:
        return P["bolt"], P["bolt"]
    return P["cloud_dark"] if face == "down" else (P["cloud_light"] if face == "up" else P["cloud"])


def bolt(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["bolt"], P["bolt"]


def foot(x, y, z, face, variant, box=None, **k):
    P = palette(variant)
    return P["red"] if box.lo[1] < 1 else P["blue"]


def teal(x, y, z, face, variant, **k):
    return palette(variant)["teal"]


def crystal(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["crystal"], P["crystal"]


def build() -> Model:
    m = Model("ragingbolt_mega")
    root = m.bone("ragingbolt_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 16, 4))
    m.box(body, -6, 11, -6, 6, 21, 14, yellow)
    # spiky teal ridge along the back
    for z in (-2, 3, 8, 13):
        spike(m, body, (0, 20.5, z), (0, 1, 0.6), 2, 4, teal)

    # the long neck and head (the head bone carries the neck, so it can sway)
    hd = m.bone("head", body, (0, 19, -5))
    chain(m, hd, [(0, 18, -5), (0, 26, -9), (0, 33, -13), (0, 38, -16)], [6, 5, 5], neck)
    m.box(hd, -3.5, 36, -23, 3.5, 42, -15, head)
    # the towering thunderhead, with lightning crackling down
    for r, y0, y1 in ((13, 44, 47), (12, 47, 50), (10, 50, 53), (7, 53, 55)):
        m.round_box(hd, 0, -17, r, r - 2, y0, y1, cloud, cut=max(2, r // 3))
    for (dx, dz) in ((-8, -12), (9, -20), (2, -26)):
        chain(m, hd, [(dx, 44, -17 + dz * 0.3), (dx + 2, 41, -18 + dz * 0.3), (dx, 38, -19 + dz * 0.3)], [1, 1], bolt)
    m.box(hd, -1.5, 42, -20, 1.5, 44, -16, head)

    for nm, (lx, lz) in (("leg_front_left", (5, -3)), ("leg_front_right", (-5, -3)),
                         ("leg_back_left", (5, 11)), ("leg_back_right", (-5, 11))):
        leg = m.bone(nm, root, (lx, 13, lz))
        m.box(leg, lx - 2, 3, lz - 2, lx + 2, 13, lz + 2, yellow)
        m.box(leg, lx - 2.5, 1, lz - 2.5, lx + 2.5, 3, lz + 2.5, foot)
        m.box(leg, lx - 2.5, 0, lz - 3.5, lx + 2.5, 1, lz + 2.5, foot)

    tl = m.bone("tail", body, (0, 17, 14))
    chain(m, tl, [(0, 17, 14), (0, 15, 21), (0, 14, 28), (0, 15, 34)], [4, 3, 3], teal)
    # the glowing spiky crystal ball
    m.box(tl, -2, 13, 33, 2, 17, 37, crystal)
    for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0.7, 0.7, 0.5), (-0.7, 0.7, 0.5), (0.7, -0.7, 0.5), (-0.7, -0.7, 0.5)):
        spike(m, tl, (0, 15, 35), d, 1, 5, crystal)
    return m
