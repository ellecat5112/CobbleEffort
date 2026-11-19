"""Yo!Yo!mon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a living yo-yo: a round blue face with a sly grin and one fang set in a big red yo-yo body with a
string loop on top, thin steel limbs, red sneakers with yellow stars, and two more star yo-yos swinging on its
strings, one spiked. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 37
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a living yo-yo: a round blue grinning face in a red yo-yo body, thin steel limbs, red star sneakers and two star yo-yos on strings"
BASE = {"red": (210, 40, 40), "red_dark": (130, 14, 14), "blue": (50, 80, 190), "blue_dark": (20, 40, 110),
        "yellow": (250, 210, 50), "steel": (190, 194, 206), "steel_dark": (90, 94, 106), "eye": (250, 220, 60),
        "mouth": (30, 20, 30), "white": (255, 255, 255)}
SHINY = {"red": (60, 160, 90), "red_dark": (20, 90, 40), "blue": (230, 150, 60), "blue_dark": (160, 90, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(b - 22.0 + sx * a * 0.15) < 0.6 and 0.8 < sx * a < 3.0:
                return p["eye"], None
        if abs(b - 17.4 - 0.1 * a * a) < 0.35 and abs(a) < 3.0:
            return p["mouth"], None
        if 1.0 < a < 1.6 and 16.2 < b < 17.4:
            return p["white"], None
    return skin(P, "blue", dark="blue_dark")(x, y, z, face, variant, box=box, **k)


def staryo(m, bone, c, spiked):
    x, y, z = c
    m.round_box(bone, x, z, 2.6, 0.8, y - 2.6, y + 2.6, solid(P, "red"), cut=0)
    for k in range(5):
        a = math.pi / 2 + k * 2 * math.pi / 5
        m.box(bone, x + 1.2 * math.cos(a) - 0.5, y + 1.2 * math.sin(a) - 0.5, z - 1.0, x + 1.2 * math.cos(a) + 0.5,
              y + 1.2 * math.sin(a) + 0.5, z - 0.8, solid(P, "yellow"))
    if spiked:
        for k in range(6):
            a = k * math.pi / 3
            spike(m, bone, (x + 2.4 * math.cos(a), y + 2.4 * math.sin(a), z), (math.cos(a), math.sin(a), 0), 0.8, 2.0,
                  metal(P, "steel"), tip=0.8)


def build():
    m = Model("yoyomon")
    top = m.bone("yoyomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 8.0, 4.0, 12.0, 28.0, skin(P, "red", dark="red_dark"), cut=4)      # yo-yo halves
    m.round_box(bd, 0, -2.0, 6.0, 2.6, 14.0, 26.0, facef, cut=2)
    for j in range(8):                                                                  # string loop on top
        ang = j * 2 * math.pi / 8
        m.box(bd, 1.6 * math.cos(ang) - 0.3, 30.0 + 1.6 * math.sin(ang) - 0.3, -0.3, 1.6 * math.cos(ang) + 0.3,
              30.0 + 1.6 * math.sin(ang) + 0.3, 0.3, metal(P, "steel"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 20.0, 0))
        rod(m, ab, (sx * 7.0, 20.0, 0), (sx * 11.0, 26.0 if sx > 0 else 14.0, -2.0), 1, metal(P, "steel"), extend=0.2)
        h = (sx * 11.0, 26.0 if sx > 0 else 14.0, -2.0)
        rod(m, ab, h, (h[0] + sx * 2.0, h[1] + (6.0 if sx > 0 else -8.0), h[2]), 1, solid(P, "steel_dark"), extend=0.0)
        staryo(m, ab, (h[0] + sx * 2.0, h[1] + (8.0 if sx > 0 else -10.0), h[2]), spiked=sx > 0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 12.0, 0))
        rod(m, lg, (sx * 3.0, 12.0, 0), (sx * 3.4, 2.4, 0), 1, metal(P, "steel"), extend=0.2)
        m.round_box(lg, sx * 3.4, -1.2, 1.8, 3.0, 0.0, 2.4, solid(P, "red"), cut=1)
        m.box(lg, sx * 3.4 - 0.6, 1.0, -4.3, sx * 3.4 + 0.6, 2.0, -4.0, solid(P, "yellow"))
    return m
