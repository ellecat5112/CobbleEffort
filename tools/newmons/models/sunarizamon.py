"""Sunarizamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sand lizard with a stone head: a yellow-ochre lizard body crusted with brown spikes and dripping
mud, a heavy cracked brown rock skull-helm with a green red-rimmed eye and a jagged mouth, splayed clawed feet and a
long curling tail. 1 block. Child stage.

Front is -z, y is up. 20 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, skin, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a yellow-ochre sand lizard crusted with brown spikes under a heavy cracked rock skull-helm with a green red-rimmed eye"
BASE = {"ochre": (220, 190, 70), "ochre_dark": (150, 120, 30), "rock": (110, 90, 70), "rock_dark": (60, 46, 34),
        "spike": (130, 100, 40), "eye": (90, 200, 90), "red": (200, 40, 40), "black": (24, 20, 20)}
SHINY = {"ochre": (150, 190, 220), "ochre_dark": (80, 120, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "ochre", dark="ochre_dark", var=0.05)
ROCK = armour(P, "rock", "rock_dark", panel=(2.0, 2.0))


def build():
    m = Model("sunarizamon")
    mats = {"skin": HIDE, "head": ROCK, "snout": ROCK, "jaw": ROCK, "claw": solid(P, "black")}
    a = quadruped(m, mats, "sunarizamon", length=18.0, body_y=8.0, body_rx=4.0, body_ry=3.6, neck=((0, 9, -10),
                  (0, 10, -12)), head_len=8.0, head_w=4.0, head_h=4.0, mouth_open=10, teeth=4, leg_len=5.0,
                  tail=((0, 9, 9), (0, 12, 14), (2, 15, 16)), tail_r=(2.0, 1.4, 1.0))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 3.9, sx * 4.2))
        m.box(a["head"], x0, 11.0, -15.6, x1, 12.4, -14.0, solid(P, "eye"))
        m.box(a["head"], x0, 10.6, -16.0, x1, 12.8, -13.6, solid(P, "red"))
    for j in range(8):                                                                   # brown spikes
        spike(m, a["body"], ((j % 2 * 2 - 1) * 2.0, 11.0, -6.0 + j * 1.8), ((j % 2 * 2 - 1) * 0.4, 1, 0.2), 1.0, 2.6,
              solid(P, "spike"), tip=0.8)
    return m
