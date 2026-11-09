"""Mega Iron Treads, hand-built from boxes in Cobblemon's style.

Iron Treads (official art: a future Donphan robot: a grey rounded body, a black tread wheel arching over its back with
glowing red panels, a small head with a short trunk and black tusk-blades, a red eye, four short jointed legs) as a
mega: two tread wheels side by side, both glowing, longer tusk-blades and a glowing red visor.

Front is -z, y is up. ~30 units tall; baseScale 1.3 (about 2.4 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.3
HITBOX = [2.6, 2.4]
LOOK = "a grey robot Donphan under two black tread wheels with glowing red panels, long black tusk-blades and a glowing red visor"
KIND = "quadruped"

BASE = {"grey": (150, 156, 166), "grey_light": (186, 192, 200), "grey_dark": (100, 104, 116), "black": (36, 36, 44),
        "red": (240, 50, 60), "red_dark": (150, 24, 34), "visor": (255, 70, 70)}
SHINY = {"grey": (170, 160, 130), "grey_light": (200, 190, 160), "grey_dark": (120, 110, 84), "red": (60, 220, 255),
         "red_dark": (30, 120, 160), "visor": (90, 230, 255)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def grey(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["grey_dark"] if face == "down" else (P["grey_light"] if face == "up" else P["grey"])


def tread(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
    """A tread segment: black rim, glowing red panel inside."""
    P = palette(variant)
    if face in ("up", "east", "west") and 1 <= r < rows - 1 and 1 <= c < cols - 1:
        return P["red"], P["red"]
    return P["black"]


def head(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and 15.5 <= y <= 17 and abs(x) <= 3:
        return P["visor"], P["visor"]
    return grey(x, y, z, face, variant)


def black(x, y, z, face, variant, **k):
    return palette(variant)["black"]


def build() -> Model:
    m = Model("irontreads_mega")
    root = m.bone("irontreads_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 12, 2))
    m.round_box(body, 0, 2, 8, 10, 6, 18, grey, cut=3)
    # two tread wheels arching over the back, segment by segment
    for sgn in (1, -1):
        x0 = sgn * 5.5
        for n in range(11):
            a = math.radians(-100 + n * 20)
            py, pz = 12 + 14 * math.sin(a + math.pi / 2), 2 + 14 * math.cos(a + math.pi / 2)
            if py < 4:
                continue
            m.box(body, x0 - 2.5, py - 1.5, pz - 3.5, x0 + 2.5, py + 1.5, pz + 3.5, tread,
                  rotation=(math.degrees(a), 0, 0), pivot=(x0, py, pz))

    hd = m.bone("head", body, (0, 13, -8))
    m.box(hd, -4, 10, -15, 4, 18, -8, head)
    chain(m, hd, [(0, 11, -15), (0, 8, -19), (0, 5, -20)], [4, 3], grey)
    for sgn in (1, -1):
        chain(m, hd, [(sgn * 3.5, 11, -13), (sgn * 6, 9, -19), (sgn * 7, 11, -25), (sgn * 7, 15, -27)], [3, 2, 2], black)

    for nm, (lx, lz) in (("leg_front_left", (5, -4)), ("leg_front_right", (-5, -4)),
                         ("leg_back_left", (5, 8)), ("leg_back_right", (-5, 8))):
        leg = m.bone(nm, root, (lx, 7, lz))
        m.box(leg, lx - 2, 2, lz - 2, lx + 2, 7, lz + 2, grey)
        m.box(leg, lx - 2.5, 0, lz - 3, lx + 2.5, 2, lz + 2.5, black)
    return m
