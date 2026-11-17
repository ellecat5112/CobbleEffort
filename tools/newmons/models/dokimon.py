"""Dokimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a round
white baby blob with a bright green V-shaped mask across its face, big yellow-green eyes, a cat-like little smile and
a single white curved horn on top. Baby I stage, a third of a block tall.

Front is -z, y is up. 16 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 0.5)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 4}
LOOK = "a round white blob with a bright green V-shaped mask, big yellow-green eyes, a little smile and a curved white horn"
BASE = {"white": (248, 248, 250), "white_dark": (190, 192, 204), "green": (40, 230, 40), "eye": (200, 230, 40),
        "pupil": (16, 16, 16), "mouth": (40, 40, 44)}
SHINY = {"green": (230, 60, 180), "eye": (250, 160, 220)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "white", dark="white_dark", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.6, y - 6.6)
            if d < 0.7:
                return tone(p["pupil"], face), None
            if d < 1.5:
                return tone(p["eye"], face), None
        if 6.6 < y < 9.6 and abs(x) < 5.6 and y > 6.6 + (3.0 - abs(abs(x) - 2.6)) * 0.0 and \
                not (abs(x) < 1.6 and y < 8.6 - abs(x) * 0.6):
            return tone(p["green"], face), None                         # the V mask
        if abs(y - (4.4 + 0.3 * abs(abs(x) - 0.8))) < 0.2 and abs(x) < 1.8:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dokimon")
    top = m.bone("dokimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 0, 0))
    ball(m, bd, (0, 6.0, 0), 7.0, bodyf, layers=6, squash=0.9, ry=6.0)
    hd = m.bone("head", bd, (0, 11, 0))
    spike(m, hd, (-1.0, 11.4, 0), (-0.3, 1, 0.1), 2.0, 5.0, SKIN, tip=0.8)              # curved white horn
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        m.bone(nm, top, (sx * 3.0, 1.0, 0))
    return m
