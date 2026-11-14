"""Boracle, the Fortune Pig Pokémon (Psychic), Grumpig evolved, after the art the user shared (artist and name not
given; the name, boar + oracle, is ours): a heavy charcoal-grey pig seer bouncing on a coiled spring instead of legs,
white rings stacked above the coil. A small purple head peeks out from under a white hood with a pointed, pink-lined
tip; it has a pink snout, white tusks and a narrow black eye. A necklace of glossy black pearls hangs round its neck
and more float about it. Its purple-palmed hands cradle a pink crystal ball wrapped in a dripping veil of translucent
pink light, and a thin black tail curls out behind.

Shiny: slate blue with a teal head and a cyan crystal ball.

Front is -z, y is up. 40 units tall to its hood tip; baseScale 0.6 (1.5 m). It bounces on its spring.
"""
from __future__ import annotations

import math

from _afake import CUT, solid_of, tongues
from _boxmodel import Model, rod, spike
from _route import pal, tone

SCALE = 0.6
HITBOX = [1.5, 2.5]
KIND = "floater"
K = 3
HEIGHT = 40
LOOK = ("a heavy charcoal pig seer on a coiled spring with a purple head under a white pointed hood, a pink snout, "
        "white tusks, a necklace of black pearls and a pink crystal ball in a dripping veil of light")

BASE = {"grey": (78, 78, 84), "grey_dark": (52, 52, 58), "grey_light": (112, 112, 120), "purple": (150, 112, 178),
        "purple_dark": (112, 80, 140), "white": (244, 244, 246), "white_shade": (204, 204, 212), "pink": (236, 168, 168),
        "pink_dark": (214, 120, 150), "black": (22, 22, 26), "shine": (240, 240, 250), "ball": (240, 150, 176, 190),
        "veil": (236, 120, 190, 130)}
SHINY = {"grey": (70, 84, 120), "grey_dark": (48, 58, 92), "grey_light": (104, 118, 156), "purple": (84, 170, 168),
         "purple_dark": (54, 128, 128), "pink_dark": (90, 190, 200), "ball": (120, 220, 236, 190),
         "veil": (100, 200, 236, 130)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west", "south") and y < 20.0 + (0 if face == "south" else -z * 0.4):
        return tone(p["purple_dark"], face), None                             # its purple underside
    return tone(p["grey_light"] if face == "up" else p["grey"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        dx, dy = x - 1.2, y - 33.4
        if (dx / 0.9) ** 2 + ((dy - dx * 0.3) / 0.5) ** 2 < 1:
            return p["black"], None                                           # a narrow black eye
    return tone(p["purple"], face), None


def hoodf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["white"] if face != "down" else p["white_shade"], face), None


def pearlf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    lo, sz = box.lo, box.size
    if face == "north" and y > lo[1] + sz[1] * 0.6 and x < lo[0] + sz[0] * 0.45:
        return p["shine"], None                                               # a glossy highlight
    return p["black"], None


def pearl(m, bone, c, r):
    m.round_box(bone, c[0], c[2], r, r, c[1] - r, c[1] + r, pearlf, cut=max(0.5, r * 0.5))


def ballf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and math.hypot(x + 1.0, y - 21.4) < 0.7:
        return (255, 255, 255, 230), None
    return p["ball"], None


def veil(top_y, x0, x1):
    """The dripping veil of pink light round the crystal ball: a translucent plane with drips along its bottom."""
    def s(x, y, z, face, variant, **k):
        u = (x - x0) / (x1 - x0)
        bottom = top_y - 3.0 - tongues(u, [(0.12, 5, 0.1), (0.35, 3, 0.08), (0.62, 4.5, 0.1), (0.85, 2.5, 0.08)])
        if not bottom < y < top_y:
            return CUT, None
        return P(variant)["veil"], None
    return s


def build() -> Model:
    m = Model("boracle")
    top = m.bone("boracle", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    pts = []                                                                    # the coiled spring
    for i in range(33):
        a = 2 * math.pi * i / 16
        r = 5.0 - i * 0.05
        pts.append((r * math.sin(a), 1.2 + i * 0.22, -r * math.cos(a) + 1.0))
    for a, b in zip(pts, pts[1:]):
        rod(m, bd, a, b, 2.4, solid("grey_dark"), extend=0.5)
    spike(m, bd, pts[0], (-1, -0.2, -0.3), 2.0, 3.0, solid("grey_dark"), tip=1.0)
    for i, (y0, r) in enumerate(((8.4, 5.0), (10.4, 5.4), (12.4, 5.8))):       # white rings above the coil
        m.round_box(bd, 0, 1.0, r, r, y0, y0 + 1.6, solid("white"), cut=max(1, round(r * 0.35)))
    m.round_box(bd, 0, 1.0, 7.0, 6.0, 14.0, 29.0, bodyf, cut=2.4)               # the heavy body
    m.round_box(bd, 0, 1.0, 5.6, 4.8, 28.6, 30.6, bodyf, cut=1.8)
    for sx in (-1, 1):
        m.round_box(bd, sx * 6.4, 1.0, 2.6, 3.0, 22.0, 29.4, bodyf, cut=1.0)     # broad shoulders
    for i in range(9):                                                          # the pearl necklace
        a = math.pi * (i / 8.0) - math.pi / 2
        pearl(m, bd, (4.4 * math.sin(a), 28.4 - 1.6 * math.cos(a) * 0.5, -4.4 * math.cos(a) + 0.6),
              1.4 if i % 2 else 1.1)

    hd = m.bone("head", bd, (0, 30, -1))
    m.round_box(hd, 0, -1.6, 3.0, 2.8, 30.0, 35.6, headf, cut=1.0)
    m.box(hd, -1.4, 30.6, -6.0, 1.4, 32.6, -4.2, solid("pink"))                 # the pink snout
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.8, 30.8, -4.4), (sx * 0.4, 1, -0.3), 1.0, 1.8, solid("white"))   # tusks
        m.round_box(hd, sx * 3.2, -1.0, 1.4, 2.0, 30.6, 34.6, hoodf, cut=0.6)                 # the hood's sides
    m.round_box(hd, 0, -0.6, 3.6, 3.4, 34.6, 37.2, hoodf, cut=1.2)               # the white hood
    rod(m, hd, (0, 36.6, 0.6), (-0.6, 40.4, 3.0), 2.6, hoodf, extend=0.4)        # its pointed tip
    m.box(hd, -0.9, 37.0, -0.6, 0.9, 39.0, -0.5, solid("pink_dark"))             # pink lining

    for sx, side in ((-1, "left"), (1, "right")):                                # arms round the crystal ball
        ar = m.bone(f"arm_{side}", bd, (sx * 6.4, 26, 0))
        hand = (sx * 2.6, 23.6 if sx < 0 else 18.4, -8.0)
        rod(m, ar, (sx * 6.4, 26.0, 0.0), (sx * 8.0, 21.0, -3.6), 3.4, solid("grey"), extend=0.6)
        rod(m, ar, (sx * 8.0, 21.0, -3.6), hand, 3.0, solid("grey"), extend=0.6)
        m.round_box(ar, hand[0], hand[2], 1.6, 1.4, hand[1] - 1.0, hand[1] + 1.0, solid("purple"), cut=0.6)
    m.round_box(bd, 0, -9.0, 3.2, 3.2, 18.6, 23.4, ballf, cut=1.2)              # the crystal ball
    m.round_box(bd, 0, -9.0, 2.2, 2.2, 17.6, 24.4, ballf, cut=0.8)
    m.box(bd, -10.0, 13.0, -12.2, 8.0, 21.0, -12.2, veil(21.0, -10.0, 8.0))     # its veil of light
    m.box(bd, -10.0, 21.0, -12.2, 8.0, 21.0, -6.0, veil(99.0, -10.0, 8.0))
    for c, r in (((7.6, 33.0, 3.0), 1.4), ((9.4, 30.4, 1.0), 1.2), ((-7.4, 31.4, 1.0), 1.1), ((3.0, 2.0, -6.0), 0.9)):
        pearl(m, bd, c, r)                                                       # pearls floating round it

    tl = m.bone("tail", bd, (0, 22, 6.6))
    loop = [(0, 22.0, 6.6), (2.0, 21.0, 10.0), (5.0, 22.0, 13.0), (7.0, 25.0, 13.0), (6.0, 26.0, 10.0), (4.0, 23.6, 9.0),
            (6.0, 21.0, 13.0), (9.0, 20.0, 16.0)]
    for a, b in zip(loop, loop[1:]):
        rod(m, tl, a, b, 1.0, solid("black"), extend=0.4, t2=0.8)
    return m
