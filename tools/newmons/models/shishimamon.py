"""Shishimamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the lion-dance beast: a great golden-red shishi lion head with a fiery mane, bulging eyes and a
snapping jaw, a billowing green cloth body patterned with swirls, red-and-white striped streamers, a blue cloud-swirl
tail, and armoured black limbs with red-tipped claws. 25 blocks.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fabric, metal, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lion-dance beast: a great golden-red shishi head with a fiery mane, a billowing green swirl-patterned cloth body and striped streamers"
BASE = {"green": (40, 120, 70), "green_dark": (14, 60, 30), "swirl": (200, 230, 210), "red": (210, 40, 40),
        "gold": (250, 200, 60), "gold_dark": (190, 110, 20), "white": (246, 246, 246), "blue": (60, 80, 170),
        "black": (30, 28, 34), "black_dark": (10, 10, 12), "eye": (250, 240, 200), "tooth": (250, 250, 236)}
SHINY = {"green": (130, 40, 120), "green_dark": (60, 14, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def clothf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    r = math.hypot(((x + z) % 5.0) - 2.5, (y % 5.0) - 2.5)
    if abs(r - 1.4) < 0.25:
        return tone(p["swirl"], face), None
    return fabric(P, "green", "green_dark", axis="x", period=2.6)(x, y, z, face, variant, box=box, **k)


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (x + y + z) % 2.4 < 1.2 else p["white"], face), None


def build():
    m = Model("shishimamon")
    top = m.bone("shishimamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    for i in range(5):                                                                   # billowing cloth body
        r = 9.0 + 2.0 * math.sin(i * 1.2)
        m.round_box(bd, 0, -6.0 + i * 5.0, r, 3.0, 10.0 + i, 26.0 - i, clothf, cut=2)
    hd = m.bone("head", bd, (0, 22, -12))
    ball(m, hd, (0, 24.0, -14.0), 7.0, armour(P, "red", "gold_dark", trim="gold", trim_w=0.4), layers=5)
    for sx in (-1, 1):
        ball(m, hd, (sx * 3.0, 27.0, -20.0), 2.0, solid(P, "eye"), layers=2)
        m.box(hd, sx * 3.0 - 0.6, 26.4, -22.1, sx * 3.0 + 0.6, 27.6, -21.9, solid(P, "black"))
    jb = m.bone("jaw", hd, (0, 20, -16))
    m.round_box(jb, 0, -19.0, 5.0, 3.0, 17.0, 20.0, armour(P, "red", "gold_dark"), cut=1)
    for j in range(6):
        spike(m, hd, (-4.0 + j * 1.6, 21.0, -20.6), (0, -1, 0), 0.9, 1.6, solid(P, "tooth"), tip=0.8)
    for j in range(16):                                                                  # fiery mane
        ang = 2 * math.pi * j / 16
        spike(m, hd, (6.4 * math.cos(ang), 24.0 + 6.4 * math.sin(ang), -11.0), (math.cos(ang), math.sin(ang), 0.5), 2.0,
              6.0, strands(P, "gold", "red"), tip=0.8)
    for j in range(2):                                                                   # striped streamers
        pts = [(0, 30.0, -6.0 + j * 4.0), (6.0 + j * 4.0, 38.0, 0.0 + j * 6.0), (18.0, 36.0, 10.0 + j * 6.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 2, stripef, extend=0.3)
    tl = m.bone("tail", bd, (0, 18, 14))                                                 # cloud-swirl tail
    for i in range(6):
        ang = i * 1.0
        ball(m, tl, (4.0 * math.cos(ang), 14.0 + i, 18.0 + 4.0 * math.sin(ang)), 2.0, solid(P, "blue"), layers=2)
    for sx, nm in ((1, "leg_front_left"), (-1, "leg_front_right"), (1, "leg_back_left"), (-1, "leg_back_right")):
        zz = -6.0 if "front" in nm else 10.0
        lg = m.bone(nm, top, (sx * 6.0, 12.0, zz))
        rod(m, lg, (sx * 6.0, 12.0, zz), (sx * 7.0, 2.0, zz - 1.0), 3, armour(P, "black", "black_dark"), extend=0.4)
        for f in range(3):
            spike(m, lg, (sx * 7.0 + (f - 1) * 1.2, 1.0, zz - 3.0), (0, -0.2, -1), 0.9, 3.0, solid(P, "red"), tip=0.8)
    return m
