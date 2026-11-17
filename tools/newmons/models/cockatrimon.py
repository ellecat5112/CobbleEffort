"""Cockatrimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the giant gorgon chicken. A huge shaggy white bird with a yellow hooked beak open in a squawk, a
red eye, a ruff of white feathers tipped orange-red like flames fanning round its head, stubby wings, thick scaly
orange legs with black talons, and long dangling wattles. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, scales, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a huge shaggy white bird with a yellow hooked beak, a red eye, a ruff of flame-tipped feathers round its head "
        "and thick scaly orange legs with black talons")
BASE = {"white": (246, 244, 236), "white_dark": (200, 194, 180), "flame": (240, 90, 40), "flame2": (250, 170, 60),
        "beak": (250, 210, 50), "beak_dark": (200, 150, 20), "mouth": (200, 40, 60), "leg": (240, 150, 100),
        "leg_dark": (180, 90, 50), "talon": (30, 30, 34), "eye": (220, 30, 30), "pupil": (40, 10, 10),
        "lavender": (200, 180, 230)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "flame": (120, 80, 230), "flame2": (180, 140, 250)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "white", "white_dark", size=(1.2, 2.2))
FLAME = feathers(P, "flame", "flame2", size=(1.0, 2.0), tip="flame2")
LEG = scales(P, "leg", "leg_dark", size=1.0)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 40.0) < 1.0 and abs(z + 4.0) < 1.0:
        d = math.hypot(y - 40.0, z + 4.0)
        return tone(p["pupil"] if d < 0.4 else p["eye"], face), None
    return FEATH(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("cockatrimon")
    top = m.bone("cockatrimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 26.0, 2.0), 10.0, FEATH, layers=7, squash=0.9)
    hd = m.bone("head", bd, (0, 34, -4))
    m.round_box(hd, 0, -3.0, 3.6, 4.0, 34.0, 44.0, headf, cut=1)
    m.box(hd, -2.4, 39.0, -12.0, 2.4, 42.0, -6.0, solid(P, "beak"))                     # hooked beak
    spike(m, hd, (0, 40.0, -12.0), (0, -1, -0.4), 2.4, 2.6, solid(P, "beak_dark"), tip=0.4)
    jw = m.bone("jaw", hd, (0, 39, -6))
    m.box(jw, -2.0, 36.6, -10.6, 2.0, 38.6, -6.0, solid(P, "beak"), rotation=(20, 0, 0), pivot=(0, 39.0, -6.0))
    m.box(hd, -1.8, 38.4, -10.6, 1.8, 39.0, -6.2, solid(P, "mouth"))
    for sx in (-1, 1):                                                                 # wattles
        rod(m, hd, (sx * 1.0, 37.0, -7.0), (sx * 1.4, 30.0, -8.0), 1, solid(P, "mouth"), extend=0)
    for i in range(16):                                                                # flame-tipped ruff
        ang = math.radians(i * 22.5)
        base = (5.0 * math.cos(ang), 39.0 + 5.0 * math.sin(ang), -1.0)
        spike(m, hd, base, (math.cos(ang), math.sin(ang), 0.4), 2.4, 7.0 + (i % 3), FLAME, tip=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # stubby wings
        ab = m.bone(nm, bd, (sx * 9.0, 28.0, 0))
        for j in range(3):
            spike(m, ab, (sx * 9.0, 28.0 - j * 2.0, 0.0), (sx, -0.6, 0.3), 3.0, 6.0 - j, FLAME if j == 0 else FEATH,
                  tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                # thick scaly legs
        lg = m.bone(nm, top, (sx * 4.0, 18.0, 2.0))
        rod(m, lg, (sx * 4.0, 18.0, 2.0), (sx * 4.6, 4.0, 0.0), 5, LEG, extend=0.6)
        for d in ((-0.4, 0, -1), (0, 0, -1), (0.4, 0, -1), (0, 0, 1)):
            rod(m, lg, (sx * 4.6, 2.0, 0.0), (sx * 4.6 + d[0] * 4.0, 1.0, d[2] * 4.0), 2, LEG, extend=0.3)
            spike(m, lg, (sx * 4.6 + d[0] * 4.0, 1.0, d[2] * 4.0), (d[0], -0.3, d[2]), 1.2, 2.0, solid(P, "talon"))
    for j in range(5):                                                                 # tail plumes
        spike(m, bd, ((j - 2) * 2.0, 28.0, 11.0), ((j - 2) * 0.3, 0.6, 1), 2.4, 8.0, FEATH, tip=0.6)
    return m
