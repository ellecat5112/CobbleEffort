"""Shoutmon SH (a Digimon of the CobbleEffort: Digital crossover; built after the manga panel on wikimon.net, its only
picture): Shoutmon swinging a huge silver star on a chain, ringed by little smiling Starmons. 15 blocks. Adult stage
(no level on wikimon; by analogy with Shoutmon's other Xros forms). Shoutmon's body (_shoutmon.small) plus the star.

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, solid
from _route import pal
from _shoutmon import small

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Shoutmon swinging a huge silver star on a chain, ringed by little smiling Starmons"
_B = {"silver": (220, 224, 236), "silver_dark": (120, 124, 140), "gold": (250, 220, 70), "black": (24, 22, 26)}


def P(v):
    return pal(_B, {"silver": (250, 220, 120), "silver_dark": (180, 140, 40)}, v)


_body = small("shoutmonsh", "red")


def build():
    m = _body()
    STAR = metal(P, "silver", dark="silver_dark")
    c = (12.0, 30.0, -2.0)                                                                  # huge star
    rod(m, "arm_left", (4.8, 10.4, -1.2), c, 1, metal(P, "silver_dark"), extend=0.1, t2=1)
    ball(m, "arm_left", c, 3.0, STAR, layers=3)
    for j in range(5):
        ang = math.radians(90 + j * 72)
        spike(m, "arm_left", c, (math.cos(ang), math.sin(ang), 0), 2.6, 6.0, STAR, tip=0.8)
    for sx in (-1, 1):
        m.box("arm_left", c[0] + sx * 1.2 - 0.5, c[1] + 0.4, c[2] - 3.1, c[0] + sx * 1.2 + 0.5, c[1] + 1.4, c[2] - 2.9,
              solid(P, "black"))
    for j in range(6):                                                                      # little Starmons
        ang = 2 * math.pi * j / 6
        s = (c[0] + 12.0 * math.cos(ang), c[1] + 12.0 * math.sin(ang), c[2])
        ball(m, "arm_left", s, 1.0, solid(P, "gold"), layers=1)
        for k in range(5):
            a2 = math.radians(90 + k * 72)
            spike(m, "arm_left", s, (math.cos(a2), math.sin(a2), 0), 0.9, 1.6, solid(P, "gold"), tip=0.8)
    return m
