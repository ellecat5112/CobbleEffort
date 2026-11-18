"""Ludomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
armoured little soldier: a squat olive-green robot-like kid in a paint-splattered army helmet stamped "01", goggles and
a gap-toothed grin, two big round pink-rimmed shoulder shields splashed with colour, one with an X mark, riveted
armour, clawed metal hands and spiked feet. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a squat olive-green armoured kid in a paint-splattered army helmet, goggles, two big pink-rimmed shoulder shields and clawed hands"
BASE = {"olive": (110, 130, 80), "olive_dark": (50, 64, 30), "olive_light": (170, 190, 130), "pink": (230, 80, 140),
        "blue": (80, 160, 230), "white": (246, 246, 246), "black": (30, 30, 34), "glass": (130, 210, 240),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "tooth": (250, 250, 246)}
SHINY = {"olive": (80, 90, 150), "olive_dark": (30, 36, 80), "olive_light": (150, 160, 220)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = riveted(P, "olive", "olive_dark", light="olive_light")


def splatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    s = math.sin(x * 2.1 + y * 1.3) * math.cos(z * 1.7 - y * 0.9)
    if s > 0.75:
        return tone(p["pink"], face), None
    if s < -0.8:
        return tone(p["blue"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 22.6 < y < 24.4 and -1.6 < x < 1.6 and (x + 2.0) % 1.6 < 1.0:
        return tone(p["white"], face), None
    return splatf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ludomon")
    top = m.bone("ludomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.4, 3.6, 3.0, 6.0, 15.0, ARM, cut=1)
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 14.6, 20.4, ARM, cut=1)
    m.round_box(hd, 0, -3.1, 2.4, 0.3, 16.0, 17.0, solid(P, "tooth"), cut=0)
    m.round_box(hd, 0, -3.1, 2.6, 0.4, 18.4, 19.6, solid(P, "glass"), cut=0)                   # goggles
    m.round_box(hd, 0, 0, 4.6, 4.6, 20.0, 21.4, helmf, cut=2)                                # helmet brim
    m.round_box(hd, 0, 0, 3.6, 3.6, 21.0, 25.0, helmf, cut=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # shoulder shields + claws
        ab = m.bone(nm, bd, (sx * 3.6, 13.0, 0))
        m.box(ab, min(sx * 4.0, sx * 5.4), 9.0, -4.0, max(sx * 4.0, sx * 5.4), 17.0, 4.0, splatf)
        m.round_box(ab, sx * 5.6, 0, 0.3, 3.6, 9.4, 16.6, solid(P, "pink"), cut=0)
        if sx < 0:
            m.box(ab, -5.95, 12.0, -1.4, -5.9, 14.0, 1.4, solid(P, "white"))
        rod(m, ab, (sx * 4.0, 11.0, 0), (sx * 4.6, 7.0, -2.0), 1, ARM, extend=0.3, t2=2)
        for j in range(3):
            spike(m, ab, (sx * 4.6 + (j - 1) * 0.7, 6.4, -2.4), (0, -0.6, -1), 0.8, 2.0, metal(P, "steel", dark="steel_dark"),
                  tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 6.0, 0))
        rod(m, lg, (sx * 1.8, 6.4, 0), (sx * 2.0, 1.6, 0), 2, ARM, extend=0.3)
        m.round_box(lg, sx * 2.0, -0.8, 1.8, 2.4, 0.0, 1.8, ARM, cut=0)
        for j in range(2):
            spike(m, lg, (sx * 2.0 + (j - 0.5) * 1.2, 0.6, -3.2), (0, 0.2, -1), 0.8, 1.4, solid(P, "white"), tip=0.8)
    return m
