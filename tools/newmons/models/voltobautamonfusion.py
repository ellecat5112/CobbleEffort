"""Voltobautamon (Fusion) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the art on wikimon.net): Voltobautamon merged with its monstrous mounts: a vast teal-and-blue mass covered in
glittering scale-like spots with red eyes and black horns, fused to a great silver orb bearing a skull-like face of
dark sockets, the little pirate figure riding on top among cables and spines. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, metal, plane, solid
from _route import pal, tone

HEIGHT = 41
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a vast teal spotted mass with red eyes and black horns fused to a silver skull-faced orb, a little pirate riding on top"
BASE = {"teal": (40, 150, 170), "teal_dark": (14, 70, 100), "blue": (40, 80, 200), "spot": (150, 240, 230),
        "silver": (200, 204, 220), "silver_dark": (100, 104, 124), "black": (24, 22, 28), "red": (255, 40, 50),
        "coat": (40, 38, 44), "bone": (230, 222, 200), "pink": (230, 120, 200)}
SHINY = {"teal": (170, 80, 160), "teal_dark": (100, 30, 100), "blue": (200, 70, 120), "spot": (250, 200, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def massf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    v = (int(x * 1.3 + 50) * 7 + int(y * 1.3) * 13 + int(z * 1.3 + 50) * 5) % 11
    if v == 0:
        return p["spot"], p["spot"]
    return tone(p["teal"] if v % 3 else p["blue"], face), None


def orbf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.6, b - 13.0) < 1.8:
                return p["black"], None
        if 8.0 < b < 9.4 and abs(a) < 3.0 and (a * 1.6) % 1.0 < 0.5:
            return p["black"], None
        if abs(b - 15.0) < 0.4 and abs(a) < 4.0:
            return p["pink"], p["pink"]
    return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("voltobautamonfusion")
    top = m.bone("voltobautamonfusion", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 12.0, -4.0), 7.0, orbf, layers=6)                                    # silver skull orb
    for (x, y, z, r) in ((2, 24, 6, 10.0), (-6, 20, 8, 7.0), (9, 18, 4, 6.0), (0, 30, 4, 6.0)):
        ball(m, bd, (x, y, z), r, massf, layers=4)                                       # teal spotted mass
    for sx in (-1, 1):
        ball(m, bd, (sx * 3.0 + 2.0, 27.0, -4.6), 1.0, solid(P, "red", glow=True), layers=1)
        spike(m, bd, (sx * 4.0 + 2.0, 32.0, 2.0), (sx * 0.6, 1, 0.3), 2.0, 8.0, solid(P, "black"), tip=0.8)
    rb = m.bone("rider", bd, (0, 34, 0))                                                 # the little pirate on top
    m.round_box(rb, 0, 0, 1.6, 1.4, 34.0, 38.0, fabric(P, "coat", "coat"), cut=0)
    ball(m, rb, (0, 39.0, 0), 1.2, solid(P, "bone"), layers=1)
    m.round_box(rb, 0, 0, 2.0, 1.6, 39.8, 40.6, solid(P, "black"), cut=0)
    for j in range(4):                                                                   # cables and spines
        ang = j * 1.6
        rod(m, bd, (0, 18.0, 0), (12.0 * math.cos(ang), 10.0 + j * 3.0, 12.0 * math.sin(ang)), 1, solid(P, "black"),
            extend=0.2)
    return m
