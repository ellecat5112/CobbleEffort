"""Baboongamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a hulking baboon armoured in rock. Shaggy grey-brown fur bristling along its back, a grey stone
mask over a pink snarling muzzle, heavy boulder plates on its shoulders and arms bound with leather straps, black
hands and feet, and a tail ending in a chained stone mace. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, fur, leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a hulking baboon armoured in rock: shaggy grey-brown fur, a stone mask over a pink snarling muzzle, boulder "
        "plates on its shoulders and arms bound with straps, and a chained stone mace tail")
BASE = {"fur": (120, 110, 100), "fur_dark": (60, 54, 48), "fur_light": (180, 170, 160), "rock": (190, 190, 196),
        "rock_dark": (110, 110, 120), "rock_light": (240, 240, 246), "pink": (220, 110, 120), "black": (34, 32, 36),
        "black_light": (90, 88, 96), "strap": (90, 60, 40), "mouth": (110, 20, 30), "tooth": (250, 248, 240),
        "tongue": (200, 80, 90), "eye": (255, 60, 60)}
SHINY = {"fur": (190, 140, 80), "fur_dark": (120, 80, 30), "fur_light": (240, 200, 140), "rock": (120, 140, 190),
         "rock_dark": (60, 70, 120)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=2.0)
ROCK = armour(P, "rock", "rock_dark", light="rock_light", panel=(2.6, 2.2))
BLACK = skin(P, "black", light="black_light")
STRAP = leather(P, "strap", "black")


def build():
    m = Model("baboongamon")
    mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": ROCK, "snout": skin(P, "pink"), "jaw": skin(P, "pink"),
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": ROCK, "leg_lower": FUR, "paw": BLACK,
            "claw": BLACK, "tail": FUR}
    a = quadruped(m, mats, "baboongamon", length=26.0, body_y=18.0, body_rx=8.0, body_ry=7.0, chest_bulk=1.35,
                  neck=((0, 20, -14), (0, 21, -17)), head_len=9.0, head_w=4.6, head_h=4.6, snout=0.4, mouth_open=16,
                  teeth=4, leg_len=17.0, leg_bulk=1.8, toes=4, tail=((0, 24, 15), (2, 30, 18), (4, 32, 22)),
                  tail_r=(1.2, 1.0, 0.8))
    bd = a["body"]
    for i in range(14):                                          # shaggy fur bristling along the back
        t = i / 13
        spike(m, bd, (0, 24.0 + 2.0 * math.sin(t * math.pi), -12.0 + 24.0 * t), (0, 1, 0.4), 3.0, 5.0, FUR, tip=1.4)
        for sx in (-1, 1):
            spike(m, bd, (sx * 6.6, 21.0, -10.0 + 20.0 * t), (sx, 0.6, 0.3), 2.4, 3.6, FUR, tip=1.0)
    for sx in (-1, 1):                                           # boulder plates on the shoulders and rump
        for j in range(3):
            ball(m, bd, (sx * 7.0, 25.0 - j * 2.0, -9.0 + j * 3.0), 3.0 - j * 0.4, ROCK, layers=3)
        ball(m, bd, (sx * 6.0, 22.0, 8.0), 2.6, ROCK, layers=3)
    for nm in ("leg_front_left", "leg_front_right"):            # straps round the stone forearms
        lg = a[nm]
        el = lg["elbow"]
        m.round_box(lg["bone"], el[0], el[2], 3.4, 3.4, el[1] - 4.0, el[1] - 2.6, STRAP, cut=1)
    tl = a["tail"]                                               # chained stone mace
    e = a["tail_pts"][-1]
    for j in range(4):
        c = (e[0] + j * 0.4, e[1] + 1.4 + j * 1.4, e[2] + j * 0.6)
        m.box(tl, c[0] - 0.6, c[1] - 0.6, c[2] - 0.6, c[0] + 0.6, c[1] + 0.6, c[2] + 0.6, metal(P, "rock", dark="rock_dark"),
              rotation=(45 * (j % 2), 45, 0), pivot=c)
    ball(m, tl, (e[0] + 1.6, e[1] + 8.0, e[2] + 2.4), 3.0, ROCK, layers=3)
    hd = a["head"]
    for sx in (-1, 1):
        m.box(hd, sx * 1.8 - 0.6, 22.6, -21.3, sx * 1.8 + 0.6, 23.4, -21.1, solid(P, "eye", glow=True))
    return m
