"""Dondokomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
festival drum. A round taiko drum for a body, its top a pale drumhead ringed with silver studs, a red-and-grey band
painted with a festival glyph, an orange belly with a jagged grinning face and big eyes, little purple clawed legs,
and two long dark drumsticks tipped with white balls and trailing red and grey ribbons. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a round taiko drum body with a studded drumhead, a red festival band, an orange grinning face, little purple "
        "legs and two ribboned drumsticks")
BASE = {"head": (240, 232, 214), "head_dark": (190, 180, 160), "red": (210, 40, 40), "red_dark": (130, 14, 18),
        "grey": (180, 180, 190), "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "orange": (240, 140, 40),
        "orange_dark": (180, 80, 10), "black": (30, 26, 26), "white": (250, 250, 250), "purple": (80, 60, 110),
        "purple_dark": (40, 26, 60), "stick": (60, 40, 70), "claw": (220, 220, 230)}
SHINY = {"red": (40, 120, 200), "red_dark": (10, 60, 120), "orange": (120, 200, 90), "orange_dark": (60, 130, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up":
        return tone(p["head"], face), None
    if y > 15.0:
        if face == "north" and abs(x) < 1.8 and 16.0 < y < 19.0 and (abs(x) < 0.3 or abs(y - 17.5) < 0.3):
            return tone(p["black"], face), None                         # the festival glyph
        return tone(p["grey"] if y > 19.6 else p["red"], face), None
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.6, y - 12.0) < 1.2:
                return tone(p["white"] if math.hypot(x - sx * 2.6, y - 12.0) > 0.5 else p["black"], face), None
        if 6.0 < y < 9.6 and abs(x) < 5.0:
            tooth = abs(((x * 0.7) % 2.0) - 1.0) * 1.4
            if y < 6.6 + tooth or y > 9.0 - tooth:
                return tone(p["white"], face), None
            return tone(p["black"], face), None
    return skin(P, "orange", dark="orange_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dondokomon")
    top = m.bone("dondokomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    for i, (r, y0) in enumerate(((6.0, 4.0), (7.4, 7.0), (8.0, 10.0), (8.0, 13.0), (8.0, 16.0), (7.6, 19.0))):
        m.round_box(bd, 0, 0, r, r, y0, y0 + 3.2, bodyf, cut=max(1, round(r * 0.35)))
    hd = m.bone("head", bd, (0, 22, 0))
    for i in range(12):                                                         # silver studs on the rim
        ang = 2 * math.pi * i / 12
        m.round_box(hd, 7.4 * math.sin(ang), -7.4 * math.cos(ang), 0.6, 0.6, 21.6, 22.6,
                    metal(P, "steel", dark="steel_dark"), cut=0)
    for sx, nm, ang in ((1, "arm_left", 40), (-1, "arm_right", -30)):          # drumsticks
        ab = m.bone(nm, bd, (sx * 8.0, 14.0, 0))
        tip = (sx * 18.0, 28.0 + (5 if sx > 0 else 0), -2.0)
        rod(m, ab, (sx * 6.0, 10.0, 0), tip, 1, solid(P, "stick"), extend=0, t2=2)
        m.round_box(ab, tip[0], tip[2], 2.4, 2.4, tip[1] - 2.0, tip[1] + 2.6, solid(P, "white"), cut=1)
        for j, key in enumerate(("red", "grey")):                               # trailing ribbons
            rp = [(tip[0], tip[1] - 2.0, tip[2]), (tip[0] - sx * (3.0 + j * 2), tip[1] + 2.0 + j * 2, tip[2] + 3.0),
                  (tip[0] - sx * (5.0 + j * 2), tip[1] + 5.0, tip[2] + 6.0)]
            for p0, p1 in zip(rp, rp[1:]):
                rod(m, ab, p0, p1, 1, fabric(P, key, key if key != "red" else "red_dark"), extend=0.3, t2=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                         # little purple legs
        lg = m.bone(nm, top, (sx * 3.0, 5.0, 0))
        rod(m, lg, (sx * 3.0, 6.0, 0), (sx * 4.0, 1.0, -1.0), 2, skin(P, "purple", dark="purple_dark"), extend=0.4)
        for j in range(2):
            spike(m, lg, (sx * 4.0 + (j - 0.5) * 1.0, 0.6, -1.6), (0, -0.2, -1), 0.9, 2.0, solid(P, "claw"), tip=0.25)
    return m
