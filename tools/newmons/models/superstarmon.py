"""Superstarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the superstar: a big gleaming gold-and-silver star of a head-body with mirrored sunglasses and a
blue gem, white furry-cuffed boxing gloves studded gold on segmented arms, red-and-white striped legs in chunky gold
boots, and a red chain streaming behind. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, gem, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a gleaming gold-and-silver superstar with mirrored sunglasses, white furry-cuffed boxing gloves, striped legs and gold boots"
BASE = {"gold": (250, 210, 60), "gold_dark": (180, 130, 20), "silver": (220, 224, 236), "black": (24, 22, 28),
        "white": (250, 250, 250), "white_dark": (200, 200, 210), "red": (210, 40, 40), "blue": (80, 160, 250)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (120, 130, 160)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark")


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (y % 2.4) < 1.2 else p["white"], face), None


def build():
    m = Model("superstarmon")
    top = m.bone("superstarmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 26.0, 0), 6.0, GOLD, layers=4, squash=0.6)
    for j in range(5):
        ang = math.radians(90 + j * 72)
        spike(m, bd, (0, 26.0, 0), (math.cos(ang), math.sin(ang), 0), 5.0, 11.0, GOLD if j % 2 else metal(P, "silver"),
              tip=0.8)
    m.box(bd, -4.0, 26.0, -3.8, 4.0, 28.0, -3.4, solid(P, "black"))                           # sunglasses
    m.box(bd, -0.8, 30.0, -3.4, 0.8, 31.6, -3.0, gem(P, "blue", "white"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 22.0, 0))
        rod(m, ab, (sx * 5.0, 22.0, 0), (sx * 11.0, 17.0, -1.0), 1, metal(P, "silver"), extend=0.2, t2=2)
        m.round_box(ab, sx * 11.0, -1.0, 2.6, 2.6, 15.0, 17.6, fur(P, "white", "white_dark", length=1.2), cut=1)
        ball(m, ab, (sx * 12.4, 13.0, -1.6), 3.0, solid(P, "white"), layers=3)
        for j in range(3):
            m.box(ab, sx * 12.4 + (j - 1) * 1.2 - 0.4, 15.4, -4.4, sx * 12.4 + (j - 1) * 1.2 + 0.4, 16.2, -4.0, GOLD)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 12.0, 0))
        rod(m, lg, (sx * 2.6, 16.0, 0), (sx * 3.0, 5.0, 0), 2, legf, extend=0.3)
        m.round_box(lg, sx * 3.0, -1.0, 2.6, 3.6, 0.0, 5.4, GOLD, cut=1)
    pts = [(2.0, 32.0, 2.0), (8.0, 34.0, 8.0), (12.0, 30.0, 12.0), (16.0, 34.0, 14.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, solid(P, "red"), extend=0.2)
    return m
