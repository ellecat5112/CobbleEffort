"""Batterimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, a pixel
sprite): a living battery. A red-orange cell banded in yellow with a silver cap terminal, a sleepy face, a blue spark
mark and a red switch knob, standing on two thin steel legs. 1 block tall.

Front is -z, y is up. 28 units tall; no level known (Child used).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import local, metal, mix, plane, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 0.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 18}
LOOK = "a living battery: a red-orange cell banded in yellow, a silver cap terminal, a sleepy face, two thin legs"
BASE = {"red": (230, 70, 30), "red_dark": (150, 30, 10), "yellow": (250, 210, 60), "silver": (210, 214, 226),
        "silver_dark": (110, 114, 128), "black": (30, 30, 36), "blue": (60, 140, 240), "knob": (220, 40, 40)}
SHINY = {"red": (60, 160, 90), "red_dark": (20, 90, 40), "yellow": (200, 230, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def cellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    a, b = plane(x, y, z, face)
    if 0.65 < v / max(H, 1e-6) < 0.78:
        return tone(p["yellow"], face), None
    if face == "north":
        for sx in (-1, 1):
            if abs(a - sx * 2.0) < 1.0 and abs(b - 16.4 - 0.3 * abs(a - sx * 2.0)) < 0.25:
                return p["black"], None                          # sleepy eyes
        if abs(a - 3.4) < 0.4 and 18.0 < b < 20.0:
            return p["blue"], p["blue"]
    shade = 0.75 + 0.25 * math.cos((a / 5.0) * 1.2)
    return tone(mix(p["red_dark"], p["red"], shade), face), None


def build():
    m = Model("batterimon")
    top = m.bone("batterimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    m.round_box(bd, 0, 0, 5.0, 5.0, 8.0, 24.0, cellf, cut=2)
    m.round_box(bd, 0, 0, 2.4, 2.4, 24.0, 26.4, metal(P, "silver", dark="silver_dark"), cut=1)
    m.box(bd, -0.8, 9.0, -5.6, 0.8, 11.0, -4.6, solid(P, "knob"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 8.0, 0))
        rod(m, lg, (sx * 2.4, 8.0, 0), (sx * 3.4, 1.0, -0.6), 1, metal(P, "silver", dark="silver_dark"), extend=0.3)
        m.box(lg, sx * 3.4 - 1.2, 0.0, -2.4, sx * 3.4 + 1.2, 1.0, 1.0, solid(P, "black"))
    return m
