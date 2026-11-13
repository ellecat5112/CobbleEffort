"""Ovarupa, the Horn Pupa Pokémon (Bug/Dragon), Larvorub evolved, after the art by @artworks218_ (the art's own name,
used with the creator's permission): a round orange pupa with a dark brown base, a seam round its middle, two pale
yellow infinity marks on its front and lavender spots on its sides. A jagged orange collar opens at the top round its
dark brown head, whose green eyes have figure-eight pupils; a great curved brown horn with a barb grows out of the top,
and two smaller horns with yellow tips out of the sides.

Shiny: a teal pupa with a navy head and pink eyes.

Front is -z, y is up. 33 units tall to the tip of its horn; baseScale 0.5 (1.0 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _scarab import P, horn, lemniscate, solid

SCALE = 0.5
HITBOX = [1.1, 2.0]
KIND = "quadruped"
K = 3
HEIGHT = 33
LOOK = ("a round orange pupa with a dark base, pale yellow infinity marks and lavender spots, a jagged collar round its "
        "brown head, green eyes, a great barbed horn on top and two yellow-tipped side horns")

SPOTS = [((8.4, 8.6, -1.0), 2.4), ((-8.4, 8.6, -1.0), 2.4), ((7.0, 3.6, 3.0), 1.8), ((-7.0, 3.6, 3.0), 1.8),
         ((0.0, 8.0, 8.4), 2.3), ((4.6, 10.4, 6.6), 1.6), ((-4.6, 10.4, 6.6), 1.6)]


def shellf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down" or y < 2.2:
        return tone(p["brown"], face), None                                   # the dark base
    if face != "up" and abs(y - 6.0) < 0.28:
        return p["orange_dark"], None                                         # the seam round its middle
    if face == "north" and z < -4:
        if lemniscate(x, y - 9.4, 4.6) or lemniscate(x, y - 3.8, 3.2):
            return tone(p["mark"], face), None                                # pale infinity marks
    for c, r in SPOTS:
        if math.dist((x, y, z), c) < r:
            return tone(p["lavender"], face), None
    return tone(p["orange_light"] if face == "up" else p["orange"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 2.1, y - 15.6
            if (dx / 1.45) ** 2 + (dy / 1.05) ** 2 < 1:
                # a figure-eight pupil: two dark lobes on a slant
                for o in (-1, 1):
                    if math.hypot(dx - o * 0.45 * sx, dy + o * 0.3) < 0.42:
                        return p["eye_dark"], None
                return (p["eye_light"] if dy > 0.55 else p["eye"]), None
    return tone(p["brown"], face), None


def build() -> Model:
    m = Model("ovarupa")
    top = m.bone("ovarupa", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for y0 in range(0, 15):                                                    # the round pupa, slice by slice
        ym = y0 + 0.5
        r = round(17 * math.sqrt(max(0.0, 1 - ((ym - 7.5) / 7.6) ** 2))) / 2     # whole sizes: symmetric steps
        if r < 1:
            continue
        m.round_box(bd, 0, 0, r, r, y0, y0 + 1, shellf, cut=max(1, round(r * 0.32)))
    for i in range(9):                                                         # the jagged collar round its head
        a = 2 * math.pi * (i + 0.5) / 9
        front = math.cos(a) > 0.6
        spike(m, bd, (6.0 * math.sin(a), 12.6, -6.0 * math.cos(a)), (0.5 * math.sin(a), 1, -0.5 * math.cos(a)),
              2.4, 2.6 if front else 4.2, solid("orange"), tip=1.2)

    hd = m.bone("head", bd, (0, 14, 0))
    m.round_box(hd, 0, -0.4, 4.6, 4.3, 11.6, 18.6, headf, cut=1.6)            # dark brown head
    for a, b, t in (((0, 17.5, -1.0), (0, 24.5, -1.6), 4.0), ((0, 24.0, -1.6), (0, 29.5, -0.8), 3.0),
                    ((0, 29.0, -0.8), (0, 33.0, 0.8), 2.0)):
        rod(m, hd, a, b, t, solid("brown"), extend=1.2)                        # the great curved horn
    spike(m, hd, (1.2, 26.6, -1.2), (1, 0.45, 0), 2.0, 4.0, solid("brown"), tip=1.0)   # its barb
    for sx in (-1, 1):
        horn(m, hd, (sx * 4.0, 16.6, -0.6), (sx * 6.4, 19.4, -0.6), (sx * 8.6, 23.6, -1.2), 2.2, 1.6)
    return m
