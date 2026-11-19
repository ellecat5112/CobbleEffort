"""Shootmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the sports-ball machine: a round red ball of a head with a demonic yellow grin and a crackling blue
lightning crest, a heavy cylinder-cannon arm, a huge baseball-mitt fist, coiled cyan spring limbs, iron-boot feet, and
sports balls orbiting it. 25 blocks.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import leather, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a round red ball-headed machine with a demonic yellow grin, a lightning crest, a cylinder-cannon arm, a mitt fist and spring limbs"
BASE = {"red": (210, 40, 40), "red_dark": (130, 14, 14), "yellow": (250, 210, 50), "black": (30, 28, 32),
        "steel": (180, 184, 196), "steel_dark": (80, 84, 96), "cyan": (90, 220, 240), "brown": (170, 120, 60),
        "brown_dark": (100, 66, 24), "orange": (230, 120, 40), "white": (246, 246, 246), "purple": (100, 60, 170)}
SHINY = {"red": (60, 80, 200), "red_dark": (20, 30, 120)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.6) < 1.4 and abs(y - 28.0 + (x * sx - 2.6) * 0.5) < 0.6:
                return tone(p["yellow"], face), None
        if 22.0 < y < 25.0 and abs(x) < 4.0 - (25.0 - y):
            return tone(p["yellow"] if (x * 2) % 2 < 1 else p["black"], face), None
    return metal(P, "red", dark="red_dark")(x, y, z, face, variant, box=box, **k)


def springf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["cyan"] if (y * 1.5 + x) % 1.6 < 0.9 else p["steel_dark"], face), None


def build():
    m = Model("shootmon")
    top = m.bone("shootmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 4.0, 3.4, 12.0, 20.0, STEEL, cut=1)
    hd = m.bone("head", bd, (0, 20, 0))
    ball(m, hd, (0, 26.0, -1.0), 7.0, headf, layers=6)
    for j in range(2):                                                                   # lightning crest
        m.box(hd, -0.4 + j * 3.0, 32.0, -1.0, 0.4 + j * 3.0, 38.0, 0.0, solid(P, "cyan", glow=True),
              rotation=(0, 0, 20 - j * 40), pivot=(j * 3.0, 32.0, -0.5))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 18.0, 0))
        rod(m, ab, (sx * 4.0, 18.0, 0), (sx * 9.0, 16.0, -2.0), 2, springf, extend=0.3)
    rod(m, "arm_right", (-9.0, 16.0, -2.0), (-12.0, 8.0, -6.0), 6, STEEL, extend=0.6)          # cylinder cannon
    m.round_box("arm_right", -12.6, -6.4, 2.0, 2.0, 5.0, 7.0, solid(P, "black"), cut=0)
    ball(m, "arm_left", (11.0, 20.0, -3.0), 4.6, leather(P, "brown", "brown_dark"), layers=3)   # mitt fist
    ball(m, "arm_left", (12.0, 24.0, -5.0), 3.0, solid(P, "purple"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 12.0, 0))
        rod(m, lg, (sx * 2.6, 12.0, 0), (sx * 3.0, 4.0, 0), 2, springf, extend=0.3)
        m.round_box(lg, sx * 3.0, -1.0, 2.6, 3.6, 0.0, 4.0, STEEL, cut=1)
    rb = m.bone("ring_balls", bd, (0, 24, 0))                                            # orbiting sports balls
    for j, key in enumerate(("orange", "white", "steel", "purple")):
        ang = 2 * math.pi * j / 4
        ball(m, rb, (14.0 * math.cos(ang), 28.0 + 4.0 * math.sin(ang * 2), 14.0 * math.sin(ang)), 1.8, solid(P, key),
             layers=2)
    return m
