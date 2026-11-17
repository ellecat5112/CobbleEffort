"""Baluchimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a holy beast like a great horned rhinoceros-horse. A long pale head with a white beard and a
red brow jewel, small horns, a blue-furred body wrapped in gold-edged white armour bands with tassels, white armour
plates on its legs, brown fur above dark hooves, a hooked tail-blade and a cloud of white mist flowing from its back.
15 blocks tall.

Front is -z, y is up. 38 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, eye, fur, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 38
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a holy horned beast: a long pale head with a white beard and red brow jewel, blue fur wrapped in gold-edged "
        "white armour bands, armoured legs, dark hooves, a hooked tail-blade and a cloud of mist at its back")
BASE = {"blue": (70, 110, 190), "blue_dark": (30, 50, 120), "pale": (220, 220, 230), "pale_dark": (150, 150, 166),
        "white": (246, 246, 250), "white_dark": (180, 182, 196), "gold": (230, 186, 60), "gold_dark": (150, 110, 30),
        "brown": (110, 70, 40), "brown_dark": (60, 36, 18), "hoof": (40, 34, 30), "red": (220, 40, 60),
        "red_light": (255, 160, 170), "mist": (240, 244, 250, 190), "eye": (90, 170, 230), "pupil": (16, 20, 30),
        "mouth": (110, 50, 60), "tooth": (250, 250, 246)}
SHINY = {"blue": (180, 90, 160), "blue_dark": (110, 40, 100), "gold": (200, 210, 230), "gold_dark": (130, 140, 160)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = fur(P, "blue", "blue_dark", length=1.6)
PLATE = armour(P, "white", "white_dark", trim="gold", trim_w=0.5)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 21.0, y - 28.0, 1.0, "eye")
        if c is not None:
            return c, None
    return skin(P, "pale", dark="pale_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("baluchimon")
    mats = {"skin": BLUE, "belly": BLUE, "neck": BLUE, "head": headf, "snout": skin(P, "pale", dark="pale_dark"),
            "jaw": skin(P, "pale", dark="pale_dark"), "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
            "leg_upper": PLATE, "leg_lower": fur(P, "brown", "brown_dark"), "paw": solid(P, "hoof"),
            "claw": solid(P, "hoof"), "tail": BLUE}
    a = quadruped(m, mats, "baluchimon", length=28.0, body_y=18.0, body_rx=6.4, body_ry=6.4, chest_bulk=1.15,
                  neck=((0, 24, -16), (0, 28, -19)), head_len=11.0, head_w=3.4, head_h=4.2, snout=0.6, mouth_open=4,
                  teeth=0, leg_len=16.0, leg_bulk=1.4, toes=2, claws=False,
                  tail=((0, 22, 17), (0, 18, 21), (0, 16, 24)), tail_r=(1.2, 1.0, 0.8))
    bd = a["body"]
    for j in range(4):                                           # gold-edged white armour bands
        z = -10.0 + j * 5.6
        m.round_box(bd, 0, z, 7.0, 1.2, 12.0, 25.6, PLATE, cut=1)
        for sx in (-1, 1):
            rod(m, bd, (sx * 6.8, 12.0, z), (sx * 7.0, 8.0, z - 0.4), 1, strands(P, "gold", "gold_dark"), extend=0.2)
    hd = a["head"]
    m.box(hd, -1.6, 22.0, -26.0, 1.6, 25.0, -24.0, strands(P, "white", "white_dark"))   # white beard
    m.box(hd, -2.0, 21.0, -25.0, 2.0, 24.0, -21.0, strands(P, "white", "white_dark"))
    m.box(hd, -0.8, 30.0, -22.6, 0.8, 31.6, -22.0, gem(P, "red", "red_light"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 31.0, -19.0), (sx * 0.3, 1, 0.4), 1.4, 3.0, solid(P, "white"))
        spike(m, hd, (sx * 3.0, 30.0, -17.0), (sx * 0.6, 0.8, 0.5), 1.4, 3.0, BLUE)
    tl = a["tail"]
    e = a["tail_pts"][-1]
    rod(m, tl, e, (e[0], e[1] - 6.0, e[2] + 2.0), 1, metal(P, "white", dark="white_dark"), extend=0.2, t2=2)
    spike(m, tl, (e[0], e[1] - 6.0, e[2] + 2.0), (0, 0.4, -1), 1.0, 3.0, metal(P, "white", dark="white_dark"))
    mist = m.bone("cap", bd, (0, 26, 10))
    for j in range(6):                                           # the cloud of mist
        ball(m, mist, ((j % 3 - 1) * 4.0, 28.0 + (j // 3) * 4.0, 10.0 + j * 1.6), 4.0 - (j // 3), solid(P, "mist"),
             layers=3)
    return m
