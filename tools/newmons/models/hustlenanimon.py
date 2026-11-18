"""Hustle Nanimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a brawler Nanimon: a round, egg-shaped pink body with a scowling face, a bushy black moustache and beard, dark
sunglasses, a golden trophy cup worn as a hat, huge red boxing gloves and stubby legs in black boots. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage (no level on wikimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a round pink brawler with a scowl, a bushy black beard, sunglasses, a golden trophy-cup hat and huge red boxing gloves"
BASE = {"pink": (240, 160, 160), "pink_dark": (180, 100, 100), "black": (30, 28, 32), "black_dark": (10, 10, 12),
        "gold": (250, 200, 60), "gold_dark": (170, 120, 20), "gold_light": (255, 240, 170), "red": (220, 40, 40),
        "red_dark": (130, 14, 18), "lens": (40, 40, 60), "white": (250, 250, 250)}
SHINY = {"pink": (130, 190, 120), "pink_dark": (60, 120, 60), "red": (40, 80, 220), "red_dark": (14, 30, 130)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(y - 24.0) < 1.0 and abs(x) < 4.6 and abs(abs(x) - 2.2) < 1.6:
            return tone(p["lens"], face), None
        if abs(y - 24.6) < 0.25 and abs(x) < 5.0:
            return tone(p["black"], face), None
        if abs(y - 20.6) < 0.3 and abs(x) < 1.6:
            return tone(p["black"], face), None
    return skin(P, "pink", dark="pink_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hustlenanimon")
    top = m.bone("hustlenanimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 18.0, 0), 9.0, bodyf, layers=6, squash=1.2)
    hd = m.bone("head", bd, (0, 28, 0))
    BEARD = strands(P, "black", "black_dark")
    for i in range(9):                                                              # bushy beard
        ang = math.radians(-80 + i * 20)
        spike(m, hd, (6.0 * math.sin(ang), 18.0, -6.0 * math.cos(ang) - 1.0), (math.sin(ang) * 0.4, -1, -0.3), 2.4,
              5.0 - abs(i - 4) * 0.4, BEARD, tip=0.8)
    for sx in (-1, 1):                                                              # moustache
        rod(m, hd, (0, 21.6, -8.4), (sx * 4.0, 21.0, -7.6), 1, BEARD, extend=0.2, t2=2)
    GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
    m.round_box(hd, 0, 0, 3.0, 3.0, 27.6, 29.0, GOLD, cut=1)                             # trophy cup hat
    m.round_box(hd, 0, 0, 1.0, 1.0, 29.0, 31.0, GOLD, cut=0)
    m.round_box(hd, 0, 0, 4.0, 4.0, 31.0, 36.0, GOLD, cut=2)
    for sx in (-1, 1):
        m.round_box(hd, sx * 4.8, 0, 0.6, 1.4, 32.0, 35.0, GOLD, cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # boxing gloves
        ab = m.bone(nm, bd, (sx * 8.6, 18.0, 0))
        rod(m, ab, (sx * 8.0, 19.0, 0), (sx * 11.0, 16.0, -2.0), 2, skin(P, "pink", dark="pink_dark"), extend=0.4)
        m.round_box(ab, sx * 12.0, -3.0, 3.6, 4.0, 11.6, 19.0, leather(P, "red", "red_dark"), cut=2)
        m.round_box(ab, sx * 11.6, -2.4, 2.6, 2.6, 17.6, 19.6, solid(P, "white"), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 8.0, 0))
        rod(m, lg, (sx * 3.6, 9.0, 0), (sx * 3.8, 3.0, 0), 2, skin(P, "pink", dark="pink_dark"), extend=0.4)
        m.round_box(lg, sx * 3.8, -1.0, 2.2, 3.4, 0.0, 3.6, leather(P, "black", "black_dark"), cut=1)
    return m
