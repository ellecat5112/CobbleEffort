"""Piemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the evil clown of the Dark Masters: a tall jester with a white grinning mask with a red heart under
one eye, a crown of orange flame-plumes, a frilled white ruff with a red bow, a red-and-blue jester's coat, green
puffed trousers, golden curled boots, white gloves, a little puppet on one shoulder, a long blue sash streaming round
him and four swords on his back. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a tall evil jester with a grinning white mask, a crown of orange plumes, a frilled ruff, a red-and-blue coat, "
        "green puffed trousers, golden curled boots, a blue sash and four swords on his back")
BASE = {"white": (246, 246, 250), "white_dark": (190, 190, 200), "red": (210, 40, 40), "red_dark": (130, 14, 14),
        "blue": (60, 90, 200), "blue_dark": (20, 40, 130), "green": (100, 170, 60), "green_dark": (50, 100, 24),
        "gold": (240, 190, 50), "gold_dark": (170, 120, 20), "orange": (240, 140, 40), "black": (24, 22, 26),
        "steel": (210, 214, 226), "sash": (120, 180, 240), "sash_dark": (60, 110, 190)}
SHINY = {"red": (60, 60, 70), "red_dark": (24, 24, 30), "green": (150, 80, 180), "green_dark": (90, 30, 110)}


def P(v):
    return pal(BASE, SHINY, v)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    key = ("red", "red_dark") if x >= 0 else ("blue", "blue_dark")
    return fabric(P, key[0], key[1])(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("piemon")
    mats = {"skin": coatf, "neck": solid(P, "white"), "hand": skin(P, "white", dark="white_dark"),
            "finger": skin(P, "white", dark="white_dark"), "thigh": fabric(P, "green", "green_dark"),
            "knee": fabric(P, "green", "green_dark"), "shin": metal(P, "gold", dark="gold_dark"),
            "calf": metal(P, "gold", dark="gold_dark"), "foot": metal(P, "gold", dark="gold_dark"),
            "toe": metal(P, "gold", dark="gold_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, name="piemon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # puffed trousers, curled boots
        lg = a["leg_left" if sx > 0 else "leg_right"]
        ball(m, lg["bone"], (sx * 3.0, 24.0, 0.2), 4.0, fabric(P, "green", "green_dark"), layers=4, ry=5.0)
        ank = lg["ankle"]
        rod(m, lg["bone"], (ank[0], 1.0, ank[2] - 3.0), (ank[0], 4.0, ank[2] - 8.0), 2, metal(P, "gold"), extend=0.3)
    for i in range(10):                                                                  # frilled ruff
        ang = 2 * math.pi * i / 10
        spike(m, bd, (2.6 * math.cos(ang), 52.0, 2.6 * math.sin(ang)), (math.cos(ang), 0.1, math.sin(ang)), 2.0, 4.0,
              solid(P, "white"), tip=0.8)
    m.box(bd, -2.0, 48.6, -4.6, 2.0, 50.6, -4.2, solid(P, "red"))                          # red bow
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, skin(P, "white", dark="white_dark"), cut=1)   # grinning mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 57.4, -3.3, max(sx * 0.6, sx * 1.8), 58.0, -3.2, solid(P, "black"))
    m.box(hd, 1.0, 56.0, -3.3, 1.8, 56.8, -3.2, solid(P, "red"))
    m.box(hd, -1.8, 55.0, -3.3, 1.8, 55.4, -3.2, solid(P, "black"))
    for i in range(7):                                                                   # crown of orange plumes
        ang = math.radians(-60 + i * 20)
        spike(m, hd, (2.4 * math.sin(ang), 60.0, -0.6 * math.cos(ang)), (math.sin(ang) * 0.5, 1, 0.1), 1.2, 6.0,
              solid(P, "orange"), tip=0.8)
    for j in range(4):                                                                   # four swords on his back
        ang = math.radians(-30 + j * 20)
        rod(m, bd, (0, 40.0, 4.6), (16.0 * math.sin(ang), 40.0 + 16.0 * math.cos(ang), 5.0), 1, metal(P, "steel"),
            extend=0.2, t2=2)
        m.box(bd, 12.0 * math.sin(ang) - 1.2, 40.0 + 12.0 * math.cos(ang) - 0.3, 4.6, 12.0 * math.sin(ang) + 1.2,
              40.0 + 12.0 * math.cos(ang) + 0.3, 5.4, metal(P, "gold"))
    for j in range(8):                                                                   # streaming blue sash
        ang = 2 * math.pi * j / 8
        m.box(bd, 9.0 * math.cos(ang) - 1.6, 30.0 + j * 3.0, 9.0 * math.sin(ang) - 0.2, 9.0 * math.cos(ang) + 1.6,
              32.0 + j * 3.0, 9.0 * math.sin(ang) + 0.2, fabric(P, "sash", "sash_dark"),
              rotation=(0, -math.degrees(ang) + 90, 0), pivot=(9.0 * math.cos(ang), 31.0 + j * 3.0, 9.0 * math.sin(ang)))
    pb = m.bone("puppet", bd, (6.0, 54.0, 0))                                            # puppet on his shoulder
    ball(m, pb, (7.0, 55.0, 0), 1.6, fabric(P, "blue", "blue_dark"), layers=2)
    ball(m, pb, (7.0, 57.6, 0), 1.2, skin(P, "white", dark="white_dark"), layers=2)
    return m
