"""Ultimate Chaosmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Chaosmon fused with still more power: the white, red and silver knight with its golden
lion gauntlet and rainbow halo, now wreathed in a flowing crimson mane, pale feathered wings, and a giant spectral
blue hand raised before it to crush its foes. 35 blocks.

Front is -z, y is up. Ultimate stage. Built on _chaosmon.make(valdur=True).
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid, strands
from _route import pal

from _chaosmon import make

HEIGHT = 74
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Chaosmon in white, red and silver armour wreathed in a crimson mane, pale wings and a giant spectral blue hand"
_X = {"hand": (120, 170, 240), "hand_dark": (60, 100, 190), "mane": (220, 50, 50), "mane_dark": (140, 20, 20),
      "gold": (240, 200, 60)}


def P(v):
    return pal(_X, {"hand": (200, 120, 240), "hand_dark": (130, 60, 190)}, v)


_body = make("ultimatechaosmon", valdur=True)


def build():
    m = _body()
    bd = next(b["name"] for b in m.bones if b["name"] == "body")
    HAND = skin(P, "hand", dark="hand_dark")
    hb = m.bone("giant_hand", bd, (16, 44, -10))                                        # spectral blue hand
    m.round_box(hb, 18.0, -12.0, 5.0, 2.4, 38.0, 48.0, HAND, cut=1)
    for f in range(4):
        x = 14.6 + f * 2.3
        rod(m, hb, (x, 48.0, -12.0), (x + (f - 1.5) * 0.6, 56.0 + (1.5 - abs(f - 1.5)) * 1.6, -12.6), 2, HAND, extend=0.4)
    rod(m, hb, (13.4, 42.0, -12.0), (10.0, 48.0, -12.6), 2, HAND, extend=0.4)
    m.round_box(hb, 18.0, -12.0, 5.4, 2.8, 35.0, 38.0, solid(P, "gold"), cut=1)
    for j in range(9):                                                                 # crimson mane
        ang = (j - 4) * 0.35
        spike(m, "head" if any(b["name"] == "head" for b in m.bones) else bd, (math.sin(ang) * 3.0, 59.0, 2.0),
              (math.sin(ang) * 0.8, -0.3, 1), 1.8, 12.0, strands(P, "mane", "mane_dark"), tip=0.8)
    return m
