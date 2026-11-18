"""Penmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a stout violet penguin with a white chest marked with blue chevrons, a big yellow beak, round orange
eyes, flipper arms tipped with red claws and big yellow feet with red claws. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a stout violet penguin with a white chevron-marked chest, a big yellow beak, flipper arms and yellow feet with red claws"
BASE = {"violet": (100, 80, 180), "violet_dark": (50, 34, 110), "white": (246, 246, 250), "blue": (60, 80, 200),
        "yellow": (250, 210, 60), "red": (220, 60, 50), "eye": (240, 140, 40), "black": (24, 22, 30)}
SHINY = {"violet": (60, 60, 70), "violet_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs((y - abs(x) * 0.8) % 3.0 - 1.5) < 0.35:
        return tone(p["blue"], face), None
    return tone(p["white"], face), None


def build():
    m = Model("penmon")
    top = m.bone("penmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 13.0, 0.6), 7.0, feathers(P, "violet", "violet_dark"), layers=6, ry=9.0, squash=0.9)
    ball(m, bd, (0, 12.0, -3.0), 5.0, chestf, layers=4, ry=6.6, squash=0.5)
    hd = m.bone("head", bd, (0, 20, 0))
    ball(m, hd, (0, 22.6, -0.6), 5.0, feathers(P, "violet", "violet_dark"), layers=4, ry=4.4)
    m.round_box(hd, 0, -7.4, 2.2, 3.0, 20.4, 23.0, solid(P, "yellow"), cut=1)             # big beak
    for sx in (-1, 1):
        m.box(hd, sx * 2.4 - 0.8, 23.6, -5.25, sx * 2.4 + 0.8, 25.0, -5.1, solid(P, "eye"))
        m.box(hd, sx * 2.4 - 0.3, 24.0, -5.3, sx * 2.4 + 0.3, 24.6, -5.25, solid(P, "black"))
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 6.4, 16.0, 0))
        x0, x1 = sorted((sx * 6.0, sx * 11.0))
        m.box(ab, x0, 9.0, -1.0, x1, 16.0, 1.0, feathers(P, "violet", "violet_dark"), rotation=(0, 0, sx * 20),
              pivot=(sx * 6.0, 16.0, 0))
        for f in range(3):
            spike(m, ab, (sx * 10.0, 9.4, -0.6 + f * 0.6), (sx * 0.4, -1, -0.3), 0.8, 2.0, solid(P, "red"), tip=0.8)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 3.0, 6.0, 0))
        rod(m, lg, (sx * 3.0, 6.0, 0), (sx * 3.4, 2.0, 0), 3, solid(P, "yellow"), extend=0.3)
        m.round_box(lg, sx * 3.4, -1.6, 2.4, 3.0, 0.0, 2.0, solid(P, "yellow"), cut=1)
        for f in range(3):
            spike(m, lg, (sx * 3.4 + (f - 1) * 1.4, 0.8, -4.4), (0, -0.3, -1), 0.8, 2.0, solid(P, "red"), tip=0.8)
    return m
