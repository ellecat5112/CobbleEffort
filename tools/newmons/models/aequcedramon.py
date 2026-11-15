"""Aequcedramon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a
small blue dragon with a fluffy white ruff round its neck and chest, spiky horns, wide blue bat wings and pale blue
claws, trailing a ring of frosty wind. 15 blocks tall.

Front is -z, y is up. 30 units tall (the wings); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import eye, sized
from _digiwar import make_palette, solid_of
from _route import tone

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 1.4)
KIND = "quadruped"
K = 4
LOOK = "a small blue dragon with a fluffy white ruff, spiky horns, wide blue bat wings and pale claws, trailing a ring of frosty wind"

BASE = {"blue": (80, 110, 220), "blue_dark": (50, 70, 160), "ruff": (246, 248, 252), "ruff_dark": (200, 210, 230),
        "wing": (100, 130, 230), "wing_dark": (60, 80, 180), "claw": (200, 220, 250), "eye": (40, 40, 60),
        "pupil": (20, 20, 30), "white": (255, 255, 255), "frost": (200, 230, 255, 120)}
SHINY = {"blue": (230, 130, 190), "blue_dark": (180, 80, 140), "wing": (240, 150, 200), "wing_dark": (190, 100, 150)}
P = make_palette(BASE, SHINY)
solid = solid_of(P)


def ruff(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["ruff_dark"] if (x * 3 + y * 2 + z) % 3 < 0.8 else p["ruff"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 7.0, y - 15.5, 1.1, iris="eye")
        if c is not None:
            return c, None
    return tone(p["blue"], face), None


def wingf(x, y, z, face, variant, **k):
    """A bat wing (a cut-out plane in the xy plane): scalloped trailing edge between finger bones."""
    p = P(variant)
    u, v = abs(x) - 2.0, y - 10.0
    if u < 0 or v < 0 or v > 14 - u * 0.3:
        return (0, 0, 0, 0), None
    if v < 2.0 + 2.2 * abs(math.sin(u * 0.55)):
        return (0, 0, 0, 0), None
    if abs(v - u * 1.1) < 0.5 or abs(v - u * 0.5) < 0.5:
        return tone(p["wing_dark"], face), None
    return tone(p["wing"], face), None


def build():
    m = Model("aequcedramon")
    top = m.bone("aequcedramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 1.0, 3.0, 4.0, 4.0, 10.0, solid("blue"), cut=1.2)
    m.round_box(bd, 0, -2.0, 3.6, 2.8, 7.0, 13.0, ruff, cut=1.2)                 # the fluffy ruff
    hd = m.bone("head", bd, (0, 13, -3))
    m.round_box(hd, 0, -5.0, 2.6, 3.0, 12.0, 18.0, headf, cut=1.0)
    m.box(hd, -1.6, 12.6, -10.0, 1.6, 15.0, -7.0, headf)
    for d in ((0.4, 1, 0.6), (-0.4, 1, 0.6), (0.9, 0.7, 0.6), (-0.9, 0.7, 0.6)):
        spike(m, hd, (d[0] * 1.5, 17.5, -4.0), d, 1.0, 2.4, solid("ruff"), tip=0.3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 2.0, 10.0, 1.0))
        x0, x1 = sorted((sx * 2.0, sx * 16.0))
        m.box(w, x0, 10.0, 1.0, x1, 24.0, 1.0, wingf, rotation=(0, -sx * 25, 0), pivot=(sx * 2.0, 10.0, 1.0))
    for leg, (lx, lz) in (("leg_front_left", (2.0, -2.0)), ("leg_front_right", (-2.0, -2.0)),
                          ("leg_back_left", (2.2, 3.6)), ("leg_back_right", (-2.2, 3.6))):
        lg = m.bone(leg, top, (lx, 4.5, lz))
        m.round_box(lg, lx, lz, 1.1, 1.2, 0.0, 4.8, solid("blue"), cut=0.4)
        for dx in (-0.5, 0.5):
            spike(m, lg, (lx + dx, 0.4, lz - 1.0), (0, -0.2, -1), 0.5, 1.0, solid("claw"), tip=0.2)
    tl = m.bone("tail", bd, (0, 6.5, 5))
    rod(m, tl, (0, 6.5, 5.0), (0, 5.0, 10.0), 1.6, solid("blue"), extend=0.3)
    rod(m, tl, (0, 5.0, 10.0), (0, 6.0, 13.5), 1.0, solid("blue_dark"), extend=0.2)
    ring = m.bone("ring_frost", top, (0, 1.0, 0))
    for i in range(16):                                                         # a ring of frosty wind
        th = 2 * math.pi * i / 16
        a = (8 * math.cos(th), 1.0, 8 * math.sin(th))
        b2 = (8 * math.cos(th + 2 * math.pi / 16), 1.0, 8 * math.sin(th + 2 * math.pi / 16))
        rod(m, ring, a, b2, 0.8, solid("frost"), extend=0.2, t2=0.3)
    return m
