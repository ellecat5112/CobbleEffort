"""Marin Chimairamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the sea chimera: a patchwork beast of sea creatures: a white shark-skull head with blue fins and a red
horn, a dark blue armoured torso, octopus tentacles in crimson and violet for a lower body, a huge red crab claw on
one arm and a hooked anchor-staff on the other. 25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a patchwork sea chimera with a white shark-skull head, a dark blue torso, crimson octopus tentacles, a red crab claw and an anchor staff"
BASE = {"white": (230, 232, 240), "white_dark": (150, 154, 170), "blue": (40, 60, 160), "blue_dark": (14, 20, 80),
        "red": (210, 40, 50), "red_dark": (120, 10, 20), "violet": (130, 40, 90), "violet_dark": (70, 14, 46),
        "steel": (180, 184, 196), "steel_dark": (80, 84, 96), "eye": (100, 200, 250), "tooth": (250, 248, 236)}
SHINY = {"blue": (40, 120, 70), "blue_dark": (14, 60, 30), "red": (230, 170, 40), "red_dark": (150, 100, 10)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("marinchimairamon")
    top = m.bone("marinchimairamon", None, (0, 0, 0))
    tb = m.bone("tail", top, (0, 18, 0))                                              # octopus tentacles
    for i in range(8):
        ang = 2 * math.pi * i / 8
        pts = [(2.0 * math.cos(ang), 20.0, 2.0 * math.sin(ang)), (6.0 * math.cos(ang), 12.0, 6.0 * math.sin(ang)),
               (8.0 * math.cos(ang + 0.4), 4.0, 8.0 * math.sin(ang + 0.4)), (7.0 * math.cos(ang + 0.8), 0.6, 7.0 * math.sin(ang + 0.8))]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tb, p0, p1, 2 - j // 2, skin(P, "red" if i % 2 else "violet", dark="violet_dark"), extend=0.4)
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 0.6, 5.0, 4.0, 20.0, 36.0, armour(P, "blue", "blue_dark", trim="steel", trim_w=0.25), cut=2)
    hd = m.bone("head", bd, (0, 36, -3))
    m.round_box(hd, 0, -6.0, 3.0, 6.0, 35.0, 41.0, skin(P, "white", dark="white_dark"), cut=1)      # shark skull
    m.round_box(hd, 0, -10.0, 2.6, 2.4, 33.6, 35.4, skin(P, "white", dark="white_dark"), cut=1)
    for j in range(6):
        spike(m, hd, (-2.0 + j * 0.8, 35.0, -12.0), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.9, sx * 3.2), 38.6, -9.0, max(sx * 2.9, sx * 3.2), 39.6, -7.6, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.4, 40.0, -2.0), (sx * 0.6, 0.6, 0.8), 1.6, 5.0, solid(P, "blue"), tip=0.8)
    spike(m, hd, (0, 41.0, -6.0), (0, 1, -0.3), 1.4, 5.0, solid(P, "red"), tip=0.8)
    al = m.bone("arm_left", bd, (5.0, 32.0, 0))                                        # huge crab claw
    rod(m, al, (5.0, 32.0, 0), (12.0, 28.0, -4.0), 3, armour(P, "red", "red_dark"), extend=0.6)
    for sgn in (-1, 1):
        pts = [(12.0, 28.0, -4.0), (16.0, 28.0 + sgn * 3.0, -8.0), (18.0, 28.0 + sgn * 1.0, -12.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, al, p0, p1, 2, armour(P, "red", "red_dark"), extend=0.4)
    ar = m.bone("arm_right", bd, (-5.0, 32.0, 0))                                      # anchor staff
    rod(m, ar, (-5.0, 32.0, 0), (-10.0, 28.0, -3.0), 2, skin(P, "blue", dark="blue_dark"), extend=0.4)
    rod(m, ar, (-10.0, 14.0, -3.0), (-10.0, 42.0, -3.0), 1, metal(P, "steel", dark="steel_dark"), extend=0, t2=1)
    for sgn in (-1, 1):
        rod(m, ar, (-10.0, 15.0, -3.0), (-10.0 + sgn * 4.0, 18.0, -3.0), 1, metal(P, "steel", dark="steel_dark"), extend=0, t2=1)
    return m
