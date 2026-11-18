"""Parrotmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a giant parrot: a huge green bird with great yellow-edged wings, a steel-plated face mask and
curved grey beak, red streaks round its eyes, two long red crest feathers, gold bands on its legs and enormous blue
taloned feet. 25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import armour, feathers, metal, riveted, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a giant green parrot with great yellow-edged wings, a steel face mask, a curved beak, red crest feathers and enormous blue talons"
BASE = {"green": (60, 160, 60), "green_dark": (24, 100, 30), "yellow": (250, 220, 60), "steel": (200, 204, 214),
        "steel_dark": (100, 104, 116), "red": (220, 40, 40), "gold": (230, 180, 60), "blue": (40, 110, 140),
        "blue_dark": (14, 60, 80), "claw": (240, 236, 220), "eye": (60, 60, 140)}
SHINY = {"green": (200, 60, 60), "green_dark": (120, 20, 20), "yellow": (250, 250, 200)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "green", "green_dark", tip="yellow")


def build():
    m = Model("parrotmon")
    top = m.bone("parrotmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    ball(m, bd, (0, 26.0, 1.0), 8.0, feathers(P, "green", "green_dark"), layers=6, ry=10.0, squash=0.9)
    hd = m.bone("head", bd, (0, 34, -4))
    ball(m, hd, (0, 38.0, -4.0), 5.0, feathers(P, "green", "green_dark"), layers=4, ry=4.4)
    m.round_box(hd, 0, -8.4, 3.6, 1.2, 35.6, 41.0, riveted(P, "steel", "steel_dark", spacing=1.4), cut=1)   # mask
    spike(m, hd, (0, 37.0, -10.0), (0, -0.8, -0.6), 2.4, 5.0, metal(P, "steel", dark="steel_dark"), tip=0.8)   # beak
    for sx in (-1, 1):
        m.box(hd, sx * 2.0 - 0.8, 39.0, -9.75, sx * 2.0 + 0.8, 40.0, -9.6, solid(P, "eye"))
        for j in range(3):
            m.box(hd, sx * (3.6 + j * 0.8) - 0.3, 38.0 + j, -8.0, sx * (3.6 + j * 0.8) + 0.3, 40.0 + j, -7.6,
                  solid(P, "red"))
        spike(m, hd, (sx * 1.0, 42.0, -4.0), (sx * 0.3, 1, 0.3), 1.0, 10.0, solid(P, "red"), tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 6.0, 32.0, 2.0))
        feather_wing(m, wb, (side * 6.0, 32.0, 2.0), 22.0, 16.0, 7, FEATH, side=side, sweep=25, droop=-10.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 4.0, 18.0, 0))
        rod(m, lg, (sx * 4.0, 18.0, 0), (sx * 5.0, 8.0, -2.0), 3, armour(P, "blue", "blue_dark"), extend=0.4)
        m.round_box(lg, sx * 4.6, -1.0, 2.0, 2.0, 12.0, 14.0, metal(P, "gold"), cut=0)
        for f in range(3):
            spike(m, lg, (sx * 5.0 + (f - 1) * 1.6, 7.0, -3.0), ((f - 1) * 0.3, -0.6, -1), 1.6, 5.0, solid(P, "claw"),
                  tip=0.8)
    return m
