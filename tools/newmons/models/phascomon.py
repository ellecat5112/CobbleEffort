"""Phascomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little demon koala: a round shaggy brown koala with huge fluffy violet-lined ears, a big black
nose, sleepy half-lidded eyes with red marks below, small horns, tiny red bat wings, a pointed devil tail and bubbles
drifting from its sleepy head. 1 block tall.

Front is -z, y is up. 24 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a little demon koala with huge fluffy ears, a big black nose, sleepy eyes, small horns, tiny red bat wings and a devil tail"
BASE = {"brown": (110, 90, 80), "brown_dark": (60, 46, 40), "violet": (120, 80, 160), "black": (24, 22, 26),
        "red": (200, 40, 40), "white": (240, 240, 236), "bubble": (220, 236, 250, 170)}
SHINY = {"brown": (180, 180, 200), "brown_dark": (110, 110, 130)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "brown", "brown_dark", length=1.4)


def build():
    m = Model("phascomon")
    top = m.bone("phascomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 7.0, 0.4), 4.0, FUR, layers=4, ry=4.0)
    hd = m.bone("head", bd, (0, 11, 0))
    ball(m, hd, (0, 14.0, -0.4), 5.0, FUR, layers=5, ry=4.4)
    m.round_box(hd, 0, -5.4, 1.6, 1.4, 12.0, 15.6, solid(P, "black"), cut=1)              # big black nose
    for sx in (-1, 1):
        m.box(hd, sx * 2.6 - 1.0, 14.6, -4.75, sx * 2.6 + 1.0, 15.2, -4.6, solid(P, "black"))   # sleepy eyes
        m.box(hd, sx * 2.6 - 0.2, 12.8, -4.75, sx * 2.6 + 0.2, 14.2, -4.6, solid(P, "red"))
        ball(m, hd, (sx * 5.6, 16.0, 0), 3.0, FUR, layers=3, squash=0.5)                  # huge fluffy ears
        m.round_box(hd, sx * 5.6, -1.4, 1.6, 0.3, 14.6, 17.4, solid(P, "violet"), cut=0)
        spike(m, hd, (sx * 1.6, 18.0, 0), (sx * 0.2, 1, 0), 0.9, 1.6, solid(P, "white"), tip=0.8)
        x0, x1 = sorted((sx * 2.4, sx * 6.0))
        m.box(bd, x0, 5.0, 3.6, x1, 8.0, 3.6, solid(P, "red"), rotation=(0, 0, sx * 15), pivot=(sx * 2.4, 6.5, 3.6))
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 2.0, 4.0, 0))
        rod(m, lg, (sx * 2.0, 4.0, 0), (sx * 2.4, 1.0, -0.6), 2, FUR, extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 2.4 + (f - 1) * 0.6, 0.4, -1.6), (0, -0.3, -1), 0.6, 1.4, solid(P, "red"), tip=0.8)
    tb = m.bone("tail", bd, (0, 4, 4))
    rod(m, tb, (0, 4.0, 4.0), (3.0, 2.0, 8.0), 1, solid(P, "black"), extend=0.1)
    spike(m, tb, (3.0, 2.0, 8.0), (0.6, 0, 1), 1.0, 1.6, solid(P, "black"), tip=0.8)
    for j, (x, y) in enumerate(((-4.0, 20.0), (-5.0, 22.4), (-3.0, 23.4))):              # sleepy bubbles
        ball(m, hd, (x, y, -1.0), 0.8 - j * 0.15, solid(P, "bubble"), layers=1)
    return m
