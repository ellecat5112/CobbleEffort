"""Daxiongmaoshou (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the little panda. A round chubby panda with black ears, eye patches, arms and legs, a tuft of
white hair on top, a sprig of bamboo leaves in its mouth, a red Chinese-style vest with gold toggles and a long blue
scarf trailing over its shoulder. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, local, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = ("a round chubby panda with black eye patches, a white tuft, bamboo leaves in its mouth, a red vest with gold "
        "toggles and a long blue scarf")
BASE = {"white": (246, 246, 244), "white_dark": (200, 200, 204), "black": (40, 40, 44), "black_dark": (14, 14, 18),
        "red": (210, 40, 40), "red_dark": (130, 14, 18), "blue": (40, 80, 200), "blue_dark": (16, 36, 120),
        "gold": (240, 200, 70), "leaf": (90, 170, 70), "stem": (110, 140, 60), "eye": (60, 40, 30),
        "nose": (30, 24, 26), "shine": (255, 255, 255)}
SHINY = {"black": (130, 80, 50), "black_dark": (70, 40, 20), "red": (60, 160, 90), "red_dark": (20, 90, 40)}


def P(v):
    return pal(BASE, SHINY, v)


WFUR = fur(P, "white", "white_dark", length=1.2, density=2.6)
BFUR = fur(P, "black", "black_dark", length=1.2, density=2.6)
VEST = fabric(P, "red", "red_dark", axis="y", period=1.6)
SCARF = fabric(P, "blue", "blue_dark", axis="x", period=1.4)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot((x - sx * 2.2) * 0.9, (y - 22.6 + (x - sx * 2.2) * sx * 0.25))
            if d < 0.55:
                return tone(p["shine"] if x * sx > 2.4 and y > 22.8 else p["eye"], face), None
            if d < 1.7:
                return tone(p["black"], face), None                 # eye patch
        if abs(x) < 0.7 and 20.4 < y < 21.2:
            return tone(p["nose"], face), None
    return WFUR(x, y, z, face, variant, box=box, **k)


def vestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 0.6 and any(abs(y - yy) < 0.35 for yy in (11.5, 13.5, 15.5)):
        return tone(p["gold"], face), None
    return VEST(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("daxiongmaoshou")
    top = m.bone("daxiongmaoshou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 11.0, 0), 6.0, WFUR, layers=6, squash=0.9)                       # round belly
    m.round_box(bd, 0, 0, 5.8, 5.2, 9.6, 17.0, vestf, cut=2)                          # red vest
    hd = m.bone("head", bd, (0, 17, 0))
    m.round_box(hd, 0, -0.2, 5.6, 4.8, 17.0, 26.6, headf, cut=2)
    m.round_box(hd, 0, -4.8, 1.8, 1.0, 19.6, 21.6, WFUR, cut=1)                       # muzzle
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.4, 0.6, 1.6, 1.2, 25.4, 28.4, BFUR, cut=1)            # ears
    for i in range(5):                                                                 # white tuft
        spike(m, hd, ((i - 2) * 0.6, 26.4, 0.4), ((i - 2) * 0.3, 1, 0.2), 0.8, 2.0, WFUR)
    rod(m, hd, (-1.0, 20.6, -5.6), (-5.0, 22.6, -6.0), 1, solid(P, "stem"), extend=0)  # bamboo sprig
    m.box(hd, -9.0, 21.6, -6.0, -4.4, 24.0, -6.0, solid(P, "leaf"), rotation=(0, 0, 20), pivot=(-5.0, 22.6, -6.0))
    m.round_box(bd, 0, 0, 6.2, 5.4, 16.0, 18.0, SCARF, cut=2)                         # blue scarf
    sb = m.bone("scarf", bd, (3, 17, -4))
    m.box(sb, 2.0, 8.0, -5.6, 4.6, 17.0, -4.8, SCARF, rotation=(-10, 0, 10), pivot=(3.0, 17.0, -5.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.4, 15.0, 0))
        rod(m, ab, (sx * 5.0, 15.0, 0), (sx * 7.6, 10.6, -1.0), 3, BFUR, extend=0.6)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 6.0, 0))
        m.round_box(lg, sx * 3.0, -0.4, 2.4, 2.6, 0.0, 6.4, BFUR, cut=1)
    return m
