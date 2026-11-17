"""Bio Thunderbirmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a Bio Hybrid thunderbird. Great royal-blue wings whose feathers end in yellow lightning
bolts with yellow zigzag stripes, a red crested head with a hooked beak, a white mane, a glass capsule on its back,
steel ring bands on its wings and red talons. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, cutout, feathers, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a Bio Hybrid thunderbird: great blue wings ending in yellow lightning bolts, a red crested head with a hooked "
        "beak, a white mane, a glass capsule on its back and red talons")
BASE = {"blue": (40, 60, 170), "blue_dark": (16, 24, 90), "yellow": (250, 220, 40), "red": (220, 40, 40),
        "red_dark": (130, 14, 20), "white": (240, 240, 244), "white_dark": (180, 180, 190), "steel": (190, 194, 206),
        "steel_dark": (90, 94, 106), "glass": (90, 200, 160, 200), "glass_light": (210, 255, 240),
        "beak": (250, 200, 50), "eye": (255, 220, 60)}
SHINY = {"blue": (170, 40, 140), "blue_dark": (100, 14, 80), "yellow": (120, 230, 255), "red": (40, 160, 90),
         "red_dark": (16, 90, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = 1 - v / max(H, 1e-6)
    if t > 0.7:
        return tone(p["yellow"], face), p["yellow"]
    if abs(u - W / 2 - (((v * 0.6) % 2) - 1) * 0.6) < 0.3:
        return tone(p["yellow"], face), None
    return feathers(P, "blue", "blue_dark", size=(1.4, 2.6), flow=(0, -1))(x, y, z, face, variant, box=box, **k)


def bolt(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = 1 - v / max(H, 1e-6)
    if t < 0.7:
        return True
    zig = ((t - 0.7) / 0.3 * 3) % 1
    return abs(u / max(W, 1e-6) - 0.5 - (zig - 0.5) * 0.4) < 0.5 * (1 - (t - 0.7) / 0.3) + 0.08


def build():
    m = Model("biothunderbirmon")
    top = m.bone("biothunderbirmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    for i in range(5):
        r = 5.0 - abs(i - 2) * 0.6
        m.round_box(bd, 0, -2.0 - i * 1.4, r, r * 0.9, 18.0 + i * 2.4, 20.8 + i * 2.4,
                    feathers(P, "blue", "blue_dark", size=(1.4, 2.4)), cut=1)
    hd = m.bone("head", bd, (0, 30, -8))
    ball(m, hd, (0, 31.0, -9.0), 3.2, armour(P, "red", "red_dark"), layers=4)
    m.box(hd, -1.2, 29.0, -15.0, 1.2, 31.4, -11.0, metal(P, "beak", dark="red_dark"))
    spike(m, hd, (0, 30.0, -15.0), (0, -1, -0.3), 1.6, 2.0, metal(P, "beak", dark="red_dark"))
    for sx in (-1, 1):
        m.box(hd, sx * 2.4 - 0.4, 31.6, -11.4, sx * 2.4 + 0.4, 32.4, -11.0, solid(P, "eye", glow=True))
    for j in range(5):                                           # red crest
        spike(m, hd, (0, 33.0, -9.0 + j), (0, 1, 0.8), 1.2, 4.0 - j * 0.5, solid(P, "red"))
    for i in range(10):                                          # white mane
        ang = math.radians(i * 36)
        spike(m, bd, (3.6 * math.sin(ang), 28.0, -6.0 + 3.6 * math.cos(ang)), (math.sin(ang), -0.3, math.cos(ang)),
              1.6, 2.6, solid(P, "white"))
    m.round_box(bd, 0, 2.0, 1.4, 1.4, 27.0, 32.0, gem(P, "glass", "glass_light"), cut=1)   # glass capsule
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        wb = m.bone(nm, bd, (sx * 4.0, 26.0, -2.0))
        rod(m, wb, (sx * 4.0, 26.0, -2.0), (sx * 24.0, 34.0, 2.0), 3, armour(P, "blue", "blue_dark"), extend=0.4)
        m.round_box(wb, sx * 12.0, -0.4, 2.0, 2.0, 28.0, 30.4, metal(P, "steel", dark="steel_dark"), cut=1)
        for i in range(10):
            t = i / 9
            base = (sx * (4.0 + 20.0 * t), 26.0 + 8.0 * t, -2.0 + 4.0 * t)
            ln = 10.0 + 16.0 * t
            m.box(wb, base[0] - 1.6, base[1] - ln, base[2], base[0] + 1.6, base[1], base[2], cutout(bolt, wingf),
                  rotation=(-10, 0, -sx * (20 - 10 * t)), pivot=base)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 18.0, 0))
        rod(m, lg, (sx * 2.4, 18.0, 0), (sx * 3.0, 11.0, -1.0), 2, armour(P, "red", "red_dark"), extend=0.3)
        for d in ((0.3, -0.4, -1), (0, -0.4, -1), (-0.3, -0.4, -1)):
            spike(m, lg, (sx * 3.0, 10.6, -1.0), d, 1.0, 3.0, solid(P, "red"))
    return m
