"""Dokunemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
poison larva. A plump green caterpillar curled upright, its segmented body striped with dark zigzags, a glossy purple
face with a big round purple mouth, two curving purple horns, little purple claw legs, and two long wavy green
antennae with dark edges. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import gem, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 6}
LOOK = ("a plump upright green caterpillar with dark zigzag stripes, a glossy purple face, two curving purple horns and "
        "long wavy green antennae")
BASE = {"green": (90, 190, 90), "green_dark": (30, 100, 40), "green_light": (180, 240, 170), "zig": (30, 50, 40),
        "purple": (140, 40, 160), "purple_light": (230, 160, 240), "olive": (120, 120, 60), "olive_dark": (60, 60, 20)}
SHINY = {"green": (230, 190, 60), "green_dark": (150, 110, 10), "green_light": (255, 240, 160), "purple": (40, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "green", dark="green_dark", light="green_light", var=0.03)


def segf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs((y % 4.0) - 2.0 - abs((x % 2.0) - 1.0)) < 0.25:
        return tone(p["zig"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dokunemon")
    top = m.bone("dokunemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    for i, (r, y, z) in enumerate(((4.0, 2.0, 4.0), (5.0, 5.0, 2.0), (6.0, 9.0, 0.0), (6.4, 14.0, 0.0),
                                   (6.6, 19.0, 1.0))):
        m.round_box(bd, 0, z, r, r * 0.9, y - 2.0, y + 2.6, segf if i < 4 else segf, cut=max(1, round(r * 0.35)))
    hd = m.bone("head", bd, (0, 20, -4))
    ball(m, hd, (0, 18.0, -5.0), 3.6, gem(P, "purple", "purple_light", glow=False), layers=4, squash=0.8)  # face
    for sx in (-1, 1):                                                         # curving purple horns
        pts = [(sx * 4.0, 14.0, -3.0), (sx * 7.0, 16.0, -4.0), (sx * 8.0, 20.0, -5.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "purple"), extend=0.4, t2=2)
        pts = [(sx * 2.0, 22.0, 0.0)]                                          # long wavy antennae
        for j in range(1, 6):
            pts.append((sx * (2.0 + j * 1.6 + math.sin(j * 1.4) * 1.4), 22.0 + j * 2.4, 2.0 * math.cos(j)))
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, SKIN, extend=0.3, t2=2)
    for j in range(4):                                                         # little purple claw legs
        for sx in (-1, 1):
            spike(m, bd, (sx * 4.6, 3.0 + j * 3.0, -2.6), (sx * 0.4, -0.6, -1), 1.0, 2.0, solid(P, "purple"), tip=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        m.bone(nm, top, (sx * 3.0, 1.0, 0))
    return m
