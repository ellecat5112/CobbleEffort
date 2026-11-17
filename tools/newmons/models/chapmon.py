"""Chapmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little kappa. A plump green body with a white belly, a yellow duck bill, big black eyes, a leafy green
crest over a pale plate on its head, little flipper arms held out and a short tail. Baby II.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(0.5, HEIGHT, 0.55)
KIND = "floater"
K = 4
LOOK = "a plump green kappa baby with a white belly, a yellow bill, big black eyes and a leafy crest on a pale head plate"
BASE = {"green": (120, 200, 60), "green_dark": (60, 130, 30), "green_light": (190, 240, 130), "belly": (250, 250, 246),
        "bill": (250, 210, 40), "bill_dark": (200, 150, 20), "eye": (24, 24, 28), "white": (255, 255, 255),
        "plate": (236, 240, 220), "cheek": (250, 200, 80)}
SHINY = {"green": (90, 180, 230), "green_dark": (40, 110, 170), "green_light": (170, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 3.0, y - 15.6)
            if d < 1.6:
                return tone(p["white"] if math.hypot(x - sx * 3.0 + 0.5, y - 16.2) < 0.5 else p["eye"], face), None
        if y < 11.0 and abs(x) < 5.4 - max(0.0, (11.0 - y) * 0.2):
            return tone(p["belly"], face), None
    return skin(P, "green", dark="green_dark", light="green_light", var=0.03)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chapmon")
    top = m.bone("chapmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 11.0, 0), 8.0, bodyf, layers=7, squash=0.9)
    m.box(bd, -2.6, 11.4, -9.4, 2.6, 13.0, -6.6, solid(P, "bill"))                      # duck bill
    m.box(bd, -2.2, 10.4, -9.0, 2.2, 11.4, -6.6, solid(P, "bill_dark"))
    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 18.4, 19.4, solid(P, "plate"), cut=1)               # the pale head plate
    for j in range(5):                                                                 # leafy green crest
        ang = math.radians(-60 + j * 30)
        spike(m, hd, (4.0 * math.sin(ang), 18.6, -4.0 * math.cos(ang) + 1.0), (math.sin(ang), 0.6, 0.6), 2.0, 3.0,
              fur(P, "green", "green_dark", length=0.8), tip=0.6)
    spike(m, hd, (2.0, 19.0, -1.0), (1, 0.6, 0.2), 2.0, 4.0, fur(P, "green", "green_dark", length=0.8), tip=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # flipper arms held out
        ab = m.bone(nm, bd, (sx * 7.0, 10.0, 0))
        m.box(ab, min(sx * 6.0, sx * 12.0), 9.0, -1.4, max(sx * 6.0, sx * 12.0), 11.4, 1.4,
              skin(P, "green", dark="green_dark"), rotation=(0, 0, sx * 20), pivot=(sx * 6.0, 10.0, 0))
    tl = m.bone("tail", bd, (0, 6, 7))
    spike(m, tl, (0, 6.0, 6.0), (0, -0.3, 1), 2.4, 3.0, skin(P, "green", dark="green_dark"), tip=0.6)
    return m
