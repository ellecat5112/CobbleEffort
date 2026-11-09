"""Mega Walking Wake, hand-built from boxes in Cobblemon's style.

Walking Wake (official art: an ancient Suicune: a teal four-legged dragon with a big purple mane streaked with red and
orange, a teal head with a large crest, white muzzle and claws, white whiskers, and a long white whip of a tail with
teal markings) as a mega: the mane surges higher like a breaking wave with glowing flame streaks, the crest grows
into a tall fin and the tail streams out in two ribbons.

Front is -z, y is up. ~40 units tall; baseScale 1.35 (about 3.4 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.35
HITBOX = [2.6, 3.3]
LOOK = ("a teal four-legged dragon with a purple mane surging up like a breaking wave, glowing red and orange flame "
        "streaks, a tall teal crest fin, white muzzle, whiskers and claws, and a long white tail streaming in two ribbons")
KIND = "quadruped"

BASE = {
    "teal": (60, 176, 170), "teal_light": (96, 206, 196), "teal_dark": (40, 130, 128), "purple": (128, 76, 176),
    "purple_dark": (96, 52, 140), "flame_red": (236, 70, 50), "flame_orange": (250, 150, 50), "white": (240, 244, 246),
    "white_dark": (206, 214, 220), "eye": (220, 40, 50), "mouth": (130, 40, 50),
}
SHINY = {"teal": (90, 140, 210), "teal_light": (130, 176, 236), "teal_dark": (60, 100, 170), "purple": (60, 150, 120),
         "purple_dark": (40, 110, 90), "flame_red": (250, 210, 70), "flame_orange": (255, 240, 140)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def teal(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["teal_dark"] if face == "down" else (P["teal_light"] if face == "up" else P["teal"])


def head(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and 25.5 <= y <= 27 and -23 <= z <= -21:
        return P["eye"], P["eye"]
    return teal(x, y, z, face, variant)


def muzzle(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and 21.4 <= y <= 22.2:
        return P["mouth"]
    return P["white_dark"] if face == "down" else P["white"]


def mane(x, y, z, face, variant, **k):
    """Purple with glowing flame streaks running back and up."""
    P = palette(variant)
    t = int(math.floor(y * 0.9 - z * 0.45 + abs(x) * 0.3))
    if face in ("east", "west", "up") and t % 12 == 0:
        return P["flame_red"], P["flame_red"]
    if face in ("east", "west", "up") and t % 12 == 1:
        return P["flame_orange"], P["flame_orange"]
    return P["purple_dark"] if face == "down" else P["purple"]


def white(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["white_dark"] if face == "down" else P["white"]


def tail(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("up", "east", "west") and int(math.floor(z)) % 5 == 0:
        return P["teal"]                                 # teal markings
    return white(x, y, z, face, variant)


def build() -> Model:
    m = Model("walkingwake_mega")
    root = m.bone("walkingwake_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 16, 2))
    m.box(body, -6, 11, -10, 6, 21, 14, teal)
    # the surging mane over the shoulders and back
    manb = m.bone("mane", body, (0, 20, -4))
    m.box(manb, -9, 14, -14, 9, 26, 4, mane)
    m.box(manb, -8, 26, -12, 8, 32, 2, mane)
    m.box(manb, -6, 32, -9, 6, 36, 0, mane)
    for z0, h in ((-4, 9), (2, 7), (7, 5)):
        spike(m, manb, (0, 30 if z0 < 0 else 24, z0), (0, 1, 0.9), 6, h, mane, tip=3)
    for sgn in (1, -1):
        for z0 in (-10, -4, 2):
            spike(m, manb, (sgn * 8.5, 20, z0), (sgn * 0.8, 0.6, 0.6), 4, 6, mane, tip=2)

    hd = m.bone("head", body, (0, 22, -12))
    m.box(hd, -4, 22, -25, 4, 29, -16, head)
    m.box(hd, -3, 19, -29, 3, 24, -24, muzzle)
    # the tall crest fin and white whiskers
    chain(m, hd, [(0, 28.5, -22), (0, 34, -21), (0, 39, -17), (0, 40, -12)], [4, 3, 2], teal)
    for sgn in (1, -1):
        spike(m, hd, (sgn * 3.5, 28, -20), (sgn * 0.4, 1, 0.5), 3, 6, teal, tip=1)
        chain(m, hd, [(sgn * 3, 20.5, -27), (sgn * 8, 19, -26), (sgn * 12, 16, -23)], [1, 1], white)

    for nm, (lx, lz) in (("leg_front_left", (5, -6)), ("leg_front_right", (-5, -6)),
                         ("leg_back_left", (5, 10)), ("leg_back_right", (-5, 10))):
        leg = m.bone(nm, root, (lx, 13, lz))
        m.box(leg, lx - 2, 2, lz - 2, lx + 2, 13, lz + 2, teal)
        m.box(leg, lx - 2.5, 0, lz - 3, lx + 2.5, 2, lz + 2, teal)
        for dx in (-1.5, 0.5):
            m.box(leg, lx + dx, 0, lz - 4.5, lx + dx + 1, 1, lz - 3, white)

    tl = m.bone("tail", body, (0, 18, 14))
    for sgn in (1, -1):                                   # two streaming ribbons
        chain(m, tl, [(sgn * 1.5, 18, 14), (sgn * 3, 24, 22), (sgn * 4, 30, 30), (sgn * 6, 32, 38), (sgn * 9, 29, 44)],
              [3, 3, 2, 2], tail)
    return m
