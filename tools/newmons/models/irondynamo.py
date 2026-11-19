"""Iron Dynamo (Electric/Ground), a paradox Regieleki, built from boxes after the art the user shared (artist not
named, no name given; our name).

A pale lavender sphere split into four blue-grey panels round a pale face disc that shows Regieleki's dots in glowing
yellow. Where Regieleki has its banded side pods it carries threaded drill cones, one on each side and one pointing
straight down, each ending in a spike. Two big three-fingered hands float free of it, one raised beside it and one
low on the other side, and a little drone with a glowing yellow lens and three spikes hovers near its feet. Yellow-
green lightning crackles round it.

Shiny: teal panels with magenta lights and pink lightning.

Front is -z, y is up. 38 units tall; about 1.6 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _regi import dot_at, ellipsoid, lit, threads
from _rotomform import bolt_plane
from _route import pal, tone

HEIGHT = 38
SCALE = round(1.6 * 16 / HEIGHT, 3)
HITBOX = [1.3, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a pale lavender sphere of four blue-grey panels round a face of glowing yellow dots, with threaded drill cones "
        "on its sides and below, two floating three-fingered hands and a little spiked drone")

BASE = {"white": (238, 238, 250), "lav": (210, 214, 238), "panel": (150, 160, 208), "panel_dark": (112, 122, 172),
        "core": (88, 96, 140), "yellow": (250, 232, 64), "aura": (222, 244, 110), "aura_light": (246, 255, 200)}
SHINY = {"lav": (212, 236, 236), "panel": (88, 188, 190), "panel_dark": (56, 140, 150), "core": (40, 96, 106),
         "yellow": (255, 90, 200), "aura": (255, 150, 230), "aura_light": (255, 214, 244)}
CY = 19.0
DOTS = [(-1.7, 1.7), (0, 2.0), (1.7, 1.7), (-3.0, 0), (0, 0.2), (3.0, 0), (0, -1.8)]


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def spheref(x, y, z, face, variant, **k):
    """Four blue-grey panels split by a pale cross, round a pale face disc of glowing yellow dots."""
    p = P(variant)
    dy = y - CY
    if face == "north" and x * x + (dy - 0.3) ** 2 < 4.7 ** 2:
        if dot_at(-x, dy - 0.3, DOTS, 0.62):
            return p["yellow"], p["yellow"]
        return lit(p["white"], face, y, CY, 7), None
    if face in ("north", "south", "up", "down"):
        across = abs(x)
    else:
        across = abs(z)
    if across < 0.8 or abs(dy) < 0.8:
        return lit(p["lav"], face, y, CY, 7), None
    return lit(p["panel"], face, y, CY, 7), None


def threadf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["panel"] if face not in ("north", "south") else p["panel_dark"], face), None


def handf(x, y, z, face, variant, **k):
    p = P(variant)
    return lit(p["white"] if face != "south" else p["lav"], face, y, y, 1), None


def droneF(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and (x + 5.5) ** 2 + (y - 4.6) ** 2 < 1.3 ** 2:
        return p["yellow"], p["yellow"]
    return tone(p["white"], face), None


def floating_hand(m, bone, c, tips):
    ellipsoid(m, bone, c[0], c[1], c[2], 3.2, 3.2, 2.6, handf, step=1)
    for t in tips:
        mid = tuple(a + 0.55 * (b - a) for a, b in zip(c, t))
        rod(m, bone, c, mid, 2.4, solid("white"), extend=0.4)
        rod(m, bone, mid, t, 2.0, solid("white"), extend=0.4)


def build() -> Model:
    m = Model("irondynamo")
    top = m.bone("irondynamo", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 19, 0))
    ellipsoid(m, bd, 0, CY, 0, 7.5, 7.0, 6.5, spheref, step=1)                   # the panelled sphere
    for sx in (-1, 1):                                                          # side drills
        rod(m, bd, (sx * 6.0, CY, 0), (sx * 15.0, CY, 0), 2, solid("core"), extend=0.2)
        threads(m, bd, (sx * 6.6, CY, 0), (sx, 0, 0), 4.6, 2.6, 4, 2.4, threadf, tip=4.2, tip_w=1.2, groove=solid("core"))
    rod(m, bd, (0, 13.0, 0), (0, 4.0, 0), 2, solid("core"), extend=0.2)
    threads(m, bd, (0, 12.6, 0), (0, -1, 0), 4.2, 2.0, 4, 2.4, threadf, tip=3.8, tip_w=1.2, groove=solid("core"))   # the drill below
    floating_hand(m, m.bone("hand_left", bd, (-14, 31, -1)), (-14.0, 31.0, -1.0),
                  [(-12.6, 37.2, -1.6), (-16.4, 37.0, -1.0), (-20.0, 33.6, -0.6)])
    floating_hand(m, m.bone("hand_right", bd, (14, 9, -1)), (14.0, 9.0, -1.0),
                  [(12.8, 2.8, -1.6), (16.6, 3.0, -1.0), (19.8, 6.4, -0.6)])
    dr = m.bone("drone", bd, (-5.5, 4.5, -3))
    ellipsoid(m, dr, -5.5, 4.5, -3.0, 2.5, 2.5, 2.5, droneF, step=1)              # the little drone
    for d in ((1, 0, 0), (-1, 0, 0), (0, -1, 0)):
        base = (-5.5 + d[0] * 2.2, 4.5 + d[1] * 2.2, -3.0)
        spike(m, dr, base, d, 1.2, 2.4, solid("white"))
    for x, y, z, w, h, fl in ((-21, 12, 5, 8, 13, False), (13, 22, 5, 8, 12, True), (-8, 28, 5.5, 6, 8, True),
                              (5, 0, 5.5, 6, 8, False)):
        bolt_plane(m, bd, x, y, z, w, h, P, plane="xy", flip=fl)                 # crackling lightning
    return m
