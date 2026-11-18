"""Liskmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
crystal cockatrice: a round body of pink-red feathers studded with red crystal shards, white petal-like wings fanned
out, a pink bird head with a red crystal crest and white beak plume, a long black serpent neck-tail with a red tongue
coiling up beside it, and red crystal talons. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, gem, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a round pink-red feathered cockatrice with red crystal shards, white petal wings, a crystal-crested bird head and a black serpent tail"
BASE = {"pink": (230, 120, 130), "pink_dark": (160, 50, 70), "white": (246, 240, 240), "white_dark": (200, 180, 190),
        "red": (220, 40, 60), "red_light": (255, 160, 170), "black": (40, 36, 44), "black_dark": (12, 10, 14),
        "eye": (30, 30, 34), "tongue": (220, 40, 40)}
SHINY = {"pink": (130, 170, 230), "pink_dark": (60, 90, 170), "red": (80, 120, 230), "red_light": (190, 210, 255)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "pink", "pink_dark", size=(1.2, 2.0))
CRYS = gem(P, "red", "red_light", glow=False)
WHITE = feathers(P, "white", "white_dark", size=(1.4, 2.4))


def build():
    m = Model("liskmon")
    top = m.bone("liskmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 17.0, 1.0), 9.0, FEATH, layers=6)
    for j in range(8):                                                               # crystal shards
        ang = 2 * math.pi * j / 8
        spike(m, bd, (7.0 * math.cos(ang), 15.0 + 3.0 * math.sin(ang * 2), -4.0 + 4.0 * math.sin(ang)),
              (math.cos(ang), 0.2, -0.5), 1.6, 3.0, CRYS, tip=0.8)
    for side in (1, -1):                                                             # white petal wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 6.0, 18.0, 2.0))
        for j in range(5):
            ang = math.radians(-30 + j * 25)
            spike(m, wb, (side * 6.0, 18.0, 2.0), (side * math.cos(ang), math.sin(ang), 0.3), 3.0, 12.0, WHITE, tip=0.8)
    hd = m.bone("head", bd, (2, 26, -2))
    m.round_box(hd, 3.0, -2.0, 2.6, 3.0, 26.0, 31.4, FEATH, cut=1)
    spike(m, hd, (3.0, 28.4, -5.0), (0, -0.3, -1), 1.4, 3.0, solid(P, "white"), tip=0.8)
    m.box(hd, 0.2, 29.6, -3.6, 0.5, 30.4, -2.8, solid(P, "eye"))
    m.box(hd, 5.5, 29.6, -3.6, 5.8, 30.4, -2.8, solid(P, "eye"))
    for j in range(4):                                                               # crystal crest
        spike(m, hd, (3.0, 31.2, -2.0 + j * 1.2), (0, 1, 0.4 + j * 0.2), 1.4, 5.0 - j * 0.8, CRYS, tip=0.8)
    sb = m.bone("snake", bd, (-4, 14, 6))                                             # black serpent tail
    pts = [(-4.0, 14.0, 8.0), (-8.0, 18.0, 10.0), (-10.0, 26.0, 8.0), (-9.0, 32.0, 4.0), (-7.0, 34.0, 0.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, sb, p0, p1, 2, scales(P, "black", "black_dark"), extend=0.6)
    m.round_box(sb, -7.0, -1.6, 1.6, 2.0, 33.0, 35.4, scales(P, "black", "black_dark"), cut=1)
    rod(m, sb, (-7.0, 33.8, -3.4), (-7.4, 33.0, -6.0), 1, solid(P, "tongue"), extend=0, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # crystal talons
        lg = m.bone(nm, top, (sx * 3.0, 9.0, 0))
        rod(m, lg, (sx * 3.0, 10.0, 0), (sx * 3.4, 2.0, -1.0), 2, CRYS, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 3.4 + (j - 1) * 1.0, 1.0, -1.6), ((j - 1) * 0.3, -0.2, -1), 1.0, 3.0, CRYS, tip=0.8)
    return m
