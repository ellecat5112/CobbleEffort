"""Wolfevel, the Rebel Wolf Pokémon (Grass), Wigwoof evolved, after the art of the A. Fakemon fanpage (the art's own
name): a scrappy green werewolf standing on two legs with a wild orange mane of hair, red eyes and fangs, a collar of
spiky orange fur, orange-to-brown spiky cuffs on its arms, green fists with red claws, a vine with leaves round its
waist, huge feet with white claws and a long spiky tail running orange to red.

Shiny: slate-blue with a violet mane.

Front is -z, y is up. 30 units tall to the top of its hair; baseScale 0.7 (1.3 m).
"""
from __future__ import annotations

import math

from _afake import round_eye
from _boxmodel import Model, rod, spike
from _route import tone
from _wolfpup import P, ramp, solid

SCALE = 0.7
HITBOX = [1.1, 1.85]
KIND = "biped"
K = 4
HEIGHT = 30
LOOK = ("a scrappy green werewolf on two legs with a wild orange mane, red eyes, fangs, spiky orange fur cuffs, green "
        "fists with red claws, a leafy vine belt, huge clawed feet and a spiky orange-to-red tail")


def torsof(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.0 and y < 19:
        return tone(p["green_light"], face), None                            # its paler chest and belly
    return tone(p["green"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.5, y - 25.0
            if dy > 0.5 - dx * sx * 0.35 and abs(dx) < 1.2 and dy < 1.0:
                return p["green_dark"], None                                 # a scowling brow
            e = round_eye(dx, dy, 1.0, p, "red", ry=0.85, iris_frac=0.8)
            if e:
                return e, None
    return tone(p["green"], face), None


def snoutf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and y > 23.2 and abs(x) < 0.9:
        return p["nose"], None
    return tone(p["green_light"], face), None


def vinef(x, y, z, face, variant, **k):
    p = P(variant)
    a = math.atan2(x, z)
    if face in ("north", "south", "east", "west") and (a * 3) % 2.1 < 0.5:
        return p["vine"], None                                               # leaves along the vine
    return tone(p["nose"], face), None


def build() -> Model:
    m = Model("wolfevel")
    top = m.bone("wolfevel", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0.6, 3.6, 2.8, 12.0, 21.0, torsof, cut=1.2)
    m.round_box(bd, 0, 0.6, 3.9, 3.1, 13.0, 14.2, vinef, cut=1.2)              # the vine round its waist
    for i in range(7):                                                         # its collar of spiky orange fur
        a = math.pi * (i / 6.0) - math.pi / 2
        spike(m, bd, (3.0 * math.sin(a), 20.4, -2.0 * math.cos(a) + 0.6), (math.sin(a), 0.5, -0.6 * math.cos(a)),
              1.8, 2.6, solid("orange"))

    hd = m.bone("head", bd, (0, 21, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.0, 21.0, 27.0, headf, cut=1.0)
    m.box(hd, -1.6, 21.4, -6.2, 1.6, 24.2, -3.4, snoutf)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.0, 21.6, -5.8), (0, -1, -0.1), 0.9, 1.4, solid("white"))       # fangs
    m.box(hd, -3.8, 26.0, -4.4, 3.8, 29.0, 3.6, solid("orange"))               # its wild mane of hair
    for x, z, d in ((-2.4, -1, (-0.4, 1, 0.5)), (0, 0, (0, 1, 0.7)), (2.4, -1, (0.4, 1, 0.5)), (-1.2, 2.5, (-0.2, 0.6, 1)),
                    (1.4, 2.5, (0.3, 0.6, 1)), (3.6, 1, (1, 0.5, 0.2)), (-3.6, 1, (-1, 0.5, 0.2))):
        spike(m, hd, (x, 28.4, z), d, 2.0, 3.0, solid("orange_dark"), tip=1.0)
    for x in (-2.6, -0.6, 1.6):                                                # its fringe
        spike(m, hd, (x, 26.6, -4.2), (0, -1, -0.5), 1.8, 2.2, solid("orange"))

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 2.6, 13, 1))
        rod(m, lb, (sx * 2.6, 13.0, 1.0), (sx * 3.4, 7.0, -1.0), 3.4, solid("green"), extend=0.6)
        rod(m, lb, (sx * 3.4, 7.0, -1.0), (sx * 3.6, 2.4, 0.4), 3.0, solid("green"), extend=0.6)
        m.round_box(lb, sx * 3.6, -1.0, 2.2, 3.2, 0.0, 3.0, solid("green_dark"), cut=0.8)   # huge feet
        for dx in (-1.2, 0.0, 1.2):
            spike(m, lb, (sx * 3.6 + dx, 1.0, -4.0), (0, -0.2, -1), 1.0, 1.6, solid("claw"))
        spike(m, lb, (sx * 3.6, 6.0, 0.4), (sx * 1, 0.2, 0.4), 1.6, 2.2, solid("green_dark"))   # leafy tufts

        ar = m.bone(f"arm_{side}", bd, (sx * 3.8, 20, 0))                       # fists up like a brawler
        rod(m, ar, (sx * 3.8, 20.0, 0.0), (sx * 7.0, 16.5, -2.0), 2.4, solid("green"), extend=0.5)
        rod(m, ar, (sx * 7.0, 16.5, -2.0), (sx * 8.6, 19.4, -6.0), 2.4, ramp("orange", "orange_dark"), extend=0.5)
        spike(m, ar, (sx * 7.8, 18.0, -3.6), (sx * 1, 0.3, 0.3), 1.8, 3.0, solid("orange"), tip=0.9)
        spike(m, ar, (sx * 7.0, 16.6, -2.0), (sx * 0.6, -0.7, 0.6), 1.8, 2.6, solid("orange_dark"))
        m.round_box(ar, sx * 8.8, -6.8, 1.6, 1.6, 18.8, 21.8, solid("green"), cut=0.6)       # its fist
        for dy in (-0.9, 0.3, 1.5):
            spike(m, ar, (sx * 8.8, 19.6 + dy * 0.8, -8.2), (0, 0.3, -1), 0.9, 1.4, solid("claw_red"))

    tl = m.bone("tail", bd, (0, 14, 3))
    rod(m, tl, (0, 14.0, 2.6), (0, 12.6, 11.0), 3.0, ramp("orange", "red"), extend=0.4, t2=2.6)
    for i, z in enumerate((5.0, 7.6, 10.2)):                                   # its spiky edge
        spike(m, tl, (0, 14.0 - z * 0.12, z), (0, 1, 0.5), 1.4, 2.0 + i * 0.4, solid("orange_dark" if i < 2 else "red"))
    spike(m, tl, (0, 12.6, 10.8), (0, 0.1, 1), 2.2, 2.6, solid("red"), tip=1.0)
    return m
