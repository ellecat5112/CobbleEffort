"""Pajiramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the ram of the Twelve Devas: a centaur-like sheep with a cream woolly four-legged body and black
hooves, a dark-faced upper body in violet armour with great curled violet ram horns, a red scarf, a gold medallion,
a violet bow drawn in its hands and a round shield. 25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, fabric, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a centaur-like sheep with a cream woolly body, a dark-faced torso in violet armour, great curled ram horns, a red "
        "scarf, a violet bow and a round shield")
BASE = {"wool": (246, 240, 210), "wool_dark": (200, 190, 150), "black": (34, 30, 36), "violet": (130, 90, 180),
        "violet_dark": (70, 40, 110), "red": (200, 40, 40), "gold": (230, 190, 70), "eye": (230, 190, 60),
        "steel": (200, 204, 216)}
SHINY = {"wool": (220, 230, 250), "wool_dark": (160, 170, 210), "violet": (60, 150, 110), "violet_dark": (20, 90, 60)}


def P(v):
    return pal(BASE, SHINY, v)


WOOL = fur(P, "wool", "wool_dark", length=1.4)
ARM = armour(P, "violet", "violet_dark", trim="gold", trim_w=0.25)


def build():
    m = Model("pajiramon")
    mats = {"skin": WOOL, "claw": solid(P, "black"), "mouth": solid(P, "black"), "tooth": solid(P, "wool")}
    a = quadruped(m, mats, "pajiramon", length=22.0, body_y=14.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.1,
                  neck=((0, 18, -9), (0, 20, -10)), head_len=5.0, head_w=2.0, head_h=2.2, snout=0.3, mouth_open=0,
                  teeth=0, leg_bulk=1.1, toes=2, tail=((0, 16, 11), (0, 15, 13)), tail_r=(1.4, 1.0))
    bd = a["body"]
    ub = m.bone("torso", bd, (0, 18, -8))                                                # upright upper body
    m.round_box(ub, 0, -8.0, 4.0, 3.0, 18.0, 30.0, ARM, cut=1)
    ball(m, ub, (0, 26.0, -11.6), 1.0, metal(P, "gold"), layers=1)
    m.round_box(ub, 0, -8.0, 3.4, 3.0, 29.0, 31.0, fabric(P, "red", "violet_dark"), cut=1)   # red scarf
    hd = m.bone("head", ub, (0, 31, -8))
    m.round_box(hd, 0, -8.6, 2.4, 2.6, 31.0, 36.6, skin(P, "black", dark="violet_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 34.0, -11.3, max(sx * 0.6, sx * 1.6), 34.8, -11.15, solid(P, "eye"))
        pts = [(sx * 2.2, 36.0, -8.0), (sx * 5.0, 37.0, -7.0), (sx * 6.0, 34.0, -6.0), (sx * 4.6, 31.6, -7.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # curled ram horns
            rod(m, hd, p0, p1, max(1, 3 - j), ARM, extend=0.3)
    m.round_box(hd, 0, -7.8, 2.8, 2.8, 36.0, 37.4, ARM, cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, ub, (sx * 4.0, 28.0, -8.0))
        rod(m, ab, (sx * 4.0, 28.0, -8.0), (sx * 7.0, 30.0, -14.0), 2, ARM, extend=0.3)
    bow = [(-7.0, 40.0, -15.0), (-8.0, 34.0, -16.0), (-7.0, 28.0, -16.0), (-5.0, 22.0, -15.0)]
    for p0, p1 in zip(bow, bow[1:]):                                                     # violet bow
        rod(m, "arm_right", p0, p1, 1, metal(P, "violet", dark="violet_dark"), extend=0.2)
    rod(m, "arm_right", bow[0], bow[-1], 1, solid(P, "wool"), extend=0.0, t2=1)
    for i in range(8):                                                                   # round shield
        ang = 2 * math.pi * i / 8
        m.box("arm_left", 7.0 + 3.0 * math.cos(ang) - 1.0, 28.0 + 3.0 * math.sin(ang) - 1.0, -15.6, 7.0 + 3.0 * math.cos(ang) + 1.0,
              28.0 + 3.0 * math.sin(ang) + 1.0, -14.6, ARM)
    m.box("arm_left", 5.0, 26.0, -15.4, 9.0, 30.0, -14.8, solid(P, "black"))
    return m
