"""Mothmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of knowledge: a pale-yellow segmented insect body with green armour plates on its
head, shoulders and limbs, red eyes, two feathered antennae, broad brown moth wings ringed with eye-spots, and a
gatling gun of four barrels slung beneath it. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult (Armor) stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, feathers, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a pale-yellow segmented insect with green armour, red eyes, feathered antennae, broad brown moth wings with "
        "eye-spots and a four-barrel gatling gun beneath it")
BASE = {"yellow": (240, 230, 170), "yellow_dark": (190, 170, 100), "green": (100, 160, 60), "green_dark": (40, 90, 24),
        "brown": (150, 110, 60), "brown_dark": (80, 50, 24), "cream": (240, 220, 180), "eye": (220, 30, 40),
        "steel": (120, 124, 136), "steel_dark": (50, 54, 64)}
SHINY = {"brown": (90, 110, 170), "brown_dark": (40, 50, 110), "green": (190, 80, 160), "green_dark": (110, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "yellow", dark="yellow_dark")
GREEN = armour(P, "green", "green_dark")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    r = math.hypot(u / max(W, 1e-6) - 0.55, v / max(H, 1e-6) - 0.5)
    c = p["brown_dark"] if abs(r - 0.2) < 0.06 or abs(r - 0.38) < 0.05 else p["cream"] if r < 0.08 else p["brown"]
    return tone(c, face), None


def build():
    m = Model("mothmon")
    top = m.bone("mothmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for j in range(5):                                                                   # segmented body
        ball(m, bd, (0, 26.0 - j * 3.4, 0.4 * j), 4.0 - j * 0.3, BODY, layers=2, ry=1.8)
    hd = m.bone("head", bd, (0, 30, 0))
    m.round_box(hd, 0, -0.6, 3.2, 3.2, 29.0, 34.6, GREEN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.4), 31.0, -3.85, max(sx * 0.8, sx * 2.4), 32.4, -3.7, solid(P, "eye", glow=True))
        x0, x1 = sorted((sx * 1.4, sx * 3.6))                                            # feathered antennae
        m.box(hd, x0, 34.0, -0.6, x1, 42.0, -0.6, feathers(P, "brown", "brown_dark"), rotation=(0, 0, -sx * 20),
              pivot=(sx * 1.4, 34.0, -0.6))
        m.round_box(bd, sx * 4.6, 0, 1.8, 2.2, 24.0, 28.0, GREEN, cut=1)                 # shoulder plates
        for j in range(2):                                                               # green limbs
            ab = m.bone(("arm_left" if sx > 0 else "arm_right") if j == 0 else ("leg_left" if sx > 0 else "leg_right"),
                        bd, (sx * 3.6, 24.0 - j * 8.0, -0.6))
            rod(m, ab, (sx * 3.6, 24.0 - j * 8.0, -0.6), (sx * 6.6, 20.0 - j * 8.0, -3.0), 2, GREEN, extend=0.3)
            spike(m, ab, (sx * 6.6, 20.0 - j * 8.0, -3.0), (sx * 0.3, -1, -0.4), 1.0, 2.6, GREEN, tip=0.8)
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 2.0, 24.0, 3.0))  # broad moth wings
        x0, x1 = sorted((sx * 2.0, sx * 18.0))
        m.box(wb, x0, 18.0, 3.6, x1, 30.0, 3.6, wingf, rotation=(0, sx * 15, sx * 10), pivot=(sx * 2.0, 24.0, 3.6))
    gb = m.bone("gun", bd, (0, 12, -2))                                                  # gatling gun
    for i in range(4):
        ang = math.pi / 2 * i + math.pi / 4
        rod(m, gb, (1.2 * math.cos(ang), 10.0 + 1.2 * math.sin(ang), -1.0),
            (1.2 * math.cos(ang), 10.0 + 1.2 * math.sin(ang), -10.0), 1, metal(P, "steel", dark="steel_dark"),
            extend=0.2)
    m.round_box(gb, 0, 0.4, 2.4, 2.0, 8.0, 12.0, metal(P, "steel", dark="steel_dark"), cut=1)
    return m
