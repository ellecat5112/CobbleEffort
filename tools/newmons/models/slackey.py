"""Slackey, the Lounge Ape Pokémon (Water/Fighting), Splakey evolved, after the art of the A. Fakemon fanpage (the
art's own name): a huge, idle ape lounging in a dark blue and white swim ring, its light blue chest striped with white
ribs, its back dark blue, its big orange hands lazily raised. Its small head has a heavy orange brow over half-closed,
bored eyes, an orange muzzle with stubby fangs and a slab of dark blue hair; water drips off it everywhere.

Shiny: teal-green with golden hands and face.

Front is -z, y is up. 29 units tall; baseScale 0.92 (1.7 m). It floats in its ring.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _splashmonkey import P, solid

SCALE = 0.92
HITBOX = [2.0, 1.8]
KIND = "floater"
K = 3
HEIGHT = 29
LOOK = ("a huge idle ape lounging in a dark blue and white swim ring, a white-ribbed chest, big orange hands, a heavy "
        "orange brow over bored eyes and a slab of dark blue hair")


def ringf(x, y, z, face, variant, **k):
    p = P(variant)
    a = math.atan2(x, z)
    return tone(p["white"] if (a * 2 / math.pi + 0.25) % 1.0 < 0.4 else p["blue_dark"], face), None


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for yy in (12.0, 14.4, 16.8):
            if abs(y - yy - abs(x) * 0.2) < 0.4 and 1.0 < abs(x) < 4.6:
                return p["white"], None                                       # white ribs
        return tone(p["blue_light"], face), None
    return tone(p["blue_dark"] if face in ("south", "up") else p["blue"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.5, y - 24.2
            if abs(dx) < 0.85 and -0.4 < dy < 0.2:
                return (p["pupil"] if abs(dx) < 0.3 else p["red_eye"] if dy > -0.1 else p["white"]), None
        return tone(p["orange_light"], face), None
    return tone(p["orange"], face), None


def build() -> Model:
    m = Model("slackey")
    top = m.bone("slackey", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    pts = [(9.0 * math.sin(2 * math.pi * i / 16), 5.0, 9.0 * math.cos(2 * math.pi * i / 16) + 1.0) for i in range(17)]
    for a, b in zip(pts, pts[1:]):
        rod(m, bd, a, b, 6.0, ringf, extend=0.8, t2=5.0)                       # the swim ring
    m.round_box(bd, 0, 1.0, 7.0, 5.0, 6.0, 20.0, chestf, cut=2.2)              # the big body
    for sx in (-1, 1):
        rod(m, bd, (sx * 3.0, 8.0, -2.0), (sx * 5.4, 7.0, -11.0), 3.4, solid("blue"), extend=0.6)   # legs over the ring
        m.round_box(bd, sx * 5.6, -12.0, 1.8, 1.8, 5.6, 8.4, solid("orange"), cut=0.6)              # feet
        spike(m, bd, (sx * 7.6, 3.0, 1.0), (0, -1, 0), 1.2, 2.0, solid("white"))                    # drips

    hd = m.bone("head", bd, (0, 20, 0))
    m.round_box(hd, 0, 0.0, 3.6, 3.2, 19.6, 26.4, headf, cut=1.2)
    m.box(hd, -3.8, 24.6, -4.2, 3.8, 26.0, -2.8, solid("orange"))               # its heavy brow
    m.box(hd, -2.0, 20.0, -4.6, 2.0, 22.8, -2.8, solid("orange"))               # muzzle
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.2, 22.0, -4.4), (0, 1, -0.2), 0.9, 1.4, solid("white"))   # stubby fangs
    m.box(hd, -3.4, 26.0, -3.0, 3.4, 29.0, 2.0, solid("blue_dark"), rotation=(-15, 0, 0), pivot=(0, 26, 0))

    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 7.0, 17.0, 0))
        if sx < 0:                                                              # one arm resting on the ring
            rod(m, ar, (-7.0, 17.0, 0.0), (-10.0, 12.0, -4.0), 3.2, solid("blue"), extend=0.6)
            rod(m, ar, (-10.0, 12.0, -4.0), (-9.0, 11.0, -9.0), 3.0, solid("blue"), extend=0.6)
            m.round_box(ar, -9.0, -10.4, 2.0, 2.0, 9.6, 12.4, solid("orange"), cut=0.8)
        else:                                                                   # the other lazily raised
            rod(m, ar, (7.0, 17.0, 0.0), (11.0, 18.0, -4.0), 3.2, solid("blue"), extend=0.6)
            rod(m, ar, (11.0, 18.0, -4.0), (12.0, 22.0, -7.0), 3.0, solid("blue_light"), extend=0.6)
            m.round_box(ar, 12.4, -8.0, 2.4, 1.8, 21.6, 25.0, solid("orange"), cut=0.8)
    return m
