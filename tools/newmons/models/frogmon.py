"""Frogmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
leaf-hat frog. A yellow frog crouching on big clawed feet with a white belly and a wide toothy grin, an orange eye,
a huge glossy green leaf worn as a hat, a red pack on its back with a green pipe-mast turning a leafy propeller, a
brown holster at its hip and spiky green leaf cuffs on its wrists. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, leather, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a yellow crouching frog with a white belly and toothy grin, a glossy green leaf hat, a red back pack with a "
        "leafy propeller, a brown holster and spiky leaf cuffs")
BASE = {"yellow": (250, 220, 40), "yellow_dark": (200, 150, 10), "white": (250, 250, 246), "green": (100, 200, 80),
        "green_dark": (40, 120, 30), "green_light": (200, 250, 160), "red": (210, 40, 30), "red_dark": (120, 14, 10),
        "brown": (150, 110, 70), "brown_dark": (90, 60, 30), "eye": (240, 140, 30), "pupil": (16, 16, 20),
        "mouth": (120, 20, 30), "tooth": (250, 250, 250), "black": (34, 32, 38), "claw": (230, 230, 220)}
SHINY = {"yellow": (120, 220, 250), "yellow_dark": (40, 140, 200), "red": (60, 60, 70), "red_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "yellow", dark="yellow_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 3.6:
        return tone(p["white"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 18.6 < y < 20.4 and abs(x) < 4.6:
            if y > 19.6 and ((x + 5.0) % 1.2) < 0.7:
                return tone(p["tooth"], face), None
            return tone(p["mouth"], face), None
        if y < 18.6:
            return tone(p["white"], face), None
    if face in ("east", "west", "north") and math.hypot(z + 2.0, y - 23.0) < 1.4 and abs(x) > 3.0:
        return tone(p["pupil"] if math.hypot(z + 2.0, y - 23.0) < 0.6 else p["eye"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u - W / 2) < 0.3 or abs(((u - W / 2) * 0.8 + v) % 3.0) < 0.25:
        return tone(p["green_dark"], face), None
    return tone(p["green_light"] if face == "up" and v > H * 0.6 else p["green"], face), None


def build():
    m = Model("frogmon")
    top = m.bone("frogmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.6, 5.4, 4.6, 6.0, 17.0, bodyf, cut=2)
    hd = m.bone("head", bd, (0, 17, -1))
    m.round_box(hd, 0, -1.0, 5.0, 5.0, 16.0, 26.0, headf, cut=2)
    m.round_box(hd, 0, 0.0, 7.6, 8.4, 25.4, 27.0, leaff, cut=3)                       # glossy leaf hat
    spike(m, hd, (0, 26.0, -8.0), (0, -0.8, -0.6), 3.6, 7.0, leaff, tip=0.4)          # drooping leaf tip
    m.round_box(bd, 0, 6.6, 4.0, 2.4, 9.0, 16.0, armour(P, "red", "red_dark", trim="black"), cut=1)   # back pack
    pb = m.bone("ring_prop", bd, (4.0, 32.0, 8.0))
    rod(m, bd, (2.0, 16.0, 8.0), (4.0, 32.0, 8.0), 1, metal(P, "green", dark="green_dark"), extend=0.2, t2=1)
    for i in range(4):                                                                  # leafy propeller
        ang = i * 90 + 45
        m.box(pb, 4.0 - 1.0, 32.0, 8.0, 4.0 + 1.0, 32.6, 15.0, leaff, rotation=(0, ang, 0), pivot=(4.0, 32.0, 8.0))
    m.round_box(bd, -5.4, 2.0, 1.0, 1.6, 4.0, 12.0, leather(P, "brown", "brown_dark"), cut=0)   # holster
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 14.0, -2.0))
        rod(m, ab, (sx * 5.0, 14.0, -2.0), (sx * 6.0, 8.0, -5.0), 2, SKIN, extend=0.3)
        for j in range(4):                                                              # spiky leaf cuffs
            ang = math.radians(j * 90)
            spike(m, ab, (sx * 6.0, 9.0, -4.6), (math.cos(ang), 0.3, math.sin(ang)), 1.0, 3.0, leaff, tip=0.3)
        for j in range(3):
            spike(m, ab, (sx * 6.0 + (j - 1) * 0.8, 7.0, -5.6), (0, -0.6, -1), 0.6, 1.6, solid(P, "black"), tip=0.2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                               # crouching legs, big claws
        lg = m.bone(nm, top, (sx * 4.0, 8.0, 0))
        m.round_box(lg, sx * 5.4, 1.0, 2.4, 3.4, 3.0, 10.0, SKIN, cut=1)
        m.round_box(lg, sx * 5.0, -2.0, 2.4, 3.0, 0.0, 2.6, SKIN, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 5.0 + (j - 1) * 1.6, 1.0, -4.6), ((j - 1) * 0.3, -0.2, -1), 1.0, 4.0,
                  solid(P, "claw"), tip=0.2)
    return m
