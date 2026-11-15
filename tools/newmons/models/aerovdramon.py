"""Aero V-dramon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a blue
dragon crouched to pounce, white armour plates on its chest and shoulders, a great white horn on its snout, two curved
horns back from its head, a V on its chest, wide red wings and white claws. 25 blocks tall.

Front is -z, y is up. 34 units tall (the wings); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import eye, sized, teeth_row
from _digiwar import make_palette, solid_of
from _route import tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 1.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a blue dragon crouched to pounce, white chest and shoulder armour, a great white snout horn, curved horns, a V on its chest, wide red wings and white claws"

BASE = {"blue": (60, 110, 200), "blue_dark": (36, 70, 140), "armour": (238, 232, 214), "armour_dark": (190, 182, 160),
        "wing": (190, 40, 40), "wing_dark": (130, 20, 24), "horn": (240, 238, 230), "claw": (240, 240, 244),
        "eye": (230, 40, 40), "pupil": (20, 18, 22), "white": (255, 255, 255), "v": (240, 196, 50),
        "teeth": (246, 244, 236), "mouth": (160, 30, 50)}
SHINY = {"blue": (40, 40, 50), "blue_dark": (24, 24, 30), "wing": (60, 120, 220), "wing_dark": (30, 70, 150),
         "v": (90, 220, 255)}
P = make_palette(BASE, SHINY)
solid = solid_of(P)


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 8.5, y - 20.0, 1.1, iris="eye")
        if c is not None:
            return c, None
    return tone(p["blue"], face), None


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(abs(x) - (y - 12.0) * 0.45) < 0.45 and 12 < y < 18:
        return p["v"], p["v"]                                                   # the V on its chest
    return tone(p["armour"], face), None


def wingf(x, y, z, face, variant, **k):
    """A red dragon wing (a cut-out plane, yz): ribs fanning back, scalloped edge."""
    p = P(variant)
    u, v = z - 2.0, y - 18.0
    if u < 0 or v < 0 or v > 16 - u * 0.45:
        return (0, 0, 0, 0), None
    if v < 1.5 + 2.4 * abs(math.sin(u * 0.45)):
        return (0, 0, 0, 0), None
    if abs(v - u * 0.9) < 0.5 or abs(v - u * 0.35) < 0.5:
        return tone(p["wing_dark"], face), None
    return tone(p["wing"], face), None


def build():
    m = Model("aerovdramon")
    top = m.bone("aerovdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11, 2))
    m.round_box(bd, 0, 3.0, 5.0, 7.0, 7.0, 16.0, solid("blue"), cut=2.0)
    m.round_box(bd, 0, -3.5, 4.6, 3.0, 9.0, 19.0, chestf, cut=1.4)              # the armoured chest
    hd = m.bone("head", bd, (0, 19, -5))
    m.round_box(hd, 0, -6.0, 3.4, 3.6, 16.5, 23.0, headf, cut=1.2)
    m.box(hd, -2.6, 16.6, -14.0, 2.6, 20.0, -9.0, headf)                        # snout
    spike(m, hd, (0, 20.0, -12.5), (0, 1, -0.35), 2.6, 6.0, solid("horn"), tip=0.4)    # the great snout horn
    for sx in (-1, 1):
        rod(m, hd, (sx * 2.6, 22.0, -4.5), (sx * 4.0, 25.0, 1.0), 1.4, solid("horn"), extend=0.2)
        spike(m, hd, (sx * 4.0, 25.0, 1.0), (sx * 0.3, 0.2, 1), 1.2, 3.0, solid("horn"), tip=0.3)
    teeth_row(m, hd, [(sx * 2.2, 16.8, z) for sx in (-1, 1) for z in (-13.0, -11.4, -9.8)], (0, -1, 0), 0.7, 1.0)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 3.6, 18.0, 2.0))
        m.box(w, sx * 3.6, 18.0, 2.0, sx * 3.6, 34.0, 30.0, wingf, rotation=(0, sx * 30, sx * 20), pivot=(sx * 3.6, 18, 2))
    for leg, (lx, lz, front) in (("leg_front_left", (4.0, -3.0, True)), ("leg_front_right", (-4.0, -3.0, True)),
                                 ("leg_back_left", (4.4, 7.0, False)), ("leg_back_right", (-4.4, 7.0, False))):
        lg = m.bone(leg, top, (lx, 10.0, lz))
        if front:
            m.round_box(lg, lx * 1.1, lz, 2.4, 2.4, 9.0, 14.0, solid("armour"), cut=0.8)    # shoulder plate
        m.round_box(lg, lx, lz, 1.9, 2.1, 1.0, 10.5, solid("blue"), cut=0.6)
        m.box(lg, lx - 2.0, 0.0, lz - 2.8, lx + 2.0, 1.8, lz + 2.0, solid("blue_dark"))
        for dx in (-1.1, 0.0, 1.1):
            spike(m, lg, (lx + dx, 0.6, lz - 2.8), (0, -0.2, -1), 0.8, 2.0, solid("claw"), tip=0.25)
    pts = [(0, 11.0, 9.5), (0, 8.5, 15.0), (0, 7.0, 21.0), (0, 8.0, 26.0)]
    t1 = m.bone("tail", bd, pts[0])
    for i, (a, b2, t) in enumerate(zip(pts, pts[1:], (4.0, 3.0, 2.0))):
        rod(m, t1, a, b2, t, solid("blue"), extend=0.6)
    return m
