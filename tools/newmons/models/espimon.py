"""Espimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little spy robot. A glossy translucent-blue bean-shaped head with round bear ears and big determined eyes, a grinning
gold mouth grille, a white-and-silver armoured body with a red button, stubby silver gun-barrel arms with yellow
fingers, a jetpack with silver nozzles on its back and two blazing jet feet. Child stage, 1 block tall.

Front is -z, y is up. 32 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, cutout, flame_inside, gem, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1.0, HEIGHT, 1.3)
KIND = "floater"
K = 4
LOOK = ("a little spy robot with a glossy blue bean head, bear ears, big eyes, a gold mouth grille, a white armoured body "
        "with a red button, gun-barrel arms and blazing jet feet")
BASE = {"blue": (80, 190, 230), "blue_light": (210, 245, 255), "white": (246, 246, 250), "white_dark": (180, 184, 200),
        "silver": (200, 204, 216), "silver_dark": (100, 104, 118), "gold": (250, 200, 50), "black": (24, 24, 28),
        "red": (220, 40, 40), "red_light": (255, 160, 150), "yellow": (250, 220, 60), "flame": (255, 220, 80, 220),
        "flame_core": (255, 255, 230, 240), "navy": (30, 40, 90)}
SHINY = {"blue": (240, 130, 190), "blue_light": (255, 220, 240)}


def P(v):
    return pal(BASE, SHINY, v)


HEAD = gem(P, "blue", "blue_light", glow=False)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.4, y - 25.0)
            if d < 1.6:
                return tone(p["black"] if d < 1.0 and y > 24.6 else p["white"], face), None
        if abs(y - 23.0) < 0.5 and abs(x) < 1.0:
            return tone(p["navy"], face), None
    return HEAD(x, y, z, face, variant, box=box, **k)


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) > 0.7 else p["flame"]
    return c, c[:3]


def build():
    m = Model("espimon")
    top = m.bone("espimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 5.4, 4.4, 10.0, 18.0, armour(P, "white", "white_dark", trim="silver"), cut=2)
    m.round_box(bd, 0, -4.6, 1.4, 0.6, 12.0, 14.6, gem(P, "red", "red_light"), cut=0)          # red button
    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, 0, 5.4, 4.6, 17.0, 30.0, headf, cut=2)                                    # bean head
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.0, 0, 1.6, 1.4, 29.0, 32.0, HEAD, cut=1)                         # bear ears
    m.box(hd, -3.0, 18.6, -4.8, 3.0, 21.0, -4.4, metal(P, "gold", dark="gold"))                   # mouth grille
    for j in range(5):
        m.box(hd, -2.6 + j * 1.2, 18.6, -4.9, -2.3 + j * 1.2, 21.0, -4.7, solid(P, "black"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                         # gun-barrel arms
        ab = m.bone(nm, bd, (sx * 5.4, 15.0, 0))
        rod(m, ab, (sx * 5.4, 15.0, 0), (sx * 9.0, 15.0, -1.0), 3, metal(P, "silver", dark="silver_dark"), extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 9.4, 15.0 + (j - 1) * 0.8, -1.0), (sx, 0, -0.3), 0.6, 1.6, solid(P, "yellow"))
    jb = m.bone("jetpack", bd, (0, 14, 5))                                                      # jetpack
    m.box(jb, -4.0, 10.0, 4.4, 4.0, 18.0, 6.4, solid(P, "navy"))
    for sx in (-1, 1):
        m.round_box(jb, sx * 6.0, 6.0, 1.2, 1.2, 9.0, 17.0, metal(P, "silver", dark="silver_dark"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                         # blazing jet feet
        lg = m.bone(nm, top, (sx * 2.6, 10.0, 0))
        m.round_box(lg, sx * 2.6, 0, 2.0, 2.0, 6.0, 10.0, metal(P, "silver", dark="silver_dark"), cut=1)
        for ang in (0, 90):
            m.box(lg, sx * 2.6 - 2.0, 0.0, 0, sx * 2.6 + 2.0, 6.0, 0, cutout(flame_inside(3, 0, ang), flamef),
                  rotation=(180, ang, 0), pivot=(sx * 2.6, 3.0, 0))
    return m
