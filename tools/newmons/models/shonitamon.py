"""Shonitamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Shoutmon fused with a Monitamon: a little red dragon body in a green ammo belt, the head a red
pointed ninja-hood over a grey monitor face with a goofy grin and a green lens, big white cartoon gloves and white
clawed feet. 15 blocks. Adult stage.

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little red dragon with a red pointed ninja-hood over a grey monitor face with a goofy grin, a green ammo belt and big white gloves"
BASE = {"red": (220, 50, 40), "red_dark": (130, 20, 14), "grey": (170, 174, 186), "grey_dark": (90, 94, 108),
        "green": (70, 140, 60), "green_dark": (30, 80, 24), "white": (250, 250, 250), "black": (30, 30, 34),
        "lens": (90, 230, 120)}
SHINY = {"red": (70, 110, 210), "red_dark": (24, 50, 140)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark")


def screenf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(y - 22.0 - 0.4 * abs(math.sin(x * 2.0))) < 0.3 and abs(x) < 2.0:
            return tone(p["black"], face), None
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.5 and abs(y - 24.6) < 0.5:
                return tone(p["black"], face), None
    return armour(P, "grey", "grey_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("shonitamon")
    top = m.bone("shonitamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 3.4, 2.8, 6.0, 16.0, RED, cut=1)
    m.box(bd, -3.6, 11.0, -3.0, 3.6, 12.6, 3.0, leather(P, "green", "green_dark"), rotation=(0, 0, 25), pivot=(0, 12, 0))
    hd = m.bone("head", bd, (0, 16, 0))
    m.box(hd, -3.4, 18.0, -3.0, 3.4, 27.0, 3.0, RED)                                         # red hood
    m.box(hd, -2.6, 19.0, -3.2, 2.6, 26.0, -2.8, screenf)                                    # monitor face
    m.box(hd, 2.0, 25.0, -3.4, 3.0, 26.0, -3.0, solid(P, "lens", glow=True))
    spike(m, hd, (0, 27.0, 0), (0.4, 1, 0.3), 3.0, 10.0, RED, tip=0.8)                        # pointed hood tip
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 14.0, 0))
        rod(m, ab, (sx * 3.4, 14.0, 0), (sx * 7.0, 11.0, -2.0), 1, RED, extend=0.2, t2=2)
        ball(m, ab, (sx * 8.4, 11.0, -2.6), 2.4, solid(P, "white"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 6.0, 0))
        rod(m, lg, (sx * 1.8, 6.0, 0), (sx * 2.2, 1.4, 0), 2, RED, extend=0.3)
        m.round_box(lg, sx * 2.2, -0.8, 1.6, 2.2, 0.0, 1.8, solid(P, "white"), cut=0)
        for f in range(3):
            spike(m, lg, (sx * 2.2 + (f - 1) * 1.0, 0.6, -2.8), (0, -0.2, -1), 0.8, 1.6, solid(P, "white"), tip=0.8)
    return m
