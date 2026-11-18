"""Mochimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a soft pink rice-cake blob with a rounded top, big black eyes, a happy open cat-like mouth, rosy
cheeks and two stubby arms ending in little grey claws. 0.5 blocks tall.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a soft pink rice-cake blob with big black eyes, a happy cat-like mouth, rosy cheeks and stubby clawed arms"
BASE = {"pink": (246, 210, 220), "pink_dark": (220, 160, 180), "black": (20, 20, 24), "mouth": (220, 60, 80),
        "cheek": (250, 170, 190), "claw": (110, 110, 120)}
SHINY = {"pink": (220, 240, 210), "pink_dark": (170, 210, 160)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "pink", dark="pink_dark", var=0.02)


def build():
    m = Model("mochimon")
    top = m.bone("mochimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 8.0, 0), 6.0, BODY, layers=5, ry=7.0, squash=0.85)
    m.round_box(bd, 0, 0, 6.6, 5.4, 1.0, 4.0, BODY, cut=2)                               # flared hem
    for sx in (-1, 1):
        ball(m, bd, (sx * 2.2, 10.0, -4.6), 1.1, solid(P, "black"), layers=2)
        m.box(bd, sx * 3.6 - 0.8, 7.6, -4.6, sx * 3.6 + 0.8, 8.4, -4.4, solid(P, "cheek"))
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 5.4, 7.0, 0))
        rod(m, ab, (sx * 5.4, 7.0, 0), (sx * 8.0, 9.0, -1.0), 2, BODY, extend=0.3)
        for f in range(2):
            spike(m, ab, (sx * 8.4, 9.6 + f * 0.8, -1.4), (sx * 0.4, 0.6, -0.6), 0.8, 1.2, solid(P, "claw"), tip=0.8)
    m.round_box(bd, 0, -4.9, 1.2, 0.3, 6.4, 8.0, solid(P, "mouth"), cut=0)
    return m
