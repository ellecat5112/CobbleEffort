"""Ambromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a cheerful pink radish spirit. A round magenta body that is all face, laughing eyes and an open
grin, a spray of long green leaves on top, stubby arms, red booted feet and a golden staff topped with a crescent
and a gold sunburst cross. 25 blocks tall.

Front is -z, y is up. 38 units tall (the staff); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, metal, mix, plane, skin, solid
from _route import pal, tone

HEIGHT = 38
SCALE, HITBOX = sized(25, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 20}
LOOK = ("a cheerful pink radish spirit: a round magenta face-body with laughing eyes, a spray of long green leaves, "
        "red boots and a golden staff with a crescent and sunburst cross")
BASE = {"pink": (226, 70, 170), "pink_dark": (150, 30, 110), "pink_light": (255, 170, 220), "leaf": (90, 170, 60),
        "leaf_dark": (40, 100, 30), "red": (220, 40, 50), "red_dark": (140, 20, 30), "gold": (240, 190, 60),
        "gold_dark": (170, 120, 30), "gold_light": (255, 240, 170), "mouth": (110, 20, 40), "tongue": (240, 110, 140),
        "eye": (40, 16, 30), "white": (250, 250, 250)}
SHINY = {"pink": (240, 236, 220), "pink_dark": (190, 180, 160), "pink_light": (255, 255, 250), "leaf": (60, 150, 200),
         "leaf_dark": (20, 80, 140)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "pink", dark="pink_dark", light="pink_light", var=0.04)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
RED = skin(P, "red", dark="red_dark", var=0.03)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):                                       # laughing eyes: closed arcs
            du, dv = a - sx * 2.8, b - 18.0
            if abs(math.hypot(du, dv + 0.8) - 1.2) < 0.28 and dv > -0.6:
                return p["eye"], None
        du, dv = a, b - 14.0
        if (du / 3.2) ** 2 + (dv / 2.0) ** 2 < 1 and dv < 0.6:
            return (p["tongue"] if dv < -0.8 else p["mouth"]), None
        for sx in (-1, 1):
            if math.hypot(a - sx * 4.6, b - 15.6) < 1.0:
                return mix(p["pink"], p["pink_light"], 0.6), None      # blush
    return BODY(x, y, z, face, variant, box=box, **k)


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u - W / 2) < 0.25 or abs(abs(u - W / 2) - (v % 1.6) * 0.5) < 0.15:
        return tone(p["leaf_dark"], face), None
    return tone(p["leaf"], face), None


def build():
    m = Model("ambromon")
    top = m.bone("ambromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 15.0, 0), 7.6, facef, layers=8, ry=7.2)
    spike(m, bd, (0, 7.8, 0), (0, -1, 0), 2.0, 2.4, BODY)          # root tip
    cp = m.bone("cap", bd, (0, 22, 0))
    for i in range(7):                                             # long leaves fanning up
        ang = math.radians(-54 + i * 18)
        b = (0.6 * math.sin(ang), 21.6, 0.4)
        tip = (b[0] + 9.0 * math.sin(ang), 21.6 + 9.0 * math.cos(ang), 0.4 + 1.0 * abs(math.sin(ang)))
        rod(m, cp, b, tip, 3, leaff, extend=0.3, t2=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 14.0, 0))
        hand = (sx * 10.5, 12.5, -1.0)
        rod(m, ab, (sx * 7.0, 14.0, 0), hand, 2, BODY, extend=0.3)
        m.round_box(ab, hand[0], hand[2], 1.4, 1.4, hand[1] - 1.2, hand[1] + 1.4, BODY, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 8.0, 0))
        rod(m, lg, (sx * 3.0, 8.5, 0), (sx * 3.4, 3.0, 0), 2, BODY, extend=0.3)
        m.round_box(lg, sx * 3.4, -0.8, 2.0, 2.6, 0.0, 3.4, RED, cut=1)              # red boots
        m.box(lg, sx * 3.4 - 2.2, 3.0, -3.0, sx * 3.4 + 2.2, 4.0, 1.6, solid(P, "white"))
    ar = "arm_left"
    sx = 1
    st = m.bone("staff", ar, (10.5, 12.5, -1.0))                   # the golden staff
    rod(m, st, (10.5, 2.0, -1.0), (10.5, 32.0, -1.0), 1, GOLD, extend=0.2)
    for ang in range(0, 360, 45):                                  # sunburst cross
        r = math.radians(ang)
        ln = 3.2 if ang % 90 == 0 else 2.0
        rod(m, st, (10.5, 30.0, -1.0), (10.5 + ln * math.cos(r), 30.0 + ln * math.sin(r), -1.0), 1, GOLD,
            extend=0.2)
    m.round_box(st, 10.5, -1.0, 1.2, 1.2, 29.0, 31.0, solid(P, "red"), cut=1)
    for i in range(6):                                             # crescent above it
        ang = math.radians(200 + i * 28)
        c = (10.5 + 2.8 * math.cos(ang), 36.0 + 2.8 * math.sin(ang), -1.0)
        m.box(st, c[0] - 0.6, c[1] - 0.6, c[2] - 0.5, c[0] + 0.6, c[1] + 0.6, c[2] + 0.5, GOLD)
    return m
