"""Pistmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the speed-cycling plant: a lean green humanoid in a pink-spotted racing suit with a red visored helmet,
crouched over a bicycle whose two wheels are great rings of thorny green vine crackling with violet electricity, a
spiked drill-lance mounted on the front. 25 blocks tall.

Front is -z, y is up. 68 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _dorbickmon import mount
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 2}
LOOK = "a lean green racer in a pink-spotted suit and red helmet crouched over a bicycle with wheels of thorny vine crackling with electricity"
BASE = {"green": (80, 170, 70), "green_dark": (30, 100, 30), "pink": (240, 80, 160), "red": (210, 40, 40),
        "red_dark": (130, 14, 14), "black": (30, 28, 32), "bolt": (220, 120, 250), "steel": (200, 204, 216),
        "visor": (40, 40, 60)}
SHINY = {"green": (80, 130, 210), "green_dark": (30, 70, 150), "pink": (250, 200, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and math.sin(x * 1.4) * math.sin(y * 1.2 + z) > 0.85:
        return tone(p["pink"], face), None
    return skin(P, "green", dark="green_dark")(x, y, z, face, variant, box=box, **k)


def wheel(m, bone, c, r):
    cx, cy, cz = c
    for i in range(16):
        ang = 2 * math.pi * i / 16
        p = (cx, cy + r * math.sin(ang), cz + r * math.cos(ang))
        m.box(bone, cx - 1.6, p[1] - 1.6, p[2] - 1.6, cx + 1.6, p[1] + 1.6, p[2] + 1.6, skin(P, "green", dark="green_dark"))
        if i % 2 == 0:
            spike(m, bone, p, (0, math.sin(ang), math.cos(ang)), 1.0, 2.6, solid(P, "green_dark"), tip=0.8)
        else:
            for sx in (-1, 1):
                spike(m, bone, (cx + sx * 1.4, p[1], p[2]), (sx, 0.3 * math.sin(ang), 0.3 * math.cos(ang)), 0.8, 2.4,
                      solid(P, "green_dark"), tip=0.8)
        if i % 4 == 1:
            rod(m, bone, (cx, cy, cz), p, 1, solid(P, "bolt", glow=True), extend=0.0)


def build():
    m = Model("pistmon")
    root = m.bone("pistmon", None, (0, 0, 0))
    bk = m.bone("bike", root, (0, 12, 0))
    wheel(m, bk, (0, 16.0, -19.0), 15.0)
    wheel(m, bk, (0, 16.0, 19.0), 15.0)
    rod(m, bk, (0, 16.0, -19.0), (0, 30.0, -2.0), 1, metal(P, "steel"), extend=0.2)
    rod(m, bk, (0, 16.0, 19.0), (0, 30.0, 2.0), 1, metal(P, "steel"), extend=0.2)
    rod(m, bk, (0, 30.0, -2.0), (0, 30.0, 4.0), 2, metal(P, "steel"), extend=0.2)
    rod(m, bk, (0, 16.0, -19.0), (0, 40.0, -16.0), 1, metal(P, "steel"), extend=0.2)
    rod(m, bk, (-6.0, 40.0, -16.0), (6.0, 40.0, -16.0), 1, metal(P, "steel"), extend=0.2)
    spike(m, bk, (0, 26.0, -20.0), (0, 0.1, -1), 1.6, 14.0, metal(P, "steel"), tip=0.8)     # drill-lance
    i_box, i_bone = len(m.boxes), len(m.bones)
    mats = {"skin": suitf, "hand": solid(P, "black"), "finger": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="pistmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.0, armour(P, "red", "red_dark"), cut=1)   # red helmet
    m.box(hd, -2.0, 56.6, -3.5, 2.0, 58.0, -3.3, solid(P, "visor"))
    mount(m, i_box, i_bone, 6.0, 2.0, root)
    return m
