"""Petitmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tiny teal dragon blob with big black eyes, an open happy fanged mouth, little black-tipped horns,
small bat wings and a puff of flame floating before it. 0.35 blocks tall.

Front is -z, y is up. 14 units tall; Baby I stage.
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.35, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a tiny teal dragon blob with big black eyes, a happy fanged mouth, black-tipped horns, small bat wings and a puff of flame"
BASE = {"teal": (60, 170, 170), "teal_dark": (20, 100, 100), "black": (20, 20, 24), "white": (250, 250, 250),
        "mouth": (230, 90, 110), "pink": (240, 120, 160), "fire": (255, 140, 50), "fire_core": (255, 230, 130)}
SHINY = {"teal": (230, 160, 60), "teal_dark": (160, 100, 20)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "teal", dark="teal_dark", var=0.02)


def build():
    m = Model("petitmon")
    top = m.bone("petitmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 4.6, BODY, layers=4, ry=3.6, squash=1.1)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.6, 6.0, -4.2), 1.0, solid(P, "black"), layers=2)
        m.box(bd, sx * 1.6 - 0.5, 6.4, -5.25, sx * 1.6 - 0.1, 6.8, -5.15, solid(P, "white"))
        spike(m, bd, (sx * 2.0, 8.0, 0), (sx * 0.4, 1, 0.3), 1.2, 2.0, BODY, tip=0.8)
        spike(m, bd, (sx * 2.4, 9.8, 0.3), (sx * 0.4, 1, 0.3), 0.8, 1.0, solid(P, "pink"), tip=0.8)
        x0, x1 = sorted((sx * 3.0, sx * 7.0))
        m.box(bd, x0, 4.0, 2.6, x1, 7.0, 2.6, BODY, rotation=(0, 0, sx * 15), pivot=(sx * 3.0, 5.5, 2.6))
    m.round_box(bd, 0, -4.4, 1.6, 0.4, 3.0, 4.6, solid(P, "mouth"), cut=0)
    ball(m, bd, (-6.0, 5.0, -3.0), 1.4, solid(P, "fire", glow=True), layers=2)
    ball(m, bd, (-6.0, 5.0, -3.0), 0.7, solid(P, "fire_core", glow=True), layers=1)
    return m
