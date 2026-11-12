"""Sensarat, the Feeler Pokémon (Normal), built from boxes after the concept art the user shared (the art's own name).

Mousense grown into a round, shaggy ball of a rat: brown fur with darker patches and tufts all round its edge, a cream
face with a pointed snout, a pink nose and a buck tooth, eyes still closed, big round ears with yellow insides, very
long dark whiskers it sweeps about like feelers, small pink feet, and a long pink tail curving up behind it.

Shiny (from the art): dark navy fur with pale patches, a pale face and white whiskers like a moustache.

Front is -z, y is up. 17 units tall to its tail; baseScale 0.68 (0.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _route import pal, tone
from _sense import closed_eyes, ear_disc, solid, whisker

SCALE = 0.68
HITBOX = [0.7, 0.6]
KIND = "quadruped"
K = 5
HEIGHT = 17
LOOK = ("a round, shaggy brown rat with a cream face, closed eyes, big round ears, very long dark feeler whiskers and "
        "a long pink tail")

BASE = {"fur": (146, 86, 58), "patch": (104, 58, 42), "face": (240, 212, 166), "ear": (70, 56, 80),
        "ear_in": (236, 202, 108), "pink": (234, 160, 184), "whisker": (64, 48, 70), "tooth": (252, 252, 252),
        "line": (60, 42, 40), "fringe": (124, 72, 48)}
SHINY = {"fur": (40, 52, 82), "patch": (66, 82, 120), "face": (222, 236, 250), "ear": (190, 212, 236),
         "ear_in": (226, 140, 206), "whisker": (246, 248, 252), "fringe": (240, 244, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, **k):
    """Shaggy fur: darker streaks running down like locks of hair."""
    p = P(variant)
    n = math.sin(x * 1.7 + z * 1.3 + math.sin(y * 0.6) * 1.5)
    return tone(p["patch"] if n > 0.55 else p["fur"], face), None


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        if closed_eyes(x, y, 1.6, 9.0, 0.8, None):
            return p["line"], None
        return tone(p["face"], face), None
    return furf(x, y, z, face, variant)


def build() -> Model:
    m = Model("sensarat")
    top = m.bone("sensarat", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 1, 6, 6, 3, 10, furf, cut=2.5)                            # a round shaggy ball
    m.round_box(bd, 0, 1, 5, 5, 1.5, 11.5, furf, cut=2)
    m.round_box(bd, 0, 1, 3.5, 3.5, 0.8, 12.6, furf, cut=1.4)
    for row, (y, r, n, dy) in enumerate(((3.6, 6.2, 12, -0.6), (7, 6.4, 12, -0.25), (10.6, 5.2, 10, 0.3))):
        for i in range(n):                                                        # tufts all round its outline
            a = (i + 0.5 * row) / n * 2 * math.pi
            if row > 0 and math.sin(a) < -0.6:
                continue                                                          # keep the face clear
            spike(m, bd, (math.cos(a) * r, y, 1 + math.sin(a) * r), (math.cos(a), dy, math.sin(a)), 2.2, 2.4, furf, tip=1)
    for dx in (-2.4, 0, 2.4):                                                     # tufts on top
        spike(m, bd, (dx, 12.4, 2), (dx * 0.25, 1, 0.3), 2, 2.2, furf, tip=1)
    hd = m.bone("head", bd, (0, 8, -4))
    m.round_box(hd, 0, -5.2, 3.6, 1.4, 4.6, 11, facef, cut=1)                     # the cream face
    for dx, h in ((-1.5, 1.8), (0, 2.2), (1.5, 1.8)):                             # fringe over the brow
        spike(m, hd, (dx, 11, -6), (dx * 0.2, -0.6, -1), 1.4, h, solid(BASE, SHINY, "fringe"), tip=0.8)
    m.box(hd, -1, 6, -8.6, 1, 8, -6.4, solid(BASE, SHINY, "face"))               # snout
    m.box(hd, -0.7, 7, -9.2, 0.7, 8.2, -8.4, solid(BASE, SHINY, "pink"))         # pink nose
    m.box(hd, -0.5, 4.9, -8.1, 0.5, 6.1, -7.1, solid(BASE, SHINY, "tooth"))      # buck tooth
    for sx in (-1, 1):
        for dy, ang in ((0.5, 0.35), (0, 0.0), (-0.5, -0.35)):                   # long feeler whiskers
            a = (sx * 1.0, 7 + dy, -8)
            b = (sx * 6.5, 7.6 + dy * 3 + ang * 4, -9.5 + ang * 3)
            c = (sx * 11, 9 + dy * 4 + ang * 6, -7 + ang * 6)
            whisker(m, hd, a, b, BASE, SHINY, thick=0.4)
            whisker(m, hd, b, c, BASE, SHINY, thick=0.3)
        m.box(hd, sx * 3.8 - 2.5, 12, -2, sx * 3.8 + 2.5, 17, -2, ear_disc(BASE, SHINY, sx * 3.8, 14.5, 2.5),
              rotation=(0, sx * 12, sx * -18), pivot=(sx * 3.8, 12.5, -2))     # big round ears
    for nm, (lx, lz) in (("leg_front_left", (-2.6, -3)), ("leg_front_right", (2.6, -3)),
                         ("leg_back_left", (-2.6, 4)), ("leg_back_right", (2.6, 4))):
        lg = m.bone(nm, top, (lx, 1.5, lz))
        m.box(lg, lx - 1, 0, lz - 2, lx + 1, 1, lz + 0.6, solid(BASE, SHINY, "pink"))
    tail = m.bone("tail", bd, (0, 4, 7))
    chain(m, tail, [(0, 4, 7), (0, 6.5, 10), (0, 10.5, 11.5), (0, 14, 10.8), (0, 15.6, 9)], [1.2, 1.0, 0.8, 0.7],
          solid(BASE, SHINY, "pink"))
    return m
