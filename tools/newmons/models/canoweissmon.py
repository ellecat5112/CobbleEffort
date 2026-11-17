"""Canoweissmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the white sky dragon. A sleek white-armoured dragon with crimson joints and red inner plates,
a horned spiky white helm, great swept white wings lined with crimson webbing, clawed limbs and a long whip tail,
trailing a swirl of dark wind. 25 blocks tall.

Front is -z, y is up. 54 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, theropod
from _digidetail import armour, cutout, local, noise2, solid
from _route import pal, tone

HEIGHT = 54
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "floater"
K = 3
LOOK = ("a sleek white-armoured sky dragon with crimson joints, a horned spiky helm, great swept white wings lined "
        "with crimson and a swirl of dark wind")
BASE = {"white": (240, 244, 250), "white_dark": (170, 180, 200), "red": (190, 30, 50), "red_dark": (110, 10, 24),
        "claw": (230, 234, 244), "mouth": (110, 20, 30), "tooth": (250, 250, 250), "eye": (60, 220, 250),
        "wind": (40, 50, 80, 170), "wind_light": (140, 170, 220, 170)}
SHINY = {"white": (40, 44, 56), "white_dark": (16, 18, 24), "red": (60, 190, 230), "red_dark": (20, 110, 150)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="red", trim_w=0.3)
RED = armour(P, "red", "red_dark")


def windf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["wind_light"] if (u * 0.6 + v * 0.3) % 2.0 < 0.4 else p["wind"]
    return c, None


def windin(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = u / max(W, 1e-6)
    band = 0.5 + 0.35 * math.sin(t * math.pi * 1.5)
    return abs(v / max(H, 1e-6) - band) < 0.12 + 0.05 * noise2(u * 0.7, 3.0)


def build():
    m = Model("canoweissmon")
    mats = {"skin": WHITE, "belly": RED, "neck": WHITE, "head": WHITE, "snout": WHITE, "jaw": RED,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": WHITE, "hand": RED, "claw": solid(P, "claw"),
            "thigh": WHITE, "shin": RED, "foot": WHITE, "talon": solid(P, "claw"), "tail": WHITE, "tail_tip": RED}
    a = theropod(m, mats, "canoweissmon", hip_y=22.0, hip_z=3.0, chest=(0, 34.0, -1.0), body_r=4.6, chest_r=4.8,
                 neck_top=(0, 44.0, -5.0), head_len=10.0, head_w=3.0, head_h=3.4, mouth_open=16, teeth=5,
                 arm_len=10.0, arm_bulk=1.0, leg_bulk=1.0, stance=4.0,
                 tail=((0, 18, 10), (3, 13, 18), (8, 10, 25), (14, 10, 30), (20, 13, 32)),
                 tail_r=(3.0, 2.2, 1.6, 1.0, 0.6))
    hd = a["head"]
    top = a["skull_top"]
    z0, z1 = a["skull_z"]
    for i in range(5):                                                       # horned spiky helm
        spike(m, hd, (0, top - 0.4, z0 + 1.0 + i * 1.6), (0, 0.6, 1), 1.6, 3.4 + i * 0.6, WHITE)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, top - 0.8, z1 - 1.0), (sx * 0.6, 0.5, 1), 1.2, 6.0, WHITE, tip=0.4)
        m.box(hd, sx * 3.05, a["eye"][1] - 0.4, a["eye"][2] - 0.8, sx * 3.1, a["eye"][1] + 0.4, a["eye"][2] + 0.8,
              solid(P, "eye", glow=True))
    for side in (1, -1):                                                     # great swept white wings
        bat_wing(m, a["body"], (side * 3.0, 38.0, 3.0), 26.0, 20.0, 4, WHITE, RED, side=side, sweep=30)
    for sx in (-1, 1):
        spike(m, a["body"], (sx * 5.0, 38.0, -1.0), (sx, 0.6, 0.2), 1.6, 3.0, RED)
    wb = m.bone("wind", a["top"], (0, 6, 0))                                 # the swirl of dark wind
    for j, (yy, ang) in enumerate(((4.0, 0), (10.0, 60), (16.0, 120))):
        m.box(wb, -18.0, yy - 4.0, 0.0, 18.0, yy + 4.0, 0.0, cutout(windin, windf), rotation=(80, ang, 0),
              pivot=(0, yy, 0))
    return m
