"""Patamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round little orange-and-cream hamster-like creature with big blue eyes, a tiny snout and four stubby
feet, its huge ear-wings spread wide. 1 block tall.

Front is -z, y is up. 20 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 20
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "floater"
K = 3
LOOK = "a round little orange-and-cream creature with big blue eyes, a tiny snout, stubby feet and huge ear-wings spread wide"
BASE = {"orange": (240, 160, 50), "orange_dark": (190, 110, 20), "cream": (250, 240, 210), "cream_dark": (210, 196, 160),
        "eye": (60, 150, 230), "white": (250, 250, 250), "black": (24, 22, 22)}
SHINY = {"orange": (210, 210, 220), "orange_dark": (140, 140, 160), "eye": (230, 90, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "down" or y < 6.0 or (face == "north" and y < 8.0):
        return tone(p["cream"], face), None
    return tone(p["orange"], face), None


def build():
    m = Model("patamon")
    top = m.bone("patamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    ball(m, bd, (0, 7.0, 0), 5.6, bodyf, layers=5, ry=4.6, squash=1.05)
    for sx in (-1, 1):
        ball(m, bd, (sx * 2.2, 8.6, -4.6), 1.2, solid(P, "white"), layers=2, squash=0.5)
        m.box(bd, sx * 2.2 - 0.6, 8.0, -5.25, sx * 2.2 + 0.6, 9.2, -5.1, solid(P, "eye"))
        wb = m.bone("ear_left" if sx > 0 else "ear_right", bd, (sx * 3.0, 11.0, 0))       # huge ear-wings
        x0, x1 = sorted((sx * 2.6, sx * 16.0))
        m.box(wb, x0, 10.4, -0.4, x1, 15.0, 0.4, skin(P, "orange", dark="orange_dark"), rotation=(0, 0, sx * 25),
              pivot=(sx * 2.6, 11.0, 0))
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 2.6, 2.0, -1.0))
        m.round_box(lg, sx * 2.6, -1.0, 1.0, 1.2, 0.0, 2.0, solid(P, "black"), cut=0)
    m.round_box(bd, 0, -5.2, 1.6, 0.8, 5.6, 7.0, solid(P, "cream"), cut=0)
    return m
