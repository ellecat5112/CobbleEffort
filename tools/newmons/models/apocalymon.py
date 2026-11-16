"""Apocalymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the grudge of every Digimon that was deleted. A floating dark-blue dodecahedron core etched with
interlocking hexagon panels, capped with tan stone pentagon plates and a drill-spike below, a black horned crown with
a red crest on top, and long chains snaking out from it that end in steel claws and black shuriken stars.
35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, local, metal, mix, plane, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a floating dark-blue dodecahedron core etched with hexagon panels, tan stone pentagon caps and a drill-spike, "
        "a black horned crown and long chains ending in steel claws and black stars")
BASE = {"core": (40, 60, 130), "core_dark": (14, 20, 60), "core_light": (100, 130, 210), "stone": (220, 190, 130),
        "stone_dark": (150, 120, 70), "black": (30, 30, 36), "black_light": (90, 90, 104), "red": (210, 40, 40),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116)}
SHINY = {"core": (130, 30, 40), "core_dark": (60, 10, 16), "core_light": (220, 100, 110), "stone": (200, 200, 210),
         "stone_dark": (120, 120, 134)}


def P(v):
    return pal(BASE, SHINY, v)


STONE = armour(P, "stone", "stone_dark", panel=(2.4, 2.4))
STEEL = metal(P, "steel", dark="steel_dark")
BLACK = metal(P, "black", dark="black", light="black_light", streak=2.0)


def coref(x, y, z, face, variant, box=None, **k):
    """The core: interlocking hexagon outlines in black on deep blue."""
    p = P(variant)
    a, b = plane(x, y, z, face)
    s = 2.6
    q = (2 / 3 * a) / s
    r = (-1 / 3 * a + math.sqrt(3) / 3 * b) / s
    cx, cz = q, -q - r
    rx, ry, rz = round(q), round(r), round(cz)
    dx, dy, dz = abs(rx - q), abs(ry - r), abs(rz - cz)
    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    d = max(abs(q - rx), abs(r - ry), abs((-q - r) - (-rx - ry)))
    if d > 0.42:
        return tone(p["black"], face), None
    return tone(mix(p["core_dark"], p["core_light"], 0.25 + 0.5 * (1 - d * 2)), face), None


def chain(m, bone, pts):
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        n = max(1, round(math.dist(a, b) / 1.8))
        for j in range(n):
            c = tuple(aa + (bb - aa) * (j + 0.5) / n for aa, bb in zip(a, b))
            m.box(bone, c[0] - 0.6, c[1] - 0.6, c[2] - 0.6, c[0] + 0.6, c[1] + 0.6, c[2] + 0.6, STEEL,
                  rotation=(45 * (j % 2), 45, 0), pivot=c)


def star(m, bone, c):
    for ang in (0, 45, 90, 135):
        m.box(bone, c[0] - 3.0, c[1] - 0.5, c[2] - 0.3, c[0] + 3.0, c[1] + 0.5, c[2] + 0.3, BLACK,
              rotation=(0, 0, ang), pivot=c)


def claw(m, bone, c, d):
    ball(m, bone, c, 1.6, solid(P, "core"), layers=2)
    for j in range(4):
        a = math.radians(j * 90)
        spike(m, bone, c, (d[0] + 0.6 * math.cos(a), d[1] + 0.6 * math.sin(a), d[2]), 1.0, 3.6, STEEL)


def build():
    m = Model("apocalymon")
    top = m.bone("apocalymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    ball(m, bd, (0, 30.0, 0), 11.0, coref, layers=9)
    for ang in (0, 72, 144, 216, 288):                           # tan pentagon caps round the top
        r = math.radians(ang + 36)
        c = (9.6 * math.sin(r), 36.0, -9.6 * math.cos(r))
        m.box(bd, c[0] - 3.6, c[1] - 2.6, c[2] - 1.0, c[0] + 3.6, c[1] + 2.6, c[2] + 1.0, STONE,
              rotation=(30, -ang - 36, 0), pivot=c)
    for ang in (36, 108, 180, 252, 324):                         # and round the bottom
        r = math.radians(ang + 36)
        c = (9.6 * math.sin(r), 24.0, -9.6 * math.cos(r))
        m.box(bd, c[0] - 3.6, c[1] - 2.6, c[2] - 1.0, c[0] + 3.6, c[1] + 2.6, c[2] + 1.0, STONE,
              rotation=(-30, -ang - 36, 0), pivot=c)
    for i in range(4):                                           # the drill spike below
        r = 4.0 - i
        m.round_box(bd, 0, 0, r, r, 17.0 - i * 3.0, 20.0 - i * 3.0, STONE, cut=max(1, round(r * 0.3)))
    spike(m, bd, (0, 8.0, 0), (0, -1, 0), 1.0, 4.0, STONE)
    hd = m.bone("head", bd, (0, 41, 0))                          # the horned crown
    m.round_box(hd, 0, 0, 2.6, 2.6, 40.0, 44.0, BLACK, cut=1)
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.6, 43.0, 0), (sx * 4.0, 48.0, 0), 1, BLACK, extend=0.2)
        spike(m, hd, (sx * 4.0, 48.0, 0), (sx * 0.2, 1, 0), 1.0, 3.0, BLACK)
    for j in range(3):
        m.box(hd, -4.0 - j * 1.6, 44.0 + j * 0.6, 1.0, -1.0 - j * 1.6, 45.0 + j * 0.6, 1.0, solid(P, "red"),
              rotation=(0, 0, 20), pivot=(-1.0, 44.0, 1.0))
    ends = [((20.0, 44.0, -2.0), "claw"), ((24.0, 34.0, 2.0), "star"), ((-20.0, 46.0, 0.0), "star"),
            ((-24.0, 30.0, -2.0), "claw"), ((18.0, 22.0, -4.0), "claw"), ((-16.0, 18.0, 2.0), "star")]
    for i, (e, kind) in enumerate(ends):                         # chains snaking out to claws and stars
        cb = m.bone(f"chain_{i}", bd, (0, 30, 0))
        s = (e[0] * 0.45, 30.0 + (e[1] - 30.0) * 0.4, 0.0)
        mid = ((s[0] + e[0]) / 2, (s[1] + e[1]) / 2 + 4.0, (s[2] + e[2]) / 2 - 3.0)
        chain(m, cb, [s, mid, e])
        if kind == "claw":
            claw(m, cb, e, (1 if e[0] > 0 else -1, 0.2, 0))
        else:
            star(m, cb, e)
    return m
