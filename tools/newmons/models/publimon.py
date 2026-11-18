"""Publimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a hooded street imp: an oversized charcoal hoodie with spiked horn-hood and a pink tag on its
chest, a glowing yellow face that is all toothy grin and goggling eye, a big yellow clawed hand holding up a glowing
blue phone screen, baggy sleeves, and yellow feet in black sneakers. 15 blocks tall.

Front is -z, y is up. 38 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, solid
from _route import pal, tone

HEIGHT = 38
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hooded street imp in an oversized charcoal hoodie with a spiked hood, a glowing yellow grinning face and a glowing phone"
BASE = {"hood": (60, 64, 76), "hood_dark": (24, 26, 34), "yellow": (240, 230, 40), "yellow_dark": (180, 160, 10),
        "black": (20, 20, 24), "tooth": (250, 250, 240), "pink": (230, 80, 120), "screen": (120, 210, 250, 210),
        "white": (250, 250, 250), "green": (90, 190, 70)}
SHINY = {"hood": (150, 40, 50), "hood_dark": (80, 14, 20)}


def P(v):
    return pal(BASE, SHINY, v)


HOOD = fabric(P, "hood", "hood_dark", axis="y", period=2.2)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 25.0 < y < 28.0 and abs(x) < 3.4:
            if abs(y - 26.5) < 0.12 or abs((x + 3.4) % 1.0 - 0.5) < 0.08:
                return tone(p["black"], face), None
            return tone(p["tooth"], face), None
        if math.hypot(x - 1.6, y - 29.6) < 0.6:
            return tone(p["black"], face), None
    return tone(p["yellow"], face), p["yellow"]


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x + 1.0, y - 16.0) < 2.0 and math.hypot(x + 1.0, y - 16.0) > 1.2:
        return tone(p["pink"], face), None
    return HOOD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("publimon")
    top = m.bone("publimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 16.0, 0.6), 7.0, chestf, layers=5, ry=7.6)                             # hoodie
    hd = m.bone("head", bd, (0, 22, 0))
    ball(m, hd, (0, 28.0, 0), 6.4, HOOD, layers=5, ry=6.0)                                 # hood
    m.round_box(hd, 0, -4.4, 4.0, 1.6, 24.0, 32.0, facef, cut=1)                           # glowing face
    for j in range(7):                                                                   # spiked hood
        ang = math.radians(-70 + j * 23)
        spike(m, hd, (5.2 * math.sin(ang), 31.0 + 2.0 * math.cos(ang), 2.0), (math.sin(ang), math.cos(ang), 0.2),
              1.4, 3.0, HOOD, tip=0.8)
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.6, 33.0, 0), (sx * 0.5, 1, 0.2), 2.0, 4.0, HOOD, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 20.0, 0))
        rod(m, ab, (sx * 6.0, 20.0, 0), (sx * 11.0, 14.0, -2.0), 4, HOOD, extend=0.6)
        m.round_box(ab, sx * 11.6, -2.0, 2.4, 2.4, 11.4, 13.0, solid(P, "hood_dark"), cut=1)
        for f in range(4):
            spike(m, ab, (sx * 11.6 + (f - 1.5) * 1.0, 11.0, -2.6), ((f - 1.5) * 0.2, -1, -0.3), 0.9, 3.4,
                  solid(P, "yellow"), tip=0.8)
    m.box("arm_left", 10.0, 14.0, -8.0, 16.0, 24.0, -7.6, solid(P, "screen", glow=True),
          rotation=(0, -20, 0), pivot=(13.0, 19.0, -7.8))                                 # glowing phone
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 9.0, 0))
        m.round_box(lg, sx * 3.0, 0, 2.4, 2.4, 3.0, 10.0, HOOD, cut=1)
        m.round_box(lg, sx * 3.0, -1.0, 2.6, 3.4, 0.0, 3.0, solid(P, "black"), cut=1)
        m.box(lg, sx * 3.0 - 2.4, 0.0, -4.6, sx * 3.0 + 2.4, 0.8, 0.0, solid(P, "white"))
    return m
