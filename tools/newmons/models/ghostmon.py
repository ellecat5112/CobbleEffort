"""Ghostmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
little ghost of blue flame: a round blue head with dark hollow eyes and a stitched grin, a navy furry collar, a wide
blue witch's hat with a buckled band and blue fire streaming off its top, floating hands of flame and a wispy tail.
Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, fabric, flame_inside, fur, local, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = ("a little blue-flame ghost with dark hollow eyes, a stitched grin, a navy furry collar, a wide witch's hat and "
        "floating hands of flame")
BASE = {"blue": (110, 170, 250), "blue_dark": (50, 100, 210), "navy": (40, 50, 120), "navy_dark": (16, 20, 60),
        "hat": (60, 110, 220), "hat_dark": (24, 50, 140), "buckle": (230, 230, 240), "eye": (14, 16, 40),
        "stitch": (14, 16, 40), "fire": (90, 160, 255, 215), "fire_core": (220, 240, 255, 240)}
SHINY = {"blue": (180, 120, 250), "blue_dark": (110, 50, 200), "fire": (190, 110, 255, 215), "hat": (120, 60, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.6, y - 15.6) < 1.0:
                return tone(p["eye"], face), None
        if abs(y - 12.6 - 0.12 * x * x) < 0.25 and abs(x) < 2.6:
            return tone(p["stitch"], face), None
        if abs(y - 12.7) < 0.7 and abs((x * 1.2) % 1.2 - 0.6) < 0.15 and abs(x) < 2.6:
            return tone(p["stitch"], face), None
    return skin(P, "blue", dark="blue_dark")(x, y, z, face, variant, box=box, **k)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def flame(m, bone, at, w, h, seed):
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
              cutout(flame_inside(4, 0.15, seed), firef), rotation=(0, ang, 0), pivot=at)


def build():
    m = Model("ghostmon")
    top = m.bone("ghostmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 3.4, 3.0, 4.0, 10.0, skin(P, "blue", dark="blue_dark"), cut=1)       # wispy body
    m.round_box(bd, 0, 0, 4.6, 4.0, 9.0, 11.6, fur(P, "navy", "navy_dark", length=0.8), cut=2)   # furry collar
    hd = m.bone("head", bd, (0, 14, 0))
    m.round_box(hd, 0, 0, 4.4, 4.0, 11.0, 19.0, headf, cut=2)
    m.round_box(hd, 0, 0, 8.0, 7.0, 18.4, 19.6, fabric(P, "hat", "hat_dark"), cut=3)          # wide brim
    m.round_box(hd, 0, 0.4, 3.6, 3.2, 19.4, 23.0, fabric(P, "hat", "hat_dark"), cut=1)
    m.round_box(hd, 0, 0.4, 3.7, 3.3, 19.6, 20.8, solid(P, "navy"), cut=1)
    m.box(hd, -0.8, 19.6, -3.0, 0.8, 20.8, -2.8, solid(P, "buckle"))
    for j in range(3):
        flame(m, hd, ((j - 1) * 2.0, 22.6, 0.4), 3.0, 7.0 - abs(j - 1) * 2.0, j + 1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 9.0, -1.0))
        flame(m, ab, (sx * 7.0, 6.0, -1.0), 3.4, 6.0, 5 + sx)
    tb = m.bone("tail", bd, (0, 4, 1))
    flame(m, tb, (0, 0.4, 2.0), 4.0, 5.0, 9)
    return m
