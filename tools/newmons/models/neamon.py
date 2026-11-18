"""Neamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a slender pale-yellow creature with tall rabbit-like ears, a calm closed-eyed smiling face, long thin
arms hanging at its sides and plain brown drawstring shorts over long flat feet. 1 block tall.

Front is -z, y is up. 36 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(1, HEIGHT, 1.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slender pale-yellow creature with tall rabbit-like ears, a calm closed-eyed smile, long thin arms and brown shorts"
BASE = {"yellow": (246, 230, 160), "yellow_dark": (200, 180, 110), "brown": (170, 90, 50), "brown_dark": (110, 50, 24),
        "black": (40, 36, 30)}
SHINY = {"yellow": (220, 220, 240), "yellow_dark": (160, 160, 190), "brown": (60, 90, 160), "brown_dark": (24, 40, 100)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "yellow", dark="yellow_dark")


def build():
    m = Model("neamon")
    top = m.bone("neamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 3.0, 2.4, 10.0, 21.0, SKIN, cut=1)                              # slender body
    m.round_box(bd, 0, 0, 3.4, 2.8, 7.0, 12.0, fabric(P, "brown", "brown_dark"), cut=1)   # drawstring shorts
    m.box(bd, -0.2, 9.0, -2.9, 0.2, 11.6, -2.7, solid(P, "brown_dark"))
    hd = m.bone("head", bd, (0, 21, 0))
    ball(m, hd, (0, 24.0, -0.2), 3.4, SKIN, layers=4, ry=3.0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 24.6, -3.55, max(sx * 0.6, sx * 1.8), 25.0, -3.45, solid(P, "black"))
        spike(m, hd, (sx * 1.8, 26.4, 0), (sx * 0.3, 1, 0), 2.4, 9.0, SKIN, tip=0.8)       # tall rabbit ears
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 3.0, 19.0, 0))
        rod(m, ab, (sx * 3.0, 19.0, 0), (sx * 4.0, 10.0, 0), 1, SKIN, extend=0.2, t2=1)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 1.6, 7.0, 0))
        rod(m, lg, (sx * 1.6, 7.0, 0), (sx * 2.0, 1.0, 0), 1, SKIN, extend=0.2, t2=2)
        m.round_box(lg, sx * 2.0, -1.4, 1.2, 2.4, 0.0, 1.0, SKIN, cut=0)
    m.box(hd, -0.8, 22.6, -3.45, 0.8, 23.0, -3.35, solid(P, "black"))
    return m
