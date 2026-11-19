"""Soulmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a ragged ghost in a witch's hat: a tattered white sheet of a body with a wide grin full of red-gummed
fangs, and a big black pointed witch hat with a red band. 15 blocks.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, local, noise2, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a tattered white sheet ghost with a wide grin of red-gummed fangs under a big black pointed witch hat with a red band"
BASE = {"white": (246, 244, 236), "white_dark": (190, 186, 170), "black": (30, 28, 32), "red": (200, 30, 40),
        "gum": (170, 40, 60), "tooth": (250, 250, 240)}
SHINY = {"white": (200, 230, 210), "white_dark": (130, 170, 140), "black": (90, 40, 120)}


def P(v):
    return pal(BASE, SHINY, v)


def sheetf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 14.0 < y < 19.0 and abs(x) < 4.0:
        if abs(y - 16.5) < 0.4 or (abs((x + 4.0) % 1.2 - 0.6) < 0.3 and abs(y - 16.5) < 2.0):
            return tone(p["tooth"], face), None
        return tone(p["gum"], face), None
    return tone(p["white"] if (y + x) % 5.0 > 0.6 else p["white_dark"], face), None


def ragged(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    f = (box.lo[0] + box.lo[2] + u) * 1.2
    return v / max(H, 1e-6) > 0.35 * abs(math.sin(f)) + 0.15 * noise2(f, 5)


def build():
    m = Model("soulmon")
    top = m.bone("soulmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0, 5.4, 4.6, 12.0, 22.0, sheetf, cut=2)
    for i in range(10):                                                                  # tattered hem
        ang = 2 * math.pi * i / 10
        c = (5.0 * math.cos(ang), 0, 4.4 * math.sin(ang))
        m.box(bd, c[0] - 1.8, 4.0, c[2], c[0] + 1.8, 13.0, c[2], cutout(ragged, sheetf),
              rotation=(0, -math.degrees(ang) + 90, 0), pivot=(c[0], 8.0, c[2]))
    for sx in (-1, 1):
        spike(m, bd, (sx * 5.0, 16.0, 0), (sx * 1, -0.6, -0.2), 1.6, 5.0, sheetf, tip=0.8)
    hd = m.bone("head", bd, (0, 22, 0))
    m.round_box(hd, 0, 0, 10.0, 10.0, 22.0, 23.0, solid(P, "black"), cut=3)                  # hat brim
    m.round_box(hd, 0, 0, 4.4, 4.4, 23.0, 25.0, solid(P, "red"), cut=1)
    m.round_box(hd, 0, 0, 4.0, 4.0, 25.0, 29.0, solid(P, "black"), cut=1)
    spike(m, hd, (0, 29.0, 0), (0.6, 0.6, 0.3), 3.0, 8.0, solid(P, "black"), tip=0.8)
    return m
