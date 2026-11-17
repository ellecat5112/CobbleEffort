"""Ebi Burgamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a little pink axolotl sitting upright under a big toasted burger-bun cap dotted with sesame seeds, with frilly pink
gill-fans on each side, round shiny eyes, rosy cheeks, a tiny cat-like smile, stubby arms and a short tail. Child
stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = ("a little pink axolotl under a big sesame burger-bun cap, with frilly gill-fans, round shiny eyes, rosy cheeks "
        "and a tiny smile")
BASE = {"pink": (250, 196, 190), "pink_dark": (220, 140, 140), "bun": (190, 130, 70), "bun_dark": (130, 80, 40),
        "bun_light": (230, 180, 110), "seed": (250, 246, 230), "eye": (40, 40, 50), "shine": (255, 255, 255),
        "cheek": (250, 140, 90), "mouth": (80, 40, 40), "gill": (250, 170, 180)}
SHINY = {"pink": (200, 220, 250), "pink_dark": (140, 160, 210), "gill": (170, 200, 250)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "pink", dark="pink_dark", var=0.02)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.8, y - 18.0)
            if d < 1.3:
                return tone(p["shine"] if (x - sx * 2.8) > 0.3 and y > 18.4 else p["eye"], face), None
            if math.hypot(x - sx * 4.0, y - 16.0) < 0.9:
                return tone(p["cheek"], face), None
        if abs(y - 16.0 - 0.6 * abs(abs(x) - 0.6)) < 0.18 and abs(x) < 1.4:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def bunf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("up", "north", "east", "west") and abs((x * 0.7) % 2.6 - 1.3) < 0.3 and abs((z * 0.7 + y * 0.5) % 2.2
                                                                                           - 1.1) < 0.2:
        return tone(p["seed"], face), None
    return skin(P, "bun", dark="bun_dark", light="bun_light", var=0.04)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ebiburgamon")
    top = m.bone("ebiburgamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 7.0, 1.0), 4.6, SKIN, layers=4, squash=1.0, ry=5.0)                 # sitting body
    hd = m.bone("head", bd, (0, 12, 0))
    ball(m, hd, (0, 17.0, 0), 5.6, headf, layers=5, squash=0.9, ry=5.0)
    ball(m, hd, (0, 22.0, 0), 7.4, bunf, layers=4, squash=0.95, ry=4.6)                # burger-bun cap
    m.round_box(hd, 0, -3.0, 7.0, 4.0, 19.6, 20.6, skin(P, "bun_dark", dark="bun_dark"), cut=2)   # cap brim
    for sx in (-1, 1):                                                                   # frilly gill-fans
        for j in range(3):
            spike(m, hd, (sx * 5.0, 15.0 + j * 1.6, 0.0), (sx, 0.4 + j * 0.3, 0.2), 1.2, 3.0, solid(P, "gill"), tip=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 9.0, -1.0))
        rod(m, ab, (sx * 3.6, 9.0, -1.0), (sx * 4.6, 5.0, -2.0), 2, SKIN, extend=0.4)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 3.0, 0))
        m.round_box(lg, sx * 2.6, -2.0, 1.8, 2.6, 0.0, 2.6, SKIN, cut=1)
    tl = m.bone("tail", bd, (0, 4, 5))
    rod(m, tl, (0, 4.0, 5.0), (0, 2.0, 9.0), 2, SKIN, extend=0.4)
    return m
