"""Chackmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Hybrid of ice, as a child warrior. A stout white polar-bear cub in an olive helmet with a bear
badge, an olive armoured vest with a snowflake emblem, orange-and-olive armoured boots and gauntlets, and a boxy olive
snowball launcher on its shoulder, with a flurry of snowflakes round it. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, cutout, fur, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a stout white polar-bear cub in an olive helmet and armoured vest, orange-and-olive boots and a boxy "
        "snowball launcher on its shoulder")
BASE = {"white": (246, 246, 252), "white_dark": (190, 196, 214), "olive": (130, 130, 60), "olive_dark": (70, 70, 26),
        "olive_light": (190, 190, 110), "orange": (240, 130, 60), "orange_dark": (170, 70, 20), "red": (220, 50, 40),
        "eye": (40, 30, 30), "black": (30, 30, 36), "snow": (230, 240, 255, 190), "badge": (250, 200, 120)}
SHINY = {"olive": (60, 90, 140), "olive_dark": (24, 40, 80), "olive_light": (130, 160, 210), "orange": (230, 230, 240)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=1.0)
OLIVE = armour(P, "olive", "olive_dark", light="olive_light", rivets=True)
ORANGE = armour(P, "orange", "orange_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.0) < 0.6 and abs(y - 29.4) < 0.5:
                return tone(p["eye"], face), None
        if abs(x + 3.4) < 0.4 and 27.4 < y < 29.0:
            return tone(p["red"], face), None                              # warpaint stripe
    return FUR(x, y, z, face, variant, box=box, **k)


def vestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, y - 19.0) < 2.0:
        if abs(x) < 0.25 or abs(y - 19.0) < 0.25 or abs(abs(x) - abs(y - 19.0)) < 0.25:
            return tone(p["white"], face), None                            # snowflake emblem
        return tone(p["olive_dark"], face), None
    return OLIVE(x, y, z, face, variant, box=box, **k)


def snowin(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u - W / 2, v - H / 2
    r = math.hypot(a, b)
    ang = math.atan2(b, a)
    return r < W / 2 and (abs(math.sin(ang * 3)) < 0.25 or r < W * 0.15)


def build():
    m = Model("chackmon")
    top = m.bone("chackmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 5.6, 4.6, 10.0, 24.0, vestf, cut=2)                     # stout body in the vest
    hd = m.bone("head", bd, (0, 24, 0))
    ball(m, hd, (0, 29.0, -0.4), 5.6, headf, layers=5)
    m.box(hd, -2.0, 25.4, -6.6, 2.0, 28.0, -4.6, FUR)                              # muzzle
    m.box(hd, -0.6, 27.0, -6.8, 0.6, 27.8, -6.5, solid(P, "black"))
    m.round_box(hd, 0, -0.2, 6.0, 5.6, 31.0, 35.2, OLIVE, cut=2)                   # helmet
    m.box(hd, -1.2, 32.0, -5.8, 1.2, 34.0, -5.5, solid(P, "badge"))
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.2, 0, 1.6, 1.4, 34.0, 37.4, FUR, cut=1)            # bear ears through the helmet
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.6, 21.0, 0))
        rod(m, ab, (sx * 5.6, 21.0, 0), (sx * 7.6, 15.0, -2.0), 4, FUR, extend=0.4)
        m.round_box(ab, sx * 7.8, -2.4, 2.4, 2.4, 11.0, 15.4, ORANGE, cut=1)       # gauntlets
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 10.0, 0))
        m.round_box(lg, sx * 3.2, 0, 2.6, 2.6, 4.0, 11.0, OLIVE, cut=1)
        m.round_box(lg, sx * 3.2, -1.0, 3.0, 3.6, 0.0, 4.6, ORANGE, cut=1)       # boots
    al = m.bone("launcher", bd, (5, 24, 0))                                        # the snowball launcher
    m.box(al, 3.0, 24.0, -8.0, 10.0, 30.0, 4.0, OLIVE)
    for i in range(4):
        m.box(al, 4.0 + (i % 2) * 3.0, 25.0 + (i // 2) * 2.6, -8.4, 6.0 + (i % 2) * 3.0, 27.0 + (i // 2) * 2.6,
              -8.0, solid(P, "black"))
    sb = m.bone("snow", bd, (-8, 24, 0))
    for j, (c, s) in enumerate((((-10.0, 30.0, -2.0), 4.0), ((-12.0, 22.0, 0.0), 3.0), ((-9.0, 16.0, -3.0), 2.4))):
        m.box(sb, c[0] - s, c[1] - s, c[2], c[0] + s, c[1] + s, c[2], cutout(snowin, solid(P, "snow")),
              rotation=(0, 20 * j, 0), pivot=c)
    return m
