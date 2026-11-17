"""Exermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the wasp warrior. A slim black-armoured insect with glowing green seams, a sleek helmet with yellow
eyes and two long zig-zag green antennae, four arms ending in yellow hands with curved silver blades, a ring of steel
blade-spikes round its waist and a big round abdomen banded in green with a stinger beneath. 15 blocks tall.

Front is -z, y is up. 52 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 52
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a slim black-armoured wasp warrior with glowing green seams, yellow eyes, zig-zag green antennae, four arms with "
        "yellow hands and silver blades, a ring of waist blades and a green-banded abdomen")
BASE = {"black": (40, 40, 50), "black_dark": (12, 12, 16), "black_light": (110, 110, 130), "green": (60, 240, 110),
        "yellow": (250, 220, 40), "yellow_dark": (180, 140, 10), "steel": (210, 214, 226), "steel_dark": (100, 104, 116),
        "eye": (250, 230, 60), "face": (220, 220, 226)}
SHINY = {"black": (230, 230, 236), "black_dark": (150, 150, 160), "green": (240, 80, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light")
STEEL = metal(P, "steel", dark="steel_dark")


def seamf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and (y % 3.4) < 0.4:
        return p["green"], p["green"]
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("exermon")
    top = m.bone("exermon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    m.round_box(bd, 0, 0, 3.6, 3.0, 26.0, 38.0, seamf, cut=1)                         # slim thorax
    ball(m, bd, (0, 16.0, 3.0), 6.0, seamf, layers=6, squash=1.0, ry=7.0)             # banded abdomen
    spike(m, bd, (0, 9.4, 3.0), (0, -1, 0), 2.0, 5.0, STEEL, tip=0.4)                  # stinger
    for i in range(10):                                                                # ring of waist blades
        ang = 2 * math.pi * i / 10
        spike(m, bd, (3.6 * math.cos(ang), 25.0, 3.0 * math.sin(ang)), (math.cos(ang), -0.2, math.sin(ang)), 1.2, 6.0,
              STEEL, tip=0.3)
    hd = m.bone("head", bd, (0, 39, 0))
    m.round_box(hd, 0, -0.6, 2.6, 3.0, 38.0, 44.0, ARM, cut=1)
    m.box(hd, -1.4, 39.0, -3.7, 1.4, 41.0, -3.5, solid(P, "face"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 41.6, -3.7, max(sx * 0.6, sx * 2.0), 42.6, -3.5, solid(P, "eye", glow=True))
        pts = [(sx * 1.0, 44.0, 0)]
        for j in range(1, 6):                                                          # zig-zag antennae
            pts.append((sx * (1.0 + (j % 2) * 1.6), 44.0 + j * 2.0, 0))
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "green", glow=True), extend=0.2)
    for row, (y, up) in enumerate(((36.0, 1), (30.0, -1))):                            # four arms
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm if row == 0 else nm + "_lower", bd, (sx * 3.6, y, 0))
            elbow = (sx * 9.0, y + up * 2.0, -1.0)
            hand = (sx * 12.0, y + up * 8.0, -2.0)
            rod(m, ab, (sx * 3.6, y, 0), elbow, 2, seamf, extend=0.4)
            rod(m, ab, elbow, hand, 2, seamf, extend=0.4)
            m.round_box(ab, hand[0], hand[2], 1.8, 1.6, hand[1] - 1.6, hand[1] + 1.6,
                        armour(P, "yellow", "yellow_dark"), cut=1)
            pts = [hand, (hand[0] + sx * 3.0, hand[1] + up * 3.0, hand[2] - 1.0),
                   (hand[0] + sx * 4.0, hand[1] + up * 7.0, hand[2] - 3.0)]
            for p0, p1 in zip(pts, pts[1:]):                                           # curved silver blades
                rod(m, ab, p0, p1, 1, STEEL, extend=0.3, t2=2)
    return m
