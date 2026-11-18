"""Nanomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tiny brilliant machine: a glass dome of circuitry and gears for a head over a steel cylinder body
with a red eye lens, two long jointed steel arms ending in clawed hands (one bristling with micro-missiles), and two
stubby legs with orange-tipped feet. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tiny machine with a glass dome of circuitry for a head, a steel cylinder body with a red eye lens, long "
        "jointed clawed arms and stubby orange-tipped legs")
BASE = {"steel": (190, 194, 206), "steel_dark": (90, 94, 108), "dark": (50, 52, 62), "glass": (170, 210, 240, 130),
        "circuit": (230, 190, 70), "red": (220, 40, 40), "red_light": (255, 170, 170), "orange": (230, 110, 40)}
SHINY = {"steel": (230, 200, 120), "steel_dark": (150, 110, 40), "glass": (230, 170, 240, 130)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def glassf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["glass"] if (u / max(W, 1e-6) + v / max(H, 1e-6)) % 1.0 > 0.15 else (240, 250, 255, 180)), None


def build():
    m = Model("nanomon")
    top = m.bone("nanomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 5.0, 5.0, 10.0, 24.0, armour(P, "steel", "steel_dark", trim="dark", trim_w=0.4), cut=2)
    ball(m, bd, (0, 17.0, -4.8), 1.6, gem(P, "red", "red_light"), layers=2)
    hd = m.bone("head", bd, (0, 24, 0))
    for j in range(4):                                                                   # circuitry inside the dome
        m.box(hd, -3.0 + j * 1.2, 25.0, -1.0, -2.4 + j * 1.2, 30.0 - j, 1.0, solid(P, "circuit"))
    ball(m, hd, (0, 28.0, 0), 4.8, glassf, layers=4, ry=5.0)                               # glass dome
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 21.0, 0))
        pts = [(sx * 5.0, 21.0, 0), (sx * 10.0, 22.0, -3.0), (sx * 16.0, 20.0, -6.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, STEEL, extend=0.3)
            ball(m, ab, p1, 1.4, solid(P, "dark"), layers=2)
        for f in range(4):
            spike(m, ab, (sx * 16.0 + (f - 1.5) * 0.8, 19.0, -7.0), (sx * 0.3, -0.6, -1), 0.9, 3.0, STEEL, tip=0.8)
        if sx > 0:
            for j in range(4):                                                           # micro-missiles
                rod(m, ab, (17.0, 21.0 + j * 0.8, -7.0), (19.0, 22.0 + j * 0.8, -10.0), 1, solid(P, "orange"),
                    extend=0.1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 11.0, 0))
        rod(m, lg, (sx * 3.0, 11.0, 0), (sx * 4.0, 4.0, 0), 2, STEEL, extend=0.3)
        m.round_box(lg, sx * 4.0, -0.8, 2.0, 2.6, 0.0, 3.0, solid(P, "dark"), cut=0)
        spike(m, lg, (sx * 4.0, 1.4, -3.4), (0, -0.2, -1), 1.6, 3.0, solid(P, "orange"), tip=0.8)
    return m
