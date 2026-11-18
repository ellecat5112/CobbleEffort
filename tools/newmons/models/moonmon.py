"""Moonmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little lavender droplet with a shiny round body, big black eyes, a small smile, rosy cheeks, four
little nubs round its crown and a long tall stalk rising from its head ending in a rounded bulb. 0.5 blocks tall.

Front is -z, y is up. 20 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(0.5, HEIGHT, 1.0)
KIND = "floater"
K = 3
LOOK = "a little lavender droplet with big black eyes, a small smile, rosy cheeks and a tall stalk ending in a bulb"
BASE = {"lav": (200, 196, 240), "lav_dark": (140, 136, 200), "black": (20, 20, 26), "white": (250, 250, 255),
        "cheek": (250, 190, 220), "mouth": (60, 50, 70)}
SHINY = {"lav": (250, 230, 160), "lav_dark": (200, 170, 90)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "lav", dark="lav_dark", var=0.02)


def build():
    m = Model("moonmon")
    top = m.bone("moonmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 4.6, 0), 4.6, BODY, layers=5, ry=4.4)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.6, 5.0, -3.8), 0.9, solid(P, "black"), layers=2)
        m.box(bd, sx * 2.8 - 0.6, 3.6, -4.1, sx * 2.8 + 0.6, 4.2, -3.9, solid(P, "cheek"))
    m.box(bd, -0.8, 3.0, -4.6, 0.8, 3.4, -4.4, solid(P, "mouth"))
    for i in range(4):                                                                   # crown nubs
        import math
        ang = i * math.pi / 2 + math.pi / 4
        ball(m, bd, (2.2 * math.cos(ang), 9.0, 2.2 * math.sin(ang)), 0.8, BODY, layers=1)
    rod(m, bd, (0, 8.6, 0), (0, 16.0, 0), 2, BODY, extend=0.3)                           # tall stalk
    ball(m, bd, (0, 17.6, 0), 1.8, BODY, layers=2, ry=2.4)
    return m
