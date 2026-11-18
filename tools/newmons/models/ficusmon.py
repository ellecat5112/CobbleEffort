"""Ficusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
strangler fig. A small crouching creature hidden in a huge tangle of gnarled olive-brown aerial roots that rise over
it in two great looping masses tipped with green buds and trail down to violet ends, a red eye peering out, clawed
little arms bound with dark bands holding two spiky green seed-balls. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid, twisted
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a small crouching creature in a huge tangle of gnarled olive roots looping over it in two great masses, green "
        "buds, violet root ends, a red eye and two spiky green seed-balls")
BASE = {"root": (120, 110, 60), "root_dark": (60, 54, 24), "root_light": (180, 170, 100), "bud": (110, 200, 90),
        "violet": (150, 80, 180), "eye": (230, 40, 40), "band": (40, 40, 44), "seed": (70, 150, 70),
        "seed_dark": (30, 80, 30), "claw": (220, 220, 200)}
SHINY = {"root": (150, 100, 140), "root_dark": (80, 40, 70), "root_light": (210, 160, 200), "violet": (240, 180, 60)}


def P(v):
    return pal(BASE, SHINY, v)


ROOT = twisted(P, "root", "root_dark", light="root_light", period=1.8, angle=0.4)


def coil(m, bone, pts, t0):
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, p0, p1, max(1, t0 - j // 2), ROOT, extend=0.5)


def build():
    m = Model("ficusmon")
    top = m.bone("ficusmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    m.round_box(bd, 0, 0, 4.4, 3.6, 12.0, 20.0, ROOT, cut=1)                         # crouching body
    hd = m.bone("head", bd, (0, 20, -1))
    m.round_box(hd, 0, -1.0, 3.6, 3.0, 19.0, 25.0, ROOT, cut=1)
    m.box(hd, -1.0, 21.6, -4.2, 1.0, 23.0, -3.8, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                               # two great looping root masses
        for k in range(5):
            ang = math.radians(20 + k * 14)
            pts = [(sx * 2.0, 24.0, 0.0 + k * 0.6)]
            for j in range(1, 7):
                t = j / 6
                pts.append((sx * (2.0 + 16.0 * math.sin(t * math.pi * 0.9) * math.cos(ang - 0.3)),
                            24.0 + 18.0 * math.sin(t * math.pi * 0.6) - 26.0 * t * t,
                            (k - 2) * 1.6 + 4.0 * math.sin(t * 3.0)))
            coil(m, bd, pts, 3)
            spike(m, bd, pts[2], (sx * 0.4, 1, 0), 1.0, 2.6, solid(P, "bud"), tip=0.3)
            spike(m, bd, pts[-1], (0, -1, 0), 1.0, 3.0, solid(P, "violet"), tip=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # arms + spiky seed-balls
        ab = m.bone(nm, bd, (sx * 4.0, 16.0, -1.0))
        rod(m, ab, (sx * 4.0, 16.0, -1.0), (sx * 7.0, 10.0, -4.0), 2, ROOT, extend=0.4)
        m.round_box(ab, sx * 6.0, -3.0, 1.6, 1.6, 12.0, 13.0, solid(P, "band"), cut=0)
        ball(m, ab, (sx * 7.0, 7.0, -5.0), 2.6, fur(P, "seed", "seed_dark", length=1.0, density=2.0), layers=3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        m.bone(nm, top, (sx * 2.0, 12.0, 0))
    return m
