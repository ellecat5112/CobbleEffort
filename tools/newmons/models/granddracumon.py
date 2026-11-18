"""Grand Dracumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the vampire king and his mount: a crimson-armoured vampire lord with long blond hair,
a horned violet mask and great grey bat wings, sitting astride a hulking crimson beast whose chest gapes open in a
huge toothed maw with a pink tongue, bound with red straps, standing on black clawed legs with white talons.
35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digidetail import armour, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a crimson vampire lord with long blond hair, a horned violet mask and grey bat wings astride a hulking crimson "
        "beast with a huge toothed maw in its chest")
BASE = {"crimson": (140, 30, 40), "crimson_dark": (70, 10, 16), "crimson_light": (200, 80, 90), "black": (34, 32, 38),
        "black_dark": (12, 12, 16), "violet": (110, 100, 190), "violet_dark": (50, 44, 110), "hair": (240, 210, 100),
        "hair_dark": (180, 140, 40), "wing": (110, 110, 120), "wing_dark": (60, 60, 66), "talon": (240, 240, 246),
        "maw": (90, 20, 50), "tooth": (250, 250, 240), "tongue": (230, 120, 170), "red": (200, 30, 40),
        "eye": (230, 40, 40)}
SHINY = {"crimson": (40, 60, 120), "crimson_dark": (14, 24, 60), "crimson_light": (100, 130, 200)}


def P(v):
    return pal(BASE, SHINY, v)


CRIM = skin(P, "crimson", dark="crimson_dark", light="crimson_light")
ARM = armour(P, "crimson", "crimson_dark", light="crimson_light", trim="black", trim_w=0.3)


def build():
    m = Model("granddracumon")
    top = m.bone("granddracumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 0, 9.0, 13.0, 14.0, 32.0, CRIM, cut=3)                             # hulking beast body
    m.box(bd, -7.0, 16.0, -13.4, 7.0, 28.0, -12.8, solid(P, "maw"))                        # chest maw
    for j in range(7):
        spike(m, bd, (-6.0 + j * 2.0, 28.0, -13.2), (0, -1, -0.1), 1.0, 3.0, solid(P, "tooth"), tip=0.8)
        spike(m, bd, (-6.0 + j * 2.0, 16.0, -13.2), (0, 1, -0.1), 1.0, 2.6, solid(P, "tooth"), tip=0.8)
    rod(m, bd, (0, 18.0, -13.0), (2.0, 12.0, -18.0), 3, skin(P, "tongue", dark="maw"), extend=0.4, t2=2)
    for j in range(3):
        m.round_box(bd, 0, -2.0 + j * 6.0, 9.4, 13.4 if j == 1 else 1.0, 20.0 + j * 2.0, 21.4 + j * 2.0,
                    leather(P, "red", "crimson_dark"), cut=1)
    for sx, nm, z in ((1, "leg_front_left", -8.0), (-1, "leg_front_right", -8.0), (1, "leg_back_left", 8.0),
                      (-1, "leg_back_right", 8.0)):
        lg = m.bone(nm, bd, (sx * 8.0, 18.0, z))
        rod(m, lg, (sx * 8.0, 20.0, z), (sx * 10.0, 8.0, z - 2.0), 5, CRIM, extend=0.6)
        rod(m, lg, (sx * 10.0, 8.0, z - 2.0), (sx * 10.0, 2.0, z - 3.0), 4, leather(P, "black", "black_dark"), extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 10.0 + (j - 1) * 1.6, 1.0, z - 5.0), (0, -0.2, -1), 1.2, 4.0, solid(P, "talon"), tip=0.8)
    rb = m.bone("rider", bd, (0, 32, 2))                                                     # the vampire lord
    m.round_box(rb, 0, 2.0, 4.0, 3.0, 32.0, 44.0, ARM, cut=1)
    m.round_box(rb, 0, 2.0, 5.6, 3.4, 42.0, 46.0, ARM, cut=1)
    hd = m.bone("head", rb, (0, 46, 2))
    m.round_box(hd, 0, 1.6, 2.6, 2.8, 46.0, 52.0, skin(P, "crimson_light", dark="crimson"), cut=1)
    m.round_box(hd, 0, -1.0, 2.8, 0.6, 49.0, 52.0, metal(P, "violet", dark="violet_dark"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 50.0, -1.7, max(sx * 0.6, sx * 1.8), 50.6, -1.5, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 52.0, 1.0), (sx * 0.5, 1, 0.2), 1.4, 6.0, metal(P, "violet", dark="violet_dark"), tip=0.8)
    for i in range(10):                                                                        # long blond hair
        ang = math.radians(-120 + i * 26)
        rod(m, hd, (2.4 * math.sin(ang), 51.0, 1.6 + 2.0 * math.cos(ang) + 1.0), (3.6 * math.sin(ang), 40.0, 7.0), 1,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, rb, (sx * 5.0, 44.0, 2.0))
        rod(m, ab, (sx * 5.0, 44.0, 2.0), (sx * 8.0, 36.0, -3.0), 2, ARM, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 8.0 + (j - 1) * 0.7, 35.0, -3.6), (0, -0.6, -1), 0.6, 2.4, solid(P, "talon"), tip=0.8)
    for side in (1, -1):                                                                        # great bat wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", rb, (side * 4.0, 44.0, 5.0))
        bat_wing(m, wb, (side * 4.0, 44.0, 5.0), 22.0, 16.0, 4, metal(P, "black", dark="black_dark"),
                 skin(P, "wing", dark="wing_dark"), side=side, sweep=15)
    return m
