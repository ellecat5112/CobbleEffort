"""Gulfmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Demon Lord chimera born of corrupted data: a hulking beast-body of shaggy dark violet fur on
silver-armoured clawed legs, great brown feathered wings, a goat-horned skull helm atop a grey armoured humanoid
torso, a pale fang-ringed maw in its chest and a huge crescent blade-claw. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digidetail import armour, feathers, fur, metal, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a hulking chimera of shaggy dark violet fur on silver-armoured legs, brown feathered wings, a goat-horned skull "
        "helm, a fanged chest maw and a crescent blade-claw")
BASE = {"violet": (80, 60, 90), "violet_dark": (36, 24, 44), "violet_light": (150, 120, 160), "silver": (200, 204, 216),
        "silver_dark": (100, 104, 116), "gold": (220, 180, 70), "wing": (130, 100, 80), "wing_dark": (70, 50, 36),
        "bone": (230, 224, 210), "maw": (60, 20, 30), "tooth": (250, 240, 200), "claw": (40, 40, 60), "eye": (230, 40, 40)}
SHINY = {"violet": (180, 170, 150), "violet_dark": (110, 100, 80), "violet_light": (230, 220, 200)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "violet", "violet_dark", tip="violet_light", length=2.0, density=1.8)
SILVER = armour(P, "silver", "silver_dark", trim="gold", trim_w=0.3)


def build():
    m = Model("gulfmon")
    top = m.bone("gulfmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    m.round_box(bd, 0, 2.0, 11.0, 13.0, 16.0, 34.0, FUR, cut=4)                            # shaggy beast-body
    m.box(bd, -5.0, 20.0, -11.2, 5.0, 28.0, -10.8, solid(P, "maw"))                           # fanged chest maw
    for j in range(5):
        spike(m, bd, (-4.0 + j * 2.0, 28.0, -11.0), (0, -1, 0), 1.0, 2.6, solid(P, "tooth"), tip=0.8)
        spike(m, bd, (-4.0 + j * 2.0, 20.0, -11.0), (0, 1, 0), 1.0, 2.0, solid(P, "tooth"), tip=0.8)
    for sx, nm, z in ((1, "leg_front_left", -8.0), (-1, "leg_front_right", -8.0), (1, "leg_back_left", 9.0),
                      (-1, "leg_back_right", 9.0)):
        lg = m.bone(nm, bd, (sx * 8.0, 18.0, z))
        rod(m, lg, (sx * 8.0, 20.0, z), (sx * 10.0, 8.0, z - 2.0), 5, SILVER, extend=0.6)
        rod(m, lg, (sx * 10.0, 8.0, z - 2.0), (sx * 10.0, 2.0, z - 1.0), 4, SILVER, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 10.0 + (j - 1) * 1.6, 1.0, z - 4.0), (0, -0.3, -1), 1.4, 4.0, solid(P, "claw"), tip=0.8)
    tor = m.bone("torso", bd, (0, 34, -4))                                                     # humanoid torso
    m.round_box(tor, 0, -4.0, 5.0, 3.4, 34.0, 46.0, SILVER, cut=1)
    hd = m.bone("head", tor, (0, 46, -4))
    m.round_box(hd, 0, -4.4, 2.6, 2.8, 46.0, 52.0, metal(P, "bone", dark="silver_dark"), cut=1)  # skull helm
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 49.0, -7.3, max(sx * 0.6, sx * 1.8), 49.8, -7.1, solid(P, "eye", glow=True))
        pts = [(sx * 2.4, 51.6, -4.0), (sx * 6.0, 55.0, -3.0), (sx * 7.0, 52.0, -1.0), (sx * 5.4, 49.0, -2.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                       # curled goat horns
            rod(m, hd, p0, p1, 1, metal(P, "bone", dark="silver_dark"), extend=0.3, t2=2)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 6.0, 34.0, 6.0))
        feather_wing(m, wb, (side * 6.0, 34.0, 6.0), 26.0, 12.0, 3, feathers(P, "wing", "wing_dark"), side=side,
                     sweep=25, droop=-8.0)
    ab = m.bone("arm_right", tor, (-5.0, 44.0, -4.0))                                            # crescent blade-claw
    rod(m, ab, (-5.0, 44.0, -4.0), (-10.0, 38.0, -10.0), 2, SILVER, extend=0.4)
    pts = [(-10.0, 38.0, -10.0), (-16.0, 42.0, -12.0), (-20.0, 36.0, -12.0), (-18.0, 30.0, -11.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, ab, p0, p1, 1, metal(P, "silver", dark="silver_dark"), extend=0.3, t2=3)
    return m
