"""Oblivimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a cyborg flying saucer: a sleek blue disc hull with swept fins, a glass dome holding a pink brain
on top, a ring of glowing cyan lights beneath, and long segmented cable arms dangling from its underside, each ending
in a claw or a spinning blade-orb. 25 blocks wide.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = ("a sleek blue flying-saucer cyborg with swept fins, a glass dome holding a pink brain, glowing cyan lights and "
        "long segmented cable arms ending in claws and blade-orbs")
BASE = {"blue": (40, 90, 200), "blue_dark": (14, 34, 110), "blue_light": (130, 180, 250), "cyan": (120, 240, 250),
        "glass": (190, 230, 250, 130), "brain": (240, 150, 190), "cable": (150, 154, 166), "cable_dark": (70, 74, 86),
        "black": (24, 24, 30), "eye": (250, 220, 50)}
SHINY = {"blue": (200, 60, 60), "blue_dark": (110, 20, 20), "blue_light": (250, 150, 140), "cyan": (250, 230, 100)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "blue", "blue_dark", light="blue_light", trim="black", trim_w=0.3)


def cablef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["cable"] if (y * 1.4) % 1.6 < 1.0 else p["cable_dark"], face), None


def build():
    m = Model("oblivimon")
    top = m.bone("oblivimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    for j, (r, y0, y1) in enumerate(((10.0, 20.0, 22.0), (14.0, 22.0, 24.0), (11.0, 24.0, 26.0))):   # disc hull
        m.round_box(bd, 0, 0, r, r, y0, y1, HULL, cut=max(1, int(r * 0.35)))
    for sx in (-1, 1):                                                                   # swept fins
        x0, x1 = sorted((sx * 8.0, sx * 15.0))
        m.box(bd, x0, 24.0, 4.0, x1, 30.0, 4.6, HULL, rotation=(0, sx * 20, sx * 25), pivot=(sx * 8.0, 25.0, 4.0))
    spike(m, bd, (0, 25.0, 10.0), (0, 1, 1), 1.6, 6.0, HULL, tip=0.8)
    m.round_box(bd, 0, -1.0, 3.0, 3.0, 26.0, 28.0, solid(P, "brain"), cut=1)              # pink brain
    ball(m, bd, (0, 27.0, -1.0), 4.0, solid(P, "glass"), layers=3, ry=3.4)                 # glass dome
    for i in range(10):                                                                  # cyan lights
        ang = 2 * math.pi * i / 10
        m.box(bd, 9.0 * math.cos(ang) - 1.0, 19.6, 9.0 * math.sin(ang) - 1.0, 9.0 * math.cos(ang) + 1.0, 20.2,
              9.0 * math.sin(ang) + 1.0, solid(P, "cyan", glow=True))
    for i in range(4):                                                                   # cable arms
        ang = 2 * math.pi * i / 4 + 0.6
        ab = m.bone("arm_%d" % i, bd, (4.0 * math.cos(ang), 20.0, 4.0 * math.sin(ang)))
        pts = [(4.0 * math.cos(ang), 20.0, 4.0 * math.sin(ang)), (9.0 * math.cos(ang), 12.0, 9.0 * math.sin(ang)),
               (12.0 * math.cos(ang + 0.4), 5.0, 12.0 * math.sin(ang + 0.4))]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, cablef, extend=0.3)
        e = pts[-1]
        if i % 2:
            for f in range(3):
                spike(m, ab, e, (math.cos(ang) * 0.5 + (f - 1) * 0.5, -1, math.sin(ang) * 0.5), 1.0, 3.0,
                      metal(P, "cable"), tip=0.8)
        else:
            ball(m, ab, e, 1.6, HULL, layers=2)
            for f in range(3):
                a2 = 2 * math.pi * f / 3
                spike(m, ab, e, (math.cos(a2), 0, math.sin(a2)), 0.8, 3.0, metal(P, "cable"), tip=0.8)
    return m
