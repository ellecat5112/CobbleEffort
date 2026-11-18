"""Nyokimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a seed just sprouting: a teardrop of shaggy black fuzz with two glowing yellow eyes and a little pink
smile inside a thin pale husk, and a green stem rising from its top with two round leaves. 0.35 blocks tall.

Front is -z, y is up. 16 units tall; Baby I stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.35, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a sprouting seed: a teardrop of shaggy black fuzz with glowing yellow eyes inside a pale husk, with a green two-leaf stem"
BASE = {"black": (40, 40, 44), "black_dark": (14, 14, 16), "husk": (220, 230, 236), "eye": (250, 220, 60),
        "pink": (240, 150, 160), "green": (150, 210, 70), "green_dark": (80, 140, 30)}
SHINY = {"black": (90, 60, 40), "black_dark": (50, 30, 16), "green": (240, 150, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def build():
    m = Model("nyokimon")
    top = m.bone("nyokimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 4.6, 0), 4.6, skin(P, "husk", dark="black"), layers=4, ry=4.2)          # pale husk
    ball(m, bd, (0, 4.4, -0.6), 4.0, fur(P, "black", "black_dark", length=1.0), layers=4, ry=3.8)
    spike(m, bd, (0, 8.0, 0), (0, 1, 0), 3.0, 2.4, skin(P, "husk", dark="black"), tip=0.8)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.6, 5.0, -4.2), 0.8, solid(P, "eye", glow=True), layers=1)
    m.box(bd, -0.7, 3.0, -4.65, 0.7, 3.6, -4.5, solid(P, "pink"))
    rod(m, bd, (0, 10.0, 0), (0, 13.0, 0), 1, solid(P, "green_dark"), extend=0.1)          # stem
    for sx in (-1, 1):
        ball(m, bd, (sx * 2.6, 14.0, 0), 2.0, skin(P, "green", dark="green_dark"), layers=2, ry=0.8)
    return m
