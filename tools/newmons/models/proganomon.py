"""Proganomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an armoured tortoise-dragon of grey-brown stone hide: a great domed shell of jointed plates
crowned by a huge crimson drill spike and more drills along its back and tail, a heavy armoured head with a crimson
V crest and glowing eyes, a plated belly, short clawed legs, a black cannon arm and pink-glowing missile pods. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a grey stone tortoise-dragon under a domed plated shell crowned with crimson drills, a black cannon arm and pink missile pods"
BASE = {"stone": (120, 110, 104), "stone_dark": (60, 54, 50), "shell": (110, 104, 100), "shell_dark": (50, 46, 44),
        "red": (200, 30, 60), "red_dark": (110, 10, 30), "black": (30, 28, 32), "steel": (190, 194, 206),
        "pink": (250, 140, 230), "eye": (250, 60, 80), "belly": (150, 140, 120), "claw": (40, 36, 36)}
SHINY = {"stone": (110, 140, 120), "stone_dark": (50, 74, 60), "red": (240, 180, 40), "red_dark": (150, 100, 10)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "stone", "stone_dark", size=1.8)
SHELL = armour(P, "shell", "shell_dark", panel=(4.0, 4.0))
DRILL = armour(P, "red", "red_dark")


def drillf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y * 1.4 + math.atan2(z, x) * 2) % 2.0 < 1.2 else p["red_dark"], face), None


def build():
    m = Model("proganomon")
    mats = {"skin": HIDE, "belly": armour(P, "belly", "stone_dark"), "claw": solid(P, "claw"), "head": HIDE}
    a = quadruped(m, mats, "proganomon", length=30.0, body_y=16.0, body_rx=9.0, body_ry=8.0, neck=((0, 22, -16),
                  (0, 25, -20)), head_len=10.0, head_w=4.6, head_h=5.0, teeth=4, tail=((0, 16, 16), (0, 14, 24),
                  (0, 12, 30)), tail_r=(3.0, 2.2, 1.4))
    bd = a["body"]
    for i in range(6):                                                                   # domed shell of plates
        t = i / 5
        r = 12.0 - 7.0 * t * t
        m.round_box(bd, 0, 2.0, r, r * 1.2, 20.0 + i * 3.0, 23.0 + i * 3.0, SHELL, cut=max(1, round(r * 0.35)))
    spike(m, bd, (0, 37.0, 2.0), (0, 1, 0.1), 5.0, 12.0, drillf, tip=0.8)                  # crowning drill
    for sx in (-1, 1):
        spike(m, bd, (sx * 9.0, 30.0, 6.0), (sx * 0.7, 0.7, 0.3), 3.0, 8.0, drillf, tip=0.8)
    for j in range(3):
        spike(m, "tail", (0, 17.0 - j * 1.6, 18.0 + j * 4.6), (0, 1, 0.3), 1.6, 4.0, drillf, tip=0.8)
    hd = a["head"]
    m.box(hd, -2.6, 28.0, -24.0, 2.6, 29.0, -18.0, solid(P, "red"), rotation=(0, 0, 0), pivot=(0, 28, -20))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.0, sx * 3.2))
        m.box(hd, x0, 26.6, -24.0, x1, 27.6, -22.6, solid(P, "eye", glow=True))
    rod(m, bd, (-9.0, 18.0, -10.0), (-14.0, 16.0, -22.0), 4, metal(P, "black", dark="black"), extend=0.6)  # cannon
    m.round_box(bd, -14.0, -22.6, 1.0, 0.6, 15.0, 17.0, solid(P, "pink", glow=True), cut=0)
    for j in range(3):                                                                   # missile pods
        ang = 2 * math.pi * j / 3
        c = (11.0 + 2.4 * math.cos(ang), 20.0 + 2.4 * math.sin(ang), -6.0)
        rod(m, bd, (c[0], c[1], c[2] + 4.0), c, 2, metal(P, "steel"), extend=0.2)
        spike(m, bd, c, (0, 0, -1), 1.6, 2.6, solid(P, "pink", glow=True), tip=0.8)
    return m
