"""Abbadomon (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a
floating vortex of black ribbons wound round an empty core, every ribbon studded with staring red eyes, a purple glow
and a fanged maw in the dark at its heart. 35 blocks tall.

Front is -z, y is up. 44 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digiwar import make_palette, solid_of
from _route import tone

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "floater"
K = 2
LOOK = "a floating vortex of black ribbons round an empty core, every ribbon studded with staring red eyes, a purple glow and a fanged maw at its heart"

BASE = {"ribbon": (36, 34, 46), "ribbon_dark": (20, 18, 28), "eye": (255, 40, 40), "core": (130, 60, 200),
        "maw": (20, 10, 20), "fang": (240, 236, 240)}
SHINY = {"ribbon": (220, 222, 236), "ribbon_dark": (170, 172, 190), "eye": (60, 200, 255), "core": (230, 180, 60)}
P = make_palette(BASE, SHINY)
solid = solid_of(P)


def ribbonf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    along = box.lo[2] + box.size[2] - z
    if face in ("east", "west", "up") and along % 3.2 < 1.0 and abs(y - (box.lo[1] + box.size[1] / 2)) < 0.5:
        return p["eye"], p["eye"]
    return tone(p["ribbon"] if face != "down" else p["ribbon_dark"], face), None


def build():
    m = Model("abbadomon")
    top = m.bone("abbadomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    m.round_box(bd, 0, 0, 3.6, 3.6, 16.0, 26.0, solid("core", glow=True), cut=1.4)   # the glowing core
    m.box(bd, -2.4, 18.0, -3.8, 2.4, 21.0, -3.6, solid("maw"))
    for sx in (-1.6, -0.5, 0.6, 1.7):
        m.box(bd, sx - 0.3, 19.6, -3.9, sx + 0.3, 21.0, -3.85, solid("fang"))
    # ribbons: several tilted rings of segments wound round the core, each its own swaying bone
    for r_i, (rad, y0, tilt, phase) in enumerate(((10, 8, 18, 0.0), (13, 15, -14, 0.7), (15, 23, 10, 1.3),
                                                  (12, 31, -20, 2.1), (8, 38, 15, 2.8))):
        rb = m.bone(f"ring_{r_i + 1}", bd, (0, y0, 0))
        n = 12
        pts = []
        for i in range(n + 1):
            th = phase + 2 * math.pi * i / n * 0.9
            y = y0 + math.sin(th) * rad * math.sin(math.radians(tilt))
            pts.append((rad * math.cos(th), y, rad * math.sin(th) * math.cos(math.radians(tilt))))
        for a, b in zip(pts, pts[1:]):
            rod(m, rb, a, b, 2.4, ribbonf, extend=0.4, t2=0.8)
    return m
