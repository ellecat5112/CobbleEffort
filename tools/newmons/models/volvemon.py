"""Volvemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a sleek white-and-black android: glossy white armour panels split by black seams, a skull-like
white face with a shock of magenta hair, a round black port in its shoulder, green gem lights at its hips, huge
black-ringed fists, long segmented legs on heavy clawed boots, and a golden energy ring swirling round it. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, gem, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a sleek white-and-black android with a skull-like face, magenta hair, huge black-ringed fists and a golden energy ring"
BASE = {"white": (246, 246, 250), "white_dark": (180, 184, 200), "black": (30, 30, 36), "magenta": (230, 70, 200),
        "magenta_dark": (150, 30, 130), "green": (60, 220, 120), "green_light": (190, 255, 210),
        "gold": (255, 220, 90, 190), "eye": (40, 240, 120)}
SHINY = {"white": (60, 60, 70), "white_dark": (20, 20, 28), "black": (230, 230, 236), "magenta": (90, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (abs(x) % 5.0) < 0.5 or (y % 6.0) < 0.6:
        return tone(p["black"], face), None
    return armour(P, "white", "white_dark", panel=(4.0, 4.0))(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("volvemon")
    mats = {"skin": platef, "chest": platef, "abs": solid(P, "black"), "pelvis": platef, "deltoid": platef,
            "upper_arm": solid(P, "black"), "forearm": platef, "hand": platef, "thigh": platef,
            "knee": solid(P, "black"), "shin": platef, "calf": platef, "foot": platef, "talon": solid(P, "black"),
            "neck": solid(P, "black")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.0, talons=True, name="volvemon")
    bd = a["body"]
    for sx in (-1, 1):
        m.round_box(bd, sx * 7.6, 0, 4.0, 4.0, 46.0, 54.0, platef, cut=2)
        ball(m, bd, (sx * 4.0, 30.6, -4.4), 1.0, gem(P, "green", "green_light"), layers=1)
    m.round_box(bd, 7.6, -4.4, 2.2, 0.4, 48.0, 52.0, solid(P, "black"), cut=0)              # shoulder port
    for nm in ("arm_left", "arm_right"):                                               # huge ringed fists
        h = a[nm]["hand"]
        ball(m, a[nm]["bone"], h, 4.4, platef, layers=3)
        m.round_box(a[nm]["bone"], h[0], h[2], 4.6, 4.6, h[1] + 1.6, h[1] + 3.0, solid(P, "black"), cut=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.2, 54.0, 61.0, platef, cut=1)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.2, -3.2, 0.9, 0.4, 57.4, 59.0, solid(P, "black"), cut=0)
        ball(m, hd, (sx * 1.2, 58.2, -3.6), 0.4, solid(P, "eye", glow=True), layers=1)
    for j in range(6):
        spike(m, hd, (0, 61.0, -2.0 + j * 1.0), (0, 1, 0.3), 1.4, 5.0 - abs(j - 2) * 0.6,
              strands(P, "magenta", "magenta_dark"), tip=0.8)
    rg = m.bone("ring", bd, (0, 34, 0))                                                 # golden energy ring
    for i in range(20):
        ang = i * 2 * math.pi / 20
        cx, cy = 18.0 * math.cos(ang), 34.0 + 26.0 * math.sin(ang)
        if cy < 1.0:
            continue
        m.box(rg, cx - 1.2, cy - 1.2, 3.0, cx + 1.2, cy + 1.2, 3.8, solid(P, "gold", glow=True))
    return m
