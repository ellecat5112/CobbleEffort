"""Monimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a tiny pale-green television set with a pink screen face showing two round eyes and a flat little
mouth, a leafy pair of antenna tabs on top and two stubby feet. 0.5 blocks tall.

Front is -z, y is up. 14 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, solid
from _route import pal, tone

HEIGHT = 14
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tiny pale-green television set with a pink screen face, round eyes and leafy antenna tabs"
BASE = {"case": (170, 200, 130), "case_dark": (100, 130, 70), "screen": (240, 190, 200), "black": (24, 24, 30)}
SHINY = {"case": (200, 170, 230), "case_dark": (130, 100, 170), "screen": (190, 230, 250)}


def P(v):
    return pal(BASE, SHINY, v)


CASE = armour(P, "case", "case_dark", trim="case_dark", trim_w=0.3)


def build():
    m = Model("monimon")
    top = m.bone("monimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 2.0, 12.0, CASE, cut=1)
    m.box(bd, -4.6, 3.4, -5.25, 4.6, 10.6, -5.0, solid(P, "screen"))
    for sx in (-1, 1):
        m.box(bd, sx * 2.0 - 0.8, 7.0, -5.4, sx * 2.0 + 0.8, 8.6, -5.3, solid(P, "black"))
        spike(m, bd, (sx * 2.0, 12.0, 0), (sx * 0.6, 1, 0), 2.0, 2.4, CASE, tip=0.8)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 3.0, 2.0, 0))
        spike(m, lg, (sx * 3.0, 2.0, -1.0), (0, -1, -0.2), 1.6, 2.0, CASE, tip=0.8)
    m.box(bd, -1.2, 5.2, -5.4, 1.2, 5.6, -5.3, solid(P, "black"))
    return m
