"""Lycanmoon, the Werewolf Pokémon (Grass/Fighting), Wolfevel evolved, after the art of the A. Fakemon fanpage (the
art's own name): a towering brown werewolf brawler with a long grinning snout, a shaggy mop of yellow hair tipped red,
a muscled chest marked with three green leaves, spiky yellow star-shaped pads on its shoulders and wrists, red-brown
fists, a green leafy loincloth, yellow spiky shin wraps and clawed feet, a tail like a red-orange flame, and a vine
lasso it swings in one hand.

Shiny: grey skin, silver hair, violet tips and a slate-blue loincloth.

Front is -z, y is up. 37 units tall to the top of its lasso; baseScale 0.75 (1.7 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _route import tone
from _wolfpup import P, ramp, solid

SCALE = 0.75
HITBOX = [1.4, 2.25]
KIND = "biped"
K = 3
HEIGHT = 37
LOOK = ("a towering brown werewolf brawler with a grinning snout, shaggy yellow hair, a leaf-marked chest, spiky yellow "
        "shoulder pads, red-brown fists, a green leafy loincloth, a flame-like tail and a vine lasso")


def torsof(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for cx, cy in ((-1.8, 23.6), (0.0, 22.6), (1.8, 23.6)):                # three green leaves on its chest
            if ((x - cx) / 0.6) ** 2 + ((y - cy) / 1.1) ** 2 < 1:
                return p["green_dark"], None
        if abs(y - 25.3) < 0.2 and abs(x) > 0.4:
            return p["brown_dark"], None                                       # the line of its chest
        if abs(x) < 0.15 and y < 21.5:
            return p["brown_dark"], None
    return tone(p["brown_light"] if face == "north" else p["brown"], face), None


def snoutf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    lo = box.lo[1]
    if face in ("east", "west", "north") and y < lo + 0.9:
        return p["mouth"], None                                                # its long grin
    return tone(p["brown"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.3, y - 31.0
            if (dx / 0.9) ** 2 + (dy / 0.45) ** 2 < 1:
                return (p["red"] if abs(dx) < 0.35 else p["white"]), None
    return tone(p["brown"], face), None


def build() -> Model:
    m = Model("lycanmoon")
    top = m.bone("lycanmoon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 17, 0))
    m.round_box(bd, 0, 0.0, 5.2, 3.4, 17.0, 27.0, torsof, cut=1.6)              # the muscled torso
    m.round_box(bd, 0, 0.0, 4.6, 3.4, 13.0, 17.6, solid("vine"), cut=1.4)       # the green loincloth
    for x in (-3.2, -1.0, 1.2, 3.4):                                           # its leafy hem
        spike(m, bd, (x, 13.2, -3.2), (0, -1, -0.15), 2.0, 3.0 + (abs(x) < 2) * 1.2, solid("vine"))
    m.round_box(bd, 0, 0.0, 4.8, 3.6, 16.6, 17.6, solid("vine_dark"), cut=1.4)  # the vine belt
    for sx in (-1, 1):
        m.round_box(bd, sx * 5.4, 0.0, 2.4, 2.4, 23.0, 27.4, solid("brown"), cut=0.8)   # shoulders
        for d in ((sx * 0.5, 1, 0), (sx * 1, 0.4, -0.6), (sx * 1, 0.4, 0.6), (sx * 0.2, 0.6, -1)):
            spike(m, bd, (sx * 6.0, 27.0, 0.0), d, 2.0, 3.0, solid("yellow"), tip=1.0)  # star-shaped pads

    hd = m.bone("head", bd, (0, 27, -0.5))
    rod(m, hd, (0, 26.0, -0.5), (0, 29.0, -2.2), 3.0, solid("brown"), extend=0.4)   # its neck
    m.round_box(hd, 0, -2.5, 2.6, 2.6, 28.5, 32.5, headf, cut=0.8)
    rod(m, hd, (0, 30.0, -4.5), (0, 29.0, -10.0), 2.6, snoutf, extend=0.4, t2=2.4)  # the long snout
    m.box(hd, -0.6, 29.6, -10.6, 0.6, 30.6, -9.8, solid("brown_dark"))         # nose
    spike(m, hd, (0.9, 28.2, -8.4), (0, -1, -0.1), 0.9, 1.4, solid("white"))   # a fang
    m.box(hd, -3.4, 32.0, -5.6, 3.4, 34.0, 2.6, solid("yellow"))               # its shaggy hair
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 33.0, 1.4), (sx * 1, 0.3, 0.8), 2.2, 3.2, solid("orange_dark"), tip=1.0)
        spike(m, hd, (sx * 3.2, 32.4, -3.0), (sx * 1, -0.3, -0.3), 2.0, 2.6, solid("orange"))
    spike(m, hd, (0, 33.0, -5.4), (0, -0.2, -1), 2.4, 2.4, solid("yellow_dark"))

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 3.0, 16, 0.5))
        rod(m, lb, (sx * 3.0, 16.0, 0.5), (sx * 4.5, 9.0, -1.0), 4.0, solid("vine"), extend=0.6)   # leafy legging
        rod(m, lb, (sx * 4.5, 9.0, -1.0), (sx * 4.5, 2.6, 0.5), 3.4, solid("brown"), extend=0.6)
        for d in ((sx * 1, 0.2, -0.4), (sx * 0.3, 0.2, -1), (-sx * 0.6, 0.2, -0.8)):
            spike(m, lb, (sx * 4.5, 7.4, -1.0), d, 1.8, 2.4, solid("yellow"))   # spiky shin wraps
        m.round_box(lb, sx * 4.5, -1.2, 2.4, 3.4, 0.0, 3.0, solid("brown"), cut=0.8)
        for dx in (-1.3, 0.0, 1.3):
            spike(m, lb, (sx * 4.5 + dx, 1.0, -4.4), (0, -0.3, -1), 1.0, 1.8, solid("claw_red"))

        ar = m.bone(f"arm_{side}", bd, (sx * 6.0, 25.5, 0))
        rod(m, ar, (sx * 6.0, 25.5, 0.0), (sx * 8.6, 20.0, -1.0), 3.4, solid("brown"), extend=0.6)
        rod(m, ar, (sx * 8.6, 20.0, -1.0), (sx * 8.6, 15.6, -4.6), 3.2, solid("brown"), extend=0.6)
        m.round_box(ar, sx * 8.6, -5.6, 2.0, 2.0, 13.2, 16.6, solid("glove"), cut=0.8)     # red-brown fists
        for d in ((sx * 1, 0.4, 0), (0, 0.5, 1), (sx * 0.6, 0.6, -0.6)):
            spike(m, ar, (sx * 8.6, 16.8, -4.4), d, 1.8, 2.4, solid("yellow"))   # spiky cuffs

    ar = "arm_right"                                                            # the vine lasso in its right fist
    rod(m, ar, (8.6, 16.0, -6.0), (10.0, 24.0, -6.4), 1.2, solid("vine_dark"), extend=0.4)
    c, pts = (11.4, 30.0, -4.4), []
    for i in range(13):
        t = 2 * math.pi * i / 12 - math.pi / 2
        pts.append((c[0] + 5.0 * math.cos(t) * 0.9, c[1] + 5.4 * math.sin(t), c[2] + 2.6 * math.cos(t)))
    pts[0] = (10.0, 24.0, -6.4)
    for a, b in zip(pts, pts[1:]):
        rod(m, ar, a, b, 1.2, solid("vine"), extend=0.5)
    for a in pts[2:11:3]:
        spike(m, ar, a, (0.4, 0.3, -1), 1.0, 1.6, solid("green"))               # leaves on the lasso

    tl = m.bone("tail", bd, (0, 16, 3))
    rod(m, tl, (0, 16.0, 3.0), (-1.0, 11.0, 10.0), 3.4, ramp("yellow", "orange"), extend=0.5)
    rod(m, tl, (-1.0, 11.0, 10.0), (-2.0, 5.0, 14.0), 3.6, ramp("orange", "red"), extend=0.4)
    for i, (d, h) in enumerate((((-0.8, 0.4, 0.5), 2.6), ((0.8, 0.2, 0.6), 2.4), ((0, -1, 0.3), 3.0))):
        spike(m, tl, (-1.6, 8.0 - i * 1.5, 12.0 + i), d, 1.6, h, solid("red"), tip=0.8)  # flame-like tatters
    return m
