"""G-Cutemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
Cutemon knight riding into battle: a stout green turtle-beast carrying a red drum whose skin is a leopard-spotted
hide, and on its back a little pink rabbit in a silver helmet and armour with a red-crested shield, a lance, and a
blue-capped turtle squire peering over its shoulder; gold rings jingle on the turtle's tail. 1 block tall.

Front is -z, y is up. 30 units tall (No Level on wikimon: sized as a Child).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = ("a stout green turtle-beast carrying a leopard-spotted drum, ridden by a little pink rabbit knight in silver "
        "armour with a red-crested shield and lance and a blue-capped turtle squire")
BASE = {"green": (110, 180, 90), "green_dark": (50, 110, 40), "drum": (200, 60, 40), "drum_dark": (120, 30, 20),
        "hide": (240, 220, 160), "spot": (70, 50, 30), "pink": (250, 180, 200), "pink_dark": (210, 120, 150),
        "silver": (210, 214, 224), "silver_dark": (110, 114, 126), "red": (200, 30, 40), "blue": (60, 70, 160),
        "eye": (30, 30, 34), "gold": (240, 200, 60), "gold_dark": (160, 120, 20), "wood": (150, 110, 60),
        "white": (246, 246, 246)}
SHINY = {"green": (90, 150, 220), "green_dark": (30, 80, 160), "pink": (250, 240, 180), "pink_dark": (220, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = skin(P, "green", dark="green_dark")
PINK = skin(P, "pink", dark="pink_dark")
SILVER = armour(P, "silver", "silver_dark", trim="red", trim_w=0.2)


def drumf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = x * 1.1, (y - 10.0) * 1.1
        if math.hypot((a % 3.2) - 1.6, (b % 3.0) - 1.5) < 0.9 and math.hypot((a % 3.2) - 1.6, (b % 3.0) - 1.5) > 0.5:
            return tone(p["spot"], face), None
        return tone(p["hide"], face), None
    return tone(p["drum"] if (y % 2.0) > 0.4 else p["drum_dark"], face), None


def shieldf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and (abs(x + 5.0) < 0.4 or abs(y - 22.0) < 0.4 or math.hypot(x + 5.0, y - 22.0) < 1.2):
        return tone(p["red"], face), None
    return SILVER(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gcutemon")
    top = m.bone("gcutemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    ball(m, bd, (0, 9.0, 1.0), 6.6, GREEN, layers=5, ry=5.6)                       # turtle-beast
    m.round_box(bd, 0, -4.8, 6.0, 2.6, 4.0, 15.0, drumf, cut=2)                    # the drum it carries
    hd = m.bone("head", bd, (0, 12, -6))
    m.round_box(hd, 0, -8.6, 2.6, 2.4, 9.0, 14.0, GREEN, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 1.8), 12.2, -11.1, max(sx * 0.8, sx * 1.8), 13.0, -10.9, solid(P, "eye"))
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        z = -3.0 if "front" in nm else 5.0
        lg = m.bone(nm, top, (sx * 4.6, 4.0, z))
        m.round_box(lg, sx * 4.6, z, 1.8, 1.8, 0.0, 5.0, GREEN, cut=1)
        for j in range(2):
            spike(m, lg, (sx * 4.6 + (j - 0.5) * 1.2, 0.4, z - 1.8), (0, 0, -1), 0.8, 1.2, solid(P, "white"))
    tb = m.bone("tail", bd, (0, 7, 7))
    rod(m, tb, (0, 7.0, 7.0), (0, 5.0, 13.0), 2, GREEN, extend=0.4, t2=1)
    for j in range(3):                                                               # gold rings on the tail
        m.round_box(tb, 0, 9.0 + j * 1.4, 1.4, 0.3, 4.8, 7.6, metal(P, "gold", dark="gold_dark"), cut=0)
    rb = m.bone("rider", bd, (0, 15, 1))                                             # the rabbit knight
    m.round_box(rb, 0, 1.0, 2.6, 2.2, 15.0, 20.0, SILVER, cut=1)
    m.round_box(rb, 0, 0.6, 2.4, 2.4, 20.0, 24.4, SILVER, cut=1)                    # helmet
    m.box(rb, -1.8, 21.6, -1.9, 1.8, 22.4, -1.7, solid(P, "eye"))                    # visor slit
    for sx in (-1, 1):
        rod(m, rb, (sx * 1.0, 24.0, 1.0), (sx * 1.6, 29.0, 1.6), 1, PINK, extend=0.2, t2=2)   # long pink ears
    m.round_box(rb, -5.0, -2.0, 2.4, 0.6, 18.0, 26.0, shieldf, cut=0)                # shield
    rod(m, rb, (3.6, 14.0, -1.0), (5.0, 30.0, -3.0), 1, solid(P, "wood"), extend=0)  # lance
    spike(m, rb, (5.0, 30.0, -3.0), (0.1, 1, -0.1), 1.0, 2.6, metal(P, "gold", dark="gold_dark"), tip=0.8)
    m.round_box(rb, 3.0, 4.0, 1.8, 1.6, 16.0, 19.6, GREEN, cut=1)                    # turtle squire
    m.round_box(rb, 3.0, 4.0, 2.0, 1.8, 19.4, 20.6, solid(P, "blue"), cut=1)
    return m
