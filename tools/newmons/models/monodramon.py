"""Monodramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little purple dragon standing hunched, with a cream belly, a golden horn plate on its brow,
yellow eyes, a red scarf-like neck frill, bat-like wing flaps folded on its arms ending in big steel claws, steel
talons on its feet and a short fanned tail. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little purple dragon with a cream belly, a golden horn plate, a red neck frill, folded wing flaps, steel claws and talons"
BASE = {"purple": (140, 120, 190), "purple_dark": (80, 60, 130), "cream": (230, 220, 200), "gold": (230, 190, 90),
        "red": (200, 40, 40), "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "eye": (240, 200, 40),
        "mouth": (130, 30, 40), "tooth": (250, 250, 240)}
SHINY = {"purple": (90, 160, 120), "purple_dark": (40, 100, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "purple", dark="purple_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("monodramon")
    top = m.bone("monodramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 12.0, 0.4), 4.0, HIDE, layers=4, ry=5.0)
    m.round_box(bd, 0, -2.6, 2.6, 1.6, 8.0, 16.0, skin(P, "cream", dark="purple_dark"), cut=1)
    for sx in (-1, 1):                                                                   # red neck frill
        spike(m, bd, (sx * 1.0, 16.0, -3.0), (sx * 0.3, -1, -0.4), 1.4, 5.0, solid(P, "red"), tip=0.8)
    hd = m.bone("head", bd, (0, 17, 0))
    m.round_box(hd, 0, -1.4, 3.0, 3.6, 17.0, 23.0, HIDE, cut=1)
    m.round_box(hd, 0, -5.0, 2.0, 1.6, 17.6, 20.0, HIDE, cut=1)
    m.box(hd, -1.6, 18.6, -6.7, 1.6, 19.2, -6.5, solid(P, "mouth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 21.0, -5.15, max(sx * 1.0, sx * 2.4), 22.0, -4.95, solid(P, "eye"))
        spike(m, hd, (sx * 1.0, 19.2, -6.0), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    m.round_box(hd, 0, -3.4, 1.6, 1.4, 22.4, 23.8, solid(P, "gold"), cut=0)              # golden horn plate
    spike(m, hd, (0, 23.4, -3.0), (0, 1, 0.6), 1.4, 2.6, solid(P, "gold"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 14.0, 0))
        rod(m, ab, (sx * 3.6, 14.0, 0), (sx * 5.4, 10.0, -2.4), 2, HIDE, extend=0.3)
        x0, x1 = sorted((sx * 3.6, sx * 6.4))
        m.box(ab, x0, 8.0, 0.8, x1, 14.0, 0.8, HIDE, rotation=(0, 0, sx * 10), pivot=(sx * 3.6, 14.0, 0.8))  # wing flap
        m.round_box(ab, sx * 5.6, -3.0, 1.6, 1.6, 7.4, 10.0, STEEL, cut=0)               # big steel claws
        for f in range(3):
            spike(m, ab, (sx * 5.6 + (f - 1) * 0.9, 7.4, -3.6), (0, -0.6, -1), 0.8, 2.0, STEEL, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 7.0, 0.6))
        rod(m, lg, (sx * 2.4, 8.0, 0.6), (sx * 2.8, 2.0, 0.6), 3, HIDE, extend=0.4)
        m.round_box(lg, sx * 2.8, -0.6, 1.6, 2.2, 0.0, 1.8, HIDE, cut=0)
        for f in range(3):
            spike(m, lg, (sx * 2.8 + (f - 1) * 0.9, 0.6, -2.8), (0, -0.3, -1), 0.8, 1.6, STEEL, tip=0.8)
    tb = m.bone("tail", bd, (0, 9, 3))
    rod(m, tb, (0, 9.0, 3.0), (0, 5.0, 9.0), 2, HIDE, extend=0.3)
    for s in (-1, 1):
        spike(m, tb, (0, 5.0, 9.0), (s * 0.6, 0.2, 1), 1.0, 3.0, HIDE, tip=0.8)
    return m
