"""Unnamed Digimon 1 (Legendary Skies) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail
standard after a manga panel on wikimon.net): a little round rabbit-like Digimon from the Legendary Skies manga: a
plump cream body, two long upright ears, dizzy spiral eyes, a small nose and a startled mouth, and stubby paws. 1
block.

Front is -z, y is up. Child stage (by analogy: wikimon gives no level).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digibeast import ball
from _digidetail import plane, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little round cream rabbit-like Digimon with long upright ears and dizzy spiral eyes"
BASE = {"cream": (246, 236, 210), "cream_dark": (200, 184, 150), "ink": (40, 34, 30), "pink": (230, 150, 150)}
SHINY = {"cream": (210, 230, 246), "cream_dark": (150, 176, 210)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            dx, dy = a - sx * 2.2, b - 11.6
            r = math.hypot(dx, dy)
            if r < 1.6:
                ang = math.atan2(dy, dx)
                if abs(((r * 3.0 - ang / math.pi) % 1.0) - 0.5) < 0.18:
                    return p["ink"], None
        if math.hypot(a, b - 9.8) < 0.5:
            return p["ink"], None
        if math.hypot(a, b - 8.0) < 0.8:
            return p["pink"], None
    return skin(P, "cream", dark="cream_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("unnameddigimon1legendaryskies")
    top = m.bone("unnameddigimon1legendaryskies", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 9.0, 0), 5.8, bodyf, layers=5, squash=0.95)
    for sx in (-1, 1):
        m.round_box(bd, sx * 2.4, 0.6, 1.4, 1.0, 13.6, 23.6, skin(P, "cream", dark="cream_dark"), cut=0)
        m.box(bd, sx * 2.4 - 0.7, 15.6, -0.5, sx * 2.4 + 0.7, 22.6, -0.3, solid(P, "pink"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 8.0, -1.0))
        ball(m, ab, (sx * 5.8, 7.0, -2.0), 1.4, skin(P, "cream", dark="cream_dark"), layers=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 3.0, 0))
        m.round_box(lg, sx * 2.6, -0.8, 1.6, 2.2, 0.0, 3.2, skin(P, "cream", dark="cream_dark"), cut=1)
    return m
