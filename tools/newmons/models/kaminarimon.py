"""Kaminarimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the winning children's drawing shown
on wikimon.net): the thunder festival imp: a big round orange-pink face with a fierce festival mask (heavy black brows,
a grimacing white mouth with black bars), grey robot limbs with pincer hands, white feet and a golden round fan of
thunder on its back. Child stage (no level on wikimon), 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a big round orange-pink festival-mask face with heavy black brows and a grimacing mouth on grey robot limbs, with a golden fan"
BASE = {"face": (240, 160, 120), "face_dark": (200, 110, 80), "black": (30, 30, 34), "white": (250, 250, 250),
        "grey": (160, 160, 170), "grey_dark": (90, 90, 100), "gold": (250, 210, 60), "gold_dark": (190, 140, 20)}
SHINY = {"face": (150, 200, 240), "face_dark": (90, 140, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 17.6 < y < 18.6 and 0.8 < abs(x) < 4.6:
            return tone(p["black"], face), None
        for sx in (-1, 1):
            if abs(x - sx * 2.6) < 0.8 and abs(y - 16.4) < 0.4:
                return tone(p["black"], face), None
        if 10.6 < y < 13.6 and abs(x) < 4.0:
            if abs(y - 12.1) < 0.3 or (x + 5.0) % 2.0 < 0.3:
                return tone(p["black"], face), None
            return tone(p["white"], face), None
        if 7.6 < y < 9.6 and abs(x) < 0.4:
            return tone(p["black"], face), None
    return skin(P, "face", dark="face_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kaminarimon")
    top = m.bone("kaminarimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 7.0, 4.0, 6.0, 22.0, facef, cut=3)                         # the big round face-body
    hd = m.bone("head", bd, (0, 22, 0))
    fb = m.bone("spin_fan", bd, (0, 16, 5))                                         # golden fan of thunder
    for i in range(10):
        ang = 360.0 * i / 10
        m.box(fb, -1.4, 16.0, 4.6, 1.4, 26.0, 4.6, metal(P, "gold", dark="gold_dark"), rotation=(0, 0, ang),
              pivot=(0, 16.0, 4.6))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # grey robot arms
        ab = m.bone(nm, bd, (sx * 7.0, 14.0, 0))
        rod(m, ab, (sx * 7.0, 14.0, 0), (sx * 10.0, 10.0, -1.0), 1, metal(P, "grey", dark="grey_dark"), extend=0.3, t2=1)
        m.round_box(ab, sx * 10.0, -1.0, 1.0, 1.0, 9.0, 11.0, metal(P, "grey", dark="grey_dark"), cut=0)
        for j in (-1, 1):
            rod(m, ab, (sx * 10.0, 9.4, -1.0), (sx * 10.6 + j * 0.8, 7.0, -1.6), 1, metal(P, "grey", dark="grey_dark"),
                extend=0, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 6.0, 0))
        rod(m, lg, (sx * 3.0, 6.4, 0), (sx * 3.4, 2.0, 0), 1, metal(P, "grey", dark="grey_dark"), extend=0.3, t2=1)
        m.round_box(lg, sx * 3.6, -1.0, 1.6, 2.2, 0.0, 2.0, solid(P, "white"), cut=0)
    return m
